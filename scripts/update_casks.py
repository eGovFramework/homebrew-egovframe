#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Detect new eGovFrame IDE releases and add them to this tap.

Reads the release list on egovframe.go.kr (same page and regex as the casks' `livecheck`),
and for every version newer than the current `egovframedev-latest`:

  1. checks that the macOS DMG exists for both architectures (HEAD, must be 200),
  2. downloads both DMGs and computes SHA-256,
  3. writes Casks/egovframedev@X.Y.Z.rb from the current latest cask,
  4. removes older patch casks of the same X.Y series (upstream's convention:
     one cask per minor series),
  5. rewrites Casks/egovframedev-latest.rb, the install lists and the version badge
     between the `latest-badge` markers in the six docs/README.<lang>.md sources, then
     regenerates the root README.md from them (scripts/sync_readme.py), so the root
     entry is never stale even when the sync-readme workflow cannot run.

Needs PyYAML (see the PEP 723 header of sync_readme.py). Exit status: 0 = ok (changes or none), 1 = error.
With --github-output PATH it appends `changed`, `added`, `removed`, `skipped` for Actions.
"""
from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import sync_readme

PAGE_URL = "https://www.egovframe.go.kr/home/sub.do?menuNo=40"
PAGE_REGEX = re.compile(r"개발자용\s개발환경\s(\d+(?:\.\d+)+)")
DOWNLOAD_BASE = "https://maven.egovframe.go.kr/publist/HDD1/public"
BADGE_URL = "https://raw.githubusercontent.com/leejongyoung/egovframe-badge/main/badges"
ARCHES = ("arm", "intel")
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Safari/605.1.15"
# Releases before this have no `macOS` DMG naming; the tap's templates only fit 5.x and later.
MIN_AUTOMATED = (5, 0, 0)

CASK_NAME = re.compile(r'^cask "[^"]+" do', re.M)
VERSION_LINE = re.compile(r'^(\s*)version "[^"]+"', re.M)
SHA_BLOCK = re.compile(r'(\s*)sha256 arm:(\s+)"([0-9a-f]{64})",\n(\s+)intel:(\s+)"([0-9a-f]{64})"')
URL_LINE = re.compile(r'^\s*url "([^"]+)"', re.M)
INSTALL_LINE = re.compile(r"^brew install egovframedev@\S+$")
BADGE_BLOCK = re.compile(r"(<!-- latest-badge:start -->\n)[^\n]*((?:\n[^\n]*)*?\n<!-- latest-badge:end -->)")
READMES = (
    ("docs/README.en.md", "eGovFrame", "flat"),
    ("docs/README.ko.md", "전자정부표준프레임워크", "flat-ko"),
    ("docs/README.es.md", "Marco Estándar de Gobierno Electrónico", "flat-es"),
    ("docs/README.vi.md", "Khung chuẩn Chính phủ điện tử", "flat-vi"),
    ("docs/README.ar.md", "الإطار القياسي للحكومة الإلكترونية", "flat-ar"),
    ("docs/README.fr.md", "Cadre standard de l'administration électronique", "flat-fr"),
)


def vtuple(version: str) -> tuple[int, ...]:
    return tuple(int(p) for p in version.split("."))


def series(version: str) -> tuple[int, int]:
    t = vtuple(version)
    return (t[0], t[1] if len(t) > 1 else 0)


RETRY_DELAY = 15  # seconds, multiplied by the attempt number; tests set it to 0


def http(url: str, method: str = "GET", timeout: int = 60):
    req = urllib.request.Request(url, method=method, headers={"User-Agent": USER_AGENT})
    return urllib.request.urlopen(req, timeout=timeout)


def transient(error: Exception) -> bool:
    """Network hiccups and 5xx/429 are worth retrying; other HTTP statuses are answers."""
    if isinstance(error, urllib.error.HTTPError):
        return error.code >= 500 or error.code == 429
    return isinstance(error, (urllib.error.URLError, TimeoutError, ConnectionError))


def with_retries(fn, attempts: int = 4):
    for attempt in range(1, attempts + 1):
        try:
            return fn()
        except Exception as e:
            if not transient(e) or attempt == attempts:
                raise
            print(f"  request failed ({e}); retry {attempt}/{attempts - 1}", file=sys.stderr)
            time.sleep(RETRY_DELAY * attempt)


def fetch_text(url: str) -> str:
    with http(url) as r:
        return r.read().decode("utf-8", "replace")


def exists(url: str) -> bool:
    def head() -> bool:
        try:
            with http(url, "HEAD") as r:
                return r.status == 200
        except urllib.error.HTTPError as e:
            if e.code in (403, 404, 405):
                e.close()
                return False
            raise

    return with_retries(head)


def discover_versions(page_html: str) -> list[str]:
    return sorted(set(PAGE_REGEX.findall(page_html)), key=vtuple)


def cask_versions(casks_dir: Path) -> dict[str, Path]:
    found = {}
    for path in casks_dir.glob("egovframedev@*.rb"):
        found[path.stem.split("@", 1)[1]] = path
    return found


def latest_version(casks_dir: Path) -> str:
    text = (casks_dir / "egovframedev-latest.rb").read_text(encoding="utf-8")
    m = VERSION_LINE.search(text)
    if not m:
        raise SystemExit("egovframedev-latest.rb has no version line")
    return re.search(r'version "([^"]+)"', m.group(0)).group(1)


def dmg_urls(template: str, version: str, download_base: str) -> dict[str, str]:
    """Expand the template cask's url for a version, for each arch."""
    m = URL_LINE.search(template)
    if not m:
        raise SystemExit("template cask has no url line")
    raw = m.group(1).replace(DOWNLOAD_BASE, download_base)
    major, minor = vtuple(version)[:2]
    am = re.search(r'arch arm: "([^"]+)", intel: "([^"]+)"', template)
    if not am:
        raise SystemExit("template cask has no arch line")
    arch_names = dict(zip(ARCHES, am.groups()))
    out = {}
    for arch in ARCHES:
        out[arch] = (raw.replace("#{version.major_minor}", f"{major}.{minor}")
                        .replace("#{version}", version)
                        .replace("#{arch}", arch_names[arch]))
    return out


def sha256_of(url: str) -> str:
    def download() -> str:
        digest = hashlib.sha256()
        done = 0
        started = time.monotonic()
        with http(url, timeout=120) as r:
            while chunk := r.read(1 << 20):
                digest.update(chunk)
                done += len(chunk)
        print(f"  sha256 {digest.hexdigest()[:12]}… {done / 1e6:.0f} MB in {time.monotonic() - started:.0f}s", file=sys.stderr)
        return digest.hexdigest()

    return with_retries(download)


def render_cask(template: str, name: str, version: str, sha: dict[str, str]) -> str:
    text = CASK_NAME.sub(f'cask "{name}" do', template, count=1)
    text = VERSION_LINE.sub(lambda m: f'{m.group(1)}version "{version}"', text, count=1)

    def sha_repl(m: re.Match) -> str:
        return f'{m.group(1)}sha256 arm:{m.group(2)}"{sha["arm"]}",\n{m.group(4)}intel:{m.group(5)}"{sha["intel"]}"'

    new, n = SHA_BLOCK.subn(sha_repl, text, count=1)
    if n != 1:
        raise SystemExit("template cask sha256 block not recognised")
    return new


def render_install_list(versions: list[str]) -> list[str]:
    return [f"brew install egovframedev@{v}" for v in sorted(versions, key=vtuple, reverse=True)]


def rewrite_readme(text: str, versions: list[str], latest: str, badge_ver: str, korean: bool = False,
                   *, label: str | None = None, style: str | None = None) -> str:
    lines = text.split("\n")
    idx = [i for i, l in enumerate(lines) if INSTALL_LINE.match(l)]
    if idx:
        if idx != list(range(idx[0], idx[-1] + 1)):
            raise SystemExit("install list in README is not one contiguous block")
        lines[idx[0]:idx[-1] + 1] = render_install_list(versions)
    text = "\n".join(lines)
    style = style or ("flat-ko" if korean else "flat")
    label = label or ("전자정부표준프레임워크" if korean else "eGovFrame")
    badge = (f"[![{label}]({BADGE_URL}/unversioned/{style}.svg)]"
             f"(https://www.egovframe.go.kr/)")
    return BADGE_BLOCK.sub(lambda m: f"{m.group(1)}{badge}{m.group(2)}", text)

def pick_badge_version(latest: str, check: bool) -> str:
    if not check:
        return latest
    for candidate in (latest, ".".join(latest.split(".")[:2])):
        if exists(f"{BADGE_URL}/{candidate}/flat.svg"):
            return candidate
    return ".".join(latest.split(".")[:2])


def verify_existing(root: Path, version: str, download_base: str) -> int:
    casks = root / "Casks"
    path = cask_versions(casks).get(version)
    if path is None:
        print(f"no cask for {version}", file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")
    m = SHA_BLOCK.search(text)
    expected = {"arm": m.group(3), "intel": m.group(6)}
    template = (casks / "egovframedev-latest.rb").read_text(encoding="utf-8")
    bad = 0
    for arch, url in dmg_urls(template, version, download_base).items():
        print(f"verify {version} {arch}: {url}", file=sys.stderr)
        got = sha256_of(url)
        ok = got == expected[arch]
        print(f"  {'OK' if ok else 'MISMATCH'} expected {expected[arch][:12]}… got {got[:12]}…")
        bad += not ok
    return 1 if bad else 0


def run(root: Path, page_html: str, download_base: str, dry_run: bool, badge_check: bool) -> dict:
    casks = root / "Casks"
    current = latest_version(casks)
    template = (casks / "egovframedev-latest.rb").read_text(encoding="utf-8")
    known = cask_versions(casks)
    candidates = [v for v in discover_versions(page_html)
                  if vtuple(v) > vtuple(current) and vtuple(v) >= MIN_AUTOMATED and v not in known]
    result = {"added": [], "removed": [], "skipped": []}

    for version in candidates:
        urls = dmg_urls(template, version, download_base)
        missing = [a for a, u in urls.items() if not exists(u)]
        if missing:
            print(f"skip {version}: no DMG yet for {', '.join(missing)}", file=sys.stderr)
            result["skipped"].append(version)
            continue
        if dry_run:
            print(f"would add {version}")
            result["added"].append(version)
            continue
        print(f"add {version}", file=sys.stderr)
        sha = {arch: sha256_of(url) for arch, url in urls.items()}
        (casks / f"egovframedev@{version}.rb").write_text(
            render_cask(template, f"egovframedev@{version}", version, sha), encoding="utf-8")
        for old, path in cask_versions(casks).items():
            if old != version and series(old) == series(version) and vtuple(old) < vtuple(version):
                path.unlink()
                result["removed"].append(old)
        result["added"].append(version)

    if result["added"] and not dry_run:
        newest = max(result["added"], key=vtuple)
        newest_text = (casks / f"egovframedev@{newest}.rb").read_text(encoding="utf-8")
        (casks / "egovframedev-latest.rb").write_text(
            CASK_NAME.sub('cask "egovframedev-latest" do', newest_text, count=1), encoding="utf-8")
        versions = list(cask_versions(casks))
        badge_ver = pick_badge_version(newest, badge_check)
        for name, label, style in READMES:
            path = root / name
            if path.exists():
                path.write_text(
                    rewrite_readme(path.read_text(encoding="utf-8"), versions, newest, badge_ver,
                                   label=label, style=style),
                    encoding="utf-8")
        sync_readme.sync(root, groups=("languages",))
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--page-url", default=PAGE_URL)
    ap.add_argument("--download-base", default=DOWNLOAD_BASE, help="replaces the official DMG host (tests)")
    ap.add_argument("--dry-run", action="store_true", help="detect only: no download, no file changes")
    ap.add_argument("--no-badge-check", action="store_true")
    ap.add_argument("--verify", metavar="VERSION", help="download an existing cask's DMGs and compare SHA-256")
    ap.add_argument("--github-output", type=Path, default=os.environ.get("GITHUB_OUTPUT"))
    args = ap.parse_args()

    if args.verify:
        return verify_existing(args.root, args.verify, args.download_base)

    page = with_retries(lambda: fetch_text(args.page_url))
    if not discover_versions(page):
        print("no versions found on the release page — layout changed?", file=sys.stderr)
        return 1
    result = run(args.root, page, args.download_base, args.dry_run, not args.no_badge_check)
    print(f"current latest: {latest_version(args.root / 'Casks')}")
    for key in ("added", "removed", "skipped"):
        print(f"{key}: {', '.join(result[key]) or '-'}")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if result['added'] and not args.dry_run else 'false'}\n")
            for key in ("added", "removed", "skipped"):
                f.write(f"{key}={','.join(result[key])}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
