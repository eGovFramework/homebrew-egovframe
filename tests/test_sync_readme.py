"""Regression tests for configured root-document generation and relative links."""
import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import sync_readme as sr  # noqa: E402

LANGS = ("en", "ko", "es", "vi", "ar", "fr")

SOURCE = """# Title

[![English](https://example.com/en.svg)](README.en.md)
[![한국어](https://example.com/ko.svg)](README.ko.md "Korean")
[License](../LICENSE) | [Anchor](#install) | [Site](https://example.com/a/../b) | [Mail](mailto:a@b.c)
[Abs](/already/root.md) | [Guide](code-signing-guideline/code-signing-guideline.{lang}.md#top) | [Dir](assets/)
<img src="assets/logo.png"> and `[code](README.en.md)`

```
[fenced](README.en.md)
```

[ref]: ../.github/MAINTENANCE.md
"""


def make_repo(default_language="en"):
    """A throwaway repository with sources whose first line names their language."""
    root = Path(tempfile.mkdtemp())
    (root / "docs/code-signing-guideline").mkdir(parents=True)
    languages = {lang: f"docs/README.{lang}.md" for lang in LANGS}
    guides = {lang: f"docs/code-signing-guideline/code-signing-guideline.{lang}.md" for lang in LANGS}
    contributions = {lang: f"docs/contributing/CONTRIBUTING.{lang}.md" for lang in LANGS}
    security = {lang: f"docs/security/SECURITY.{lang}.md" for lang in LANGS}
    config = [f"default_language: {default_language}", "languages:"]
    config += [f"  {lang}: {path}" for lang, path in languages.items()]
    config += ["code_signing_guideline:"] + [f"  {lang}: {path}" for lang, path in guides.items()]
    for group, paths in (("contributing", contributions), ("security", security)):
        config += [f"{group}:"] + [f"  {lang}: {path}" for lang, path in paths.items()]
    (root / "docs/config.yml").write_text("\n".join(config) + "\n", encoding="utf-8")
    for lang in LANGS:
        (root / languages[lang]).write_text(f"LANG={lang}\n" + SOURCE.format(lang=lang), encoding="utf-8")
        (root / guides[lang]).write_text(f"GUIDE={lang}\n[Back](../README.{lang}.md)\n", encoding="utf-8")
        contribution = root / contributions[lang]
        contribution.parent.mkdir(parents=True, exist_ok=True)
        contribution.write_text(
            f"CONTRIBUTING={lang}\n[Security](../security/SECURITY.{lang}.md)\n"
            "[Maintenance](../../.github/MAINTENANCE.md)\n", encoding="utf-8")
        policy = root / security[lang]
        policy.parent.mkdir(parents=True, exist_ok=True)
        policy.write_text(
            f"SECURITY={lang}\n[Casks](../../Casks)\n[Workflows](../../.github/workflows)\n"
            f"[English](SECURITY.en.md)\n[Supported casks](../README.{lang}.md)\n", encoding="utf-8")
    return root


class RebaseTest(unittest.TestCase):
    def test_relative_targets_move_to_the_new_folder(self):
        self.assertEqual(sr.rebase_target("README.ko.md", "docs"), "docs/README.ko.md")
        self.assertEqual(sr.rebase_target("../LICENSE", "docs"), "LICENSE")
        self.assertEqual(sr.rebase_target("../.github/MAINTENANCE.md", "docs"), ".github/MAINTENANCE.md")
        self.assertEqual(sr.rebase_target("./x/../a.md#frag", "docs/g"), "docs/g/a.md#frag")
        self.assertEqual(sr.rebase_target("assets/", "docs"), "docs/assets/")
        self.assertEqual(sr.rebase_target("<a b.md>", "docs"), "<docs/a b.md>")
        self.assertEqual(sr.rebase_target("../../README.en.md", "docs/g"), "README.en.md")

    def test_absolute_and_anchor_targets_are_untouched(self):
        for target in ("https://example.com/a", "mailto:a@b.c", "#install", "/root.md", "//cdn/x.png", ""):
            self.assertEqual(sr.rebase_target(target, "docs"), target)

    def test_same_folder_is_a_no_op(self):
        self.assertEqual(sr.rebase_target("./a.md", "docs", "docs"), "./a.md")

    def test_markdown_html_and_reference_links(self):
        out = sr.rebase_links(SOURCE.format(lang="en"), "docs")
        self.assertIn("](docs/README.en.md)", out)
        self.assertIn('](docs/README.ko.md "Korean")', out)
        self.assertIn("[License](LICENSE)", out)
        self.assertIn("[Anchor](#install)", out)
        self.assertIn("[Site](https://example.com/a/../b)", out)
        self.assertIn("[Mail](mailto:a@b.c)", out)
        self.assertIn("[Abs](/already/root.md)", out)
        self.assertIn("](docs/code-signing-guideline/code-signing-guideline.en.md#top)", out)
        self.assertIn("[Dir](docs/assets/)", out)
        self.assertIn('src="docs/assets/logo.png"', out)
        self.assertIn("[ref]: .github/MAINTENANCE.md", out)
        # code is not a link
        self.assertIn("`[code](README.en.md)`", out)
        self.assertIn("```\n[fenced](README.en.md)\n```", out)

    def test_nested_badge_links_rebase_only_the_destination_that_is_relative(self):
        line = "[![x](../img/a.svg)](README.md)"
        self.assertEqual(sr.rebase_links(line, "docs"), "[![x](img/a.svg)](docs/README.md)")


