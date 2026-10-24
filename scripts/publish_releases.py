#!/usr/bin/env python3
"""Publish only the final maintained patch of each available 3.x/4.x/5.x minor series.

The reviewed versioned casks on work are the publication inventory. An initial .0 is
eligible until superseded in its X.Y series. Beta/RC versions and other majors are
never eligible. This is a maintenance-version policy, not a security certification.
Obsolete GitHub Release records are removed; Git tags and commits are never deleted.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import tempfile
from pathlib import Path

import release_notes
import update_casks as uc

STABLE_VERSION = re.compile(r"[345]\.\d+\.\d+\Z")


def eligible_versions(root: Path) -> list[str]:
    final = {}
    for version in uc.cask_versions(root / "Casks"):
        if not STABLE_VERSION.fullmatch(version):
            continue
        key = uc.series(version)
        if key not in final or uc.vtuple(version) > uc.vtuple(final[key]):
            final[key] = version
    if not final:
        raise ValueError("No eligible 3.x/4.x/5.x casks; refusing to publish or prune Releases")
    return sorted(final.values(), key=uc.vtuple)


def publication_plan(allowed: list[str], releases: list[dict], requested: str = "") -> dict:
    if not allowed:
        raise ValueError("No eligible versions; refusing to prune Releases")
    if requested and requested not in allowed:
        raise ValueError(f"{requested} is not a final maintained cask; allowed: {', '.join(allowed)}")
    desired = [requested] if requested else allowed
    existing = {r["tag_name"]: r for r in releases}
    return {
        "allowed": allowed,
        "create": [v for v in desired if v not in existing],
        "promote": [v for v in desired if v in existing and
                    (existing[v].get("draft") or existing[v].get("prerelease"))],
        "remove": [{"id": r["id"], "tag": r["tag_name"]} for r in releases
                   if r["tag_name"] not in allowed],
    }


def gh_json(repo: str, endpoint: str):
    result = subprocess.run(["gh", "api", f"repos/{repo}/{endpoint}"],
                            check=True, capture_output=True, text=True)
    return json.loads(result.stdout)



def current_latest_tag(repo: str) -> str | None:
    try:
        return gh_json(repo, "releases/latest").get("tag_name")
    except subprocess.CalledProcessError:
        return None

def list_releases(repo: str) -> list[dict]:
    result = subprocess.run(["gh", "api", "--paginate", "--slurp",
                             f"repos/{repo}/releases?per_page=100"],
                            check=True, capture_output=True, text=True)
    return [release for page in json.loads(result.stdout) for release in page]


def publish(root: Path, repo: str, requested: str, ref: str, dry_run: bool) -> dict:
    allowed = eligible_versions(root)
    # Reject an obsolete/manual version before any remote mutation.
    if requested and requested not in allowed:
        raise ValueError(f"{requested} is not a final maintained cask; allowed: {', '.join(allowed)}")
    target = subprocess.check_output(
        ["git", "rev-parse", "--verify", "--end-of-options", f"{ref or 'HEAD'}^{{commit}}"],
        cwd=root, text=True).strip()
    plan = publication_plan(allowed, list_releases(repo), requested)
    print(json.dumps({"target": target, **plan}, indent=2))

    with tempfile.TemporaryDirectory(prefix="egovframe-release-") as directory:
        notes_root = Path(directory)
        (notes_root / "Casks").mkdir()
        # The latest hint describes today's catalog, not the historical target's default.
        (notes_root / "Casks/egovframedev-latest.rb").write_text(
            (root / "Casks/egovframedev-latest.rb").read_text(encoding="utf-8"), encoding="utf-8")
        notes = {}
        for version in plan["create"] + plan["promote"]:
            relative = f"Casks/egovframedev@{version}.rb"
            text = subprocess.check_output(["git", "show", f"{target}:{relative}"], cwd=root, text=True)
            if not re.search(rf'^\s*version "{re.escape(version)}"\s*$', text, re.M):
                raise ValueError(f"{relative} does not declare version {version} at {target}")
            (notes_root / relative).write_text(text, encoding="utf-8")
            notes[version] = notes_root / f"notes-{version}.md"
            notes[version].write_text(release_notes.render(notes_root, version), encoding="utf-8")
        if dry_run:
            print("Dry run: no Release, tag or commit was changed.")
            return plan

        # Publish replacements before removing old Release records. Failure leaves old records intact.
        for version in plan["create"]:
            subprocess.run(["gh", "release", "create", version, "--repo", repo,
                            "--target", target, "--title", f"eGovFrame IDE {version}",
                            "--notes-file", str(notes[version]),
                            f"--latest={'true' if version == allowed[-1] else 'false'}"], check=True)
        for version in plan["promote"]:
            subprocess.run(["gh", "release", "edit", version, "--repo", repo,
                            "--draft=false", "--prerelease=false", "--notes-file", str(notes[version])],
                           check=True)
        for release in plan["remove"]:
            # DELETE /releases/{id} does not remove the corresponding Git tag.
            subprocess.run(["gh", "api", "--method", "DELETE",
                            f"repos/{repo}/releases/{release['id']}"], check=True)
        remaining = list_releases(repo)
        published = [r["tag_name"] for r in remaining if r["tag_name"] in allowed
                     and not r.get("draft") and not r.get("prerelease")]
        if published:
            latest = max(published, key=uc.vtuple)
            if current_latest_tag(repo) != latest:
                subprocess.run(["gh", "release", "edit", latest, "--repo", repo, "--latest"], check=True)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--repo", default=os.environ.get("GH_REPO") or os.environ.get("GITHUB_REPOSITORY") or "eGovFramework/homebrew-egovframe")
    parser.add_argument("--version", default="", help="Publish one eligible version; obsolete versions are rejected")
    parser.add_argument("--ref", default="", help="Commit containing the cask (policy still comes from work)")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    try:
        publish(args.root, args.repo, args.version, args.ref, args.dry_run)
    except (ValueError, subprocess.CalledProcessError) as error:
        parser.exit(1, f"{error}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
