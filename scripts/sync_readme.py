#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["PyYAML==6.0.3"]
# ///
"""Generate default-language documentation entrypoints from docs/config.yml.

Localized README, code-signing, contribution and security sources live in docs/.
Entries stay at the repository root or .github/ as required by GitHub discovery.
Relative Markdown/HTML links and images are re-based to each entrypoint's folder.

Exit status: 0 = ok (changed or not), 1 = configuration or source error.
With --github-output PATH (default: $GITHUB_OUTPUT) it appends `changed=true|false`
and `files=<comma separated entrypoint paths that were rewritten>` for Actions.
"""
from __future__ import annotations

import argparse
import os
import posixpath
import re
import sys
from pathlib import Path

import yaml

# config group -> generated entrypoint
ENTRIES = {
    "languages": "README.md",
    "code_signing_guideline": "code-signing-guideline.md",
    "contributing": ".github/CONTRIBUTING.md",
    "security": ".github/SECURITY.md",
}
CONFIG = "docs/config.yml"


class ConfigError(Exception):
    pass


class _UniqueKeyLoader(yaml.SafeLoader):
    """SafeLoader that rejects duplicate mapping keys instead of silently keeping the last."""


def _construct_mapping(loader: _UniqueKeyLoader, node: yaml.MappingNode, deep: bool = False):
    seen = set()
    for key_node, _ in node.value:
        key = loader.construct_object(key_node, deep=deep)
        if key in seen:
            raise ConfigError(f"duplicate key {key!r} (line {key_node.start_mark.line + 1})")
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)


_UniqueKeyLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _construct_mapping)


def load_config(root: Path) -> dict:
    path = root / CONFIG
    try:
        config = yaml.load(path.read_text(encoding="utf-8"), Loader=_UniqueKeyLoader)
    except FileNotFoundError:
        raise ConfigError(f"{CONFIG} not found") from None
    except yaml.YAMLError as error:
        raise ConfigError(f"{CONFIG}: {error}") from None
    if not isinstance(config, dict):
        raise ConfigError(f"{CONFIG} must be a mapping")
    return config


# --- link re-basing -------------------------------------------------------------------

_FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
_CODE_SPAN = re.compile(r"(`[^`\n]*`)")
_INLINE_DEST = re.compile(r"(\]\(\s*)(<[^<>\n]*>|[^\s()<>]+)")
_REF_DEF = re.compile(r"^(\s{0,3}\[[^\]\n]+\]:\s*)(<[^<>\n]*>|\S+)")
_HTML_ATTR = re.compile(r"""(\b(?:href|src)\s*=\s*)(["'])([^"'\n]*)\2""")
_SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")


def rebase_target(target: str, src_dir: str, dest_dir: str = ".") -> str:
    """Re-base one link destination written in `src_dir` so it works from `dest_dir`.

    Both directories are repository-relative POSIX paths. Absolute URLs, root-absolute
    paths and pure anchors are returned unchanged; `?query` and `#fragment` are kept.
    `dest_dir="/"` emits repository-root-relative paths for GitHub's branch-aware renderer.
    """
    angle = target.startswith("<") and target.endswith(">")
    raw = target[1:-1] if angle else target
    if not raw or raw.startswith(("#", "/")) or _SCHEME.match(raw):
        return target
    path = re.match(r"[^?#]*", raw).group(0)
    if not path or posixpath.normpath(src_dir) == posixpath.normpath(dest_dir):
        return target
    resolved = posixpath.normpath(posixpath.join(src_dir, path))
    new = posixpath.join("/", resolved) if dest_dir == "/" else posixpath.relpath(resolved, dest_dir)
    if path.endswith("/") and not new.endswith("/"):
        new += "/"
    new += raw[len(path):]
    return f"<{new}>" if angle else new


def rebase_links(text: str, src_dir: str, dest_dir: str = ".") -> str:
    """Re-base relative Markdown links/images, reference definitions and HTML href/src.

    Fenced code blocks and inline code spans are left untouched.
    """
    def dest(m: re.Match) -> str:
        return m.group(1) + rebase_target(m.group(2), src_dir, dest_dir)

    def html(m: re.Match) -> str:
        return f"{m.group(1)}{m.group(2)}{rebase_target(m.group(3), src_dir, dest_dir)}{m.group(2)}"

    out, fence = [], None
    for line in text.split("\n"):
        m = _FENCE.match(line)
        if m:
            marker = m.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            out.append(line)
            continue
        if fence is not None:
            out.append(line)
            continue
        line = _REF_DEF.sub(dest, line)
        parts = _CODE_SPAN.split(line)
        for i in range(0, len(parts), 2):  # odd items are code spans
            parts[i] = _HTML_ATTR.sub(html, _INLINE_DEST.sub(dest, parts[i]))
        out.append("".join(parts))
    return "\n".join(out)


# --- sync -----------------------------------------------------------------------------

def source_for(config: dict, group: str) -> str:
    default_lang = config.get("default_language", "en")
    mapping = config.get(group)
    if not isinstance(mapping, dict) or default_lang not in mapping:
        raise ConfigError(f"default_language {default_lang!r} not found in {group!r} mapping")
    return str(mapping[default_lang])


def render_entry(root: Path, config: dict, group: str) -> str:
    source = source_for(config, group)
    source_path = root / source
    if not source_path.is_file():
        raise ConfigError(f"source file {source} not found")
    src_dir = posixpath.dirname(posixpath.normpath(source)) or "."
    dest_dir = posixpath.dirname(ENTRIES[group]) or "."
    if dest_dir == ".github":
        # Root-relative links work in file previews and on GitHub's Security policy tab.
        # GitHub supplies the viewed repository and branch, including unmerged PR branches.
        dest_dir = "/"
    return rebase_links(source_path.read_text(encoding="utf-8"), src_dir, dest_dir)


def sync(root: Path, groups: tuple[str, ...] = tuple(ENTRIES)) -> list[str]:
    """Rewrite the entrypoints of `groups` that differ; return repository-relative paths."""
    config = load_config(root)
    rendered = {group: render_entry(root, config, group) for group in groups}
    changed = []
    for group, content in rendered.items():
        target = root / ENTRIES[group]
        current = target.read_text(encoding="utf-8") if target.exists() else None
        if current != content:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            changed.append(ENTRIES[group])
    return changed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--root", type=Path, default=Path(__file__).resolve().parent.parent)
    ap.add_argument("--github-output", type=Path, default=os.environ.get("GITHUB_OUTPUT"))
    args = ap.parse_args(argv)

    try:
        changed = sync(args.root)
    except ConfigError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1

    for name in changed:
        print(f"Updated {name}")
    if not changed:
        print("Documentation entrypoints already up to date")
    if args.github_output:
        with open(args.github_output, "a", encoding="utf-8") as f:
            f.write(f"changed={'true' if changed else 'false'}\n")
            f.write(f"files={','.join(changed)}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