class SyncTest(unittest.TestCase):

    def repo(self, *args, **kwargs):
        root = make_repo(*args, **kwargs)
        self.addCleanup(shutil.rmtree, root)
        return root

    def run_main(self, root, output=None):
        argv = ["--root", str(root)] + (["--github-output", str(output)] if output else [])
        with contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return sr.main(argv)

    def test_default_language_english(self):
        root = self.repo("en")
        self.assertEqual(self.run_main(root), 0)
        self.assertTrue((root / "README.md").read_text().startswith("LANG=en\n"))
        self.assertTrue((root / "code-signing-guideline.md").read_text().startswith("GUIDE=en\n"))

    def test_default_language_korean_selects_korean_sources(self):
        root = self.repo("ko")
        self.assertEqual(self.run_main(root), 0)
        readme = (root / "README.md").read_text()
        self.assertTrue(readme.startswith("LANG=ko\n"))
        self.assertIn("](docs/README.en.md)", readme)  # language buttons stay explicit, English included
        guide = (root / "code-signing-guideline.md").read_text()
        self.assertTrue(guide.startswith("GUIDE=ko\n"))
        self.assertIn("[Back](docs/README.ko.md)", guide)

    def test_community_links_stay_on_the_viewed_repository_and_branch(self):
        root = self.repo("ko")
        self.assertEqual(self.run_main(root), 0)
        contribution = (root / ".github/CONTRIBUTING.md").read_text()
        self.assertTrue(contribution.startswith("CONTRIBUTING=ko\n"))
        base = "/"
        self.assertIn(f"[Security]({base}docs/security/SECURITY.ko.md)", contribution)
        self.assertIn(f"[Maintenance]({base}.github/MAINTENANCE.md)", contribution)
        policy = (root / ".github/SECURITY.md").read_text()
        self.assertTrue(policy.startswith("SECURITY=ko\n"))
        self.assertIn(f"[Casks]({base}Casks)", policy)
        self.assertIn(f"[Workflows]({base}.github/workflows)", policy)
        self.assertIn(f"[English]({base}docs/security/SECURITY.en.md)", policy)
        self.assertIn(f"[Supported casks]({base}docs/README.ko.md)", policy)

    def test_github_output_reports_changed_then_noop(self):
        root = self.repo("ko")
        out = root / "github_output"
        self.assertEqual(self.run_main(root, out), 0)
        self.assertIn("changed=true\n", out.read_text())
        self.assertIn("files=README.md,code-signing-guideline.md,.github/CONTRIBUTING.md,.github/SECURITY.md\n",
                      out.read_text())

        before = {p: (root / p).read_bytes() for p in sr.ENTRIES.values()}
        out.write_text("")
        self.assertEqual(self.run_main(root, out), 0)
        self.assertEqual(out.read_text(), "changed=false\nfiles=\n")
        self.assertEqual({p: (root / p).read_bytes() for p in before}, before)

    def test_changing_one_source_rewrites_only_that_root_entry(self):
        root = self.repo("en")
        self.run_main(root)
        guide = root / "docs/code-signing-guideline/code-signing-guideline.en.md"
        guide.write_text(guide.read_text() + "more\n", encoding="utf-8")
        out = root / "github_output"
        self.run_main(root, out)
        self.assertEqual(out.read_text(), "changed=true\nfiles=code-signing-guideline.md\n")

    def test_changing_default_language_switches_the_root_entry(self):
        root = self.repo("en")
        self.run_main(root)
        config = root / "docs/config.yml"
        config.write_text(config.read_text().replace("default_language: en", "default_language: fr"))
        self.run_main(root)
        self.assertTrue((root / "README.md").read_text().startswith("LANG=fr\n"))

    def test_sync_can_be_limited_to_the_readme(self):
        root = self.repo("en")
        self.assertEqual(sr.sync(root, groups=("languages",)), ["README.md"])
        self.assertFalse((root / "code-signing-guideline.md").exists())

    def test_errors_return_1_and_write_nothing(self):
        root = self.repo("xx")
        self.assertEqual(self.run_main(root), 1)
        self.assertFalse((root / "README.md").exists())

        root = self.repo("ko")
        (root / "docs/README.ko.md").unlink()
        self.assertEqual(self.run_main(root), 1)

    def test_missing_security_source_does_not_partially_update_other_entrypoints(self):
        root = self.repo("ko")
        readme = root / "README.md"
        readme.write_text("Existing default entry\n")
        (root / "docs/security/SECURITY.ko.md").unlink()
        self.assertEqual(self.run_main(root), 1)
        self.assertEqual(readme.read_text(), "Existing default entry\n")
        self.assertFalse((root / ".github/CONTRIBUTING.md").exists())

    def test_duplicate_config_keys_are_rejected(self):
        root = self.repo("en")
        config = root / "docs/config.yml"
        config.write_text(config.read_text().replace("languages:\n", "languages:\n  en: docs/README.en.md\n", 1))
        with self.assertRaises(sr.ConfigError):
            sr.load_config(root)
        self.assertEqual(self.run_main(root), 1)



if __name__ == "__main__":
    unittest.main()
