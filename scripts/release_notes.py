#!/usr/bin/env python3
"""Print the GitHub Release notes (Markdown) for one eGovFrame IDE version of this tap.

The notes are read from Casks/egovframedev@X.Y.Z.rb, so they always match what `brew install`
downloads: file names, download URLs and SHA-256 per architecture.

Usage: scripts/release_notes.py X.Y.Z [--root DIR] [--historical]
       --historical: the cask is no longer in the tap (it was superseded); omit the install commands
       scripts/release_notes.py --latest [--root DIR]   (prints only the version of egovframedev-latest)
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import update_casks as uc  # noqa: E402

ARCH_LABEL = {"arm": "Apple Silicon (ARM64)", "intel": "Intel (x86_64)"}
def default_tap() -> str:
    repo = os.environ.get("GITHUB_REPOSITORY", "eGovFramework/homebrew-egovframe")
    return repo.lower().replace("/homebrew-", "/")


TAP = os.environ.get("HOMEBREW_TAP") or default_tap()
RELEASE_PAGE = "https://www.egovframe.go.kr/home/sub.do?menuNo=40"


def cask_assets(text: str, version: str) -> dict[str, tuple[str, str]]:
    per_arch = uc.SHA_BLOCK.search(text)
    if per_arch:
        urls = uc.dmg_urls(text, version, uc.DOWNLOAD_BASE)
        return {"arm": (urls["arm"], per_arch.group(3)),
                "intel": (urls["intel"], per_arch.group(6))}
    # The maintained 3.10.0 and 4.0.0 casks provide only the Intel Mac-64bit DMG.
    scalar = re.search(r'^\s*sha256 "([0-9a-f]{64})"', text, re.M)
    url = uc.URL_LINE.search(text)
    if not scalar or not url or "-Mac-64bit.dmg" not in url.group(1):
        raise ValueError(f"{version}: unsupported cask download/hash format")
    expanded = (url.group(1).replace("#{version.major_minor}", ".".join(version.split(".")[:2]))
                .replace("#{version}", version))
    return {"intel": (expanded, scalar.group(1))}


def render(root: Path, version: str, historical: bool = False) -> str:
    casks = root / "Casks"
    path = casks / f"egovframedev@{version}.rb"
    if not path.exists():
        raise SystemExit(f"no cask Casks/egovframedev@{version}.rb")
    text = path.read_text(encoding="utf-8")
    assets = cask_assets(text, version)
    rows = "\n".join(
        f"| {ARCH_LABEL[arch]} | [`{url.rsplit('/', 1)[1]}`]({url}) | `{sha}` |"
        for arch, (url, sha) in assets.items())
    footer = [
        "The DMGs are served by the official eGovFrame host; this release does not host them. "
        f"Version detected from [{RELEASE_PAGE}]({RELEASE_PAGE}).",
        "",
    ]
    if historical:
        install_block = [
            f"Historical release: `egovframedev@{version}` was superseded by a newer patch of the same series and is "
            "no longer in the tap's default branch. The cask is still available at this tag.",
            "",
        ]
    else:
        install = [f"brew tap {TAP}", f"brew install egovframedev@{version}"]
        latest_file = casks / "egovframedev-latest.rb"
        if latest_file.exists() and uc.latest_version(casks) == version:
            install.append("# or always the newest: brew install egovframedev-latest")
        install_block = ["```bash", *install, "```", ""]
    return "\n".join([
        f"eGovFrame IDE **{version}** for macOS, as Homebrew cask `egovframedev@{version}`.",
        "",
        "| Architecture | Download (official host) | SHA-256 |",
        "| --- | --- | --- |",
        rows,
        "",
        *install_block,
        *footer,
    ])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("version", nargs="?")
    ap.add_argument("--latest", action="store_true", help="print the version of egovframedev-latest and exit")
    ap.add_argument("--historical", action="store_true", help="cask is no longer in the tap: no install commands")
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    args = ap.parse_args()
    if args.latest:
        print(uc.latest_version(args.root / "Casks"))
        return 0
    if not args.version:
        ap.error("version required")
    print(render(args.root, args.version, args.historical), end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
