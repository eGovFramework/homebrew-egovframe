"""Tests for scripts/update_casks.py against a local fake release server (no network)."""
import hashlib
import shutil
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import sync_readme  # noqa: E402
import update_casks as uc  # noqa: E402

ARCH_FILE = {"arm": "AArch64", "intel": "x86_64"}


def page(*versions):
    return "<html>" + "".join(f"<li>개발자용 개발환경 {v} 릴리즈</li>" for v in versions) + "</html>"


class FakeMaven:
    """Serves DMG bytes at the official path layout; `files` maps URL path -> bytes."""

    def __init__(self):
        self.files = {}
        self.fail_next = {}
        outer = self

        class Handler(BaseHTTPRequestHandler):
            def _serve(self, body):
                if outer.fail_next.get(self.path, 0) > 0:
                    outer.fail_next[self.path] -= 1
                    self.send_response(503)
                    self.end_headers()
                    return
                data = outer.files.get(self.path)
                if data is None:
                    self.send_response(404)
                    self.end_headers()
                    return
                self.send_response(200)
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                if body:
                    self.wfile.write(data)

            def do_GET(self):
                self._serve(True)

            def do_HEAD(self):
                self._serve(False)

            def log_message(self, *a):
                pass

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self.base = f"http://127.0.0.1:{self.server.server_port}"
        threading.Thread(target=self.server.serve_forever, daemon=True).start()

    def publish(self, version, arches=("arm", "intel")):
        major_minor = ".".join(version.split(".")[:2])
        shas = {}
        for arch in arches:
            data = f"dmg {version} {arch}".encode()
            path = (f"/egovframework_v{major_minor}/2_DevelopmentEnvironment/eGovFrame-Dev/"
                    f"{version}/eGovFrameDev-{version}-macOS-{ARCH_FILE[arch]}.dmg")
            self.files[path] = data
            shas[arch] = hashlib.sha256(data).hexdigest()
        return shas

    def close(self):
        self.server.shutdown()
        self.server.server_close()


class UpdateCasksTest(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.tmp)
        shutil.copytree(REPO / "tests/fixtures/Casks", self.tmp / "Casks")
        # Frozen 5.0.2 baseline, not the checked-in docs: those move on with every release.
        shutil.copytree(REPO / "tests/fixtures/docs", self.tmp / "docs")
        sync_readme.sync(self.tmp, groups=("languages",))
        self.maven = FakeMaven()
        self.addCleanup(self.maven.close)
        original_delay = uc.RETRY_DELAY
        uc.RETRY_DELAY = 0
        self.addCleanup(setattr, uc, "RETRY_DELAY", original_delay)

    def run_update(self, html, dry_run=False):
        return uc.run(self.tmp, html, self.maven.base, dry_run, badge_check=False)

    def casks(self):
        return sorted(p.name for p in (self.tmp / "Casks").iterdir())

    def snapshot(self):
        return {p.relative_to(self.tmp).as_posix(): p.read_bytes()
                for p in self.tmp.rglob("*") if p.is_file()}

    def test_new_patch_replaces_previous_in_series(self):
        shas = self.maven.publish("5.0.3")
        before = self.snapshot()
        result = self.run_update(page("5.0.2", "5.0.3"))

        self.assertEqual(result, {"added": ["5.0.3"], "removed": ["5.0.2"], "skipped": []})
        self.assertIn("egovframedev@5.0.3.rb", self.casks())
        self.assertNotIn("egovframedev@5.0.2.rb", self.casks())

        # Same file as the 5.0.2 cask, except name, version and the two hashes.
        old = before["Casks/egovframedev@5.0.2.rb"].decode()
        expected = (old.replace('cask "egovframedev@5.0.2"', 'cask "egovframedev@5.0.3"')
                       .replace('version "5.0.2"', 'version "5.0.3"'))
        for arch_old, key in (("17aa276ec0775afc5169c9dbfab56bbdd94d4f74940a371c1b46608d59e57c32", "arm"),
                              ("cbe4400bacd588b622b798409dc3f4e92bbb67f5365db1b335372864a0788b23", "intel")):
            expected = expected.replace(arch_old, shas[key])
        self.assertEqual((self.tmp / "Casks/egovframedev@5.0.3.rb").read_text(), expected)

        latest = (self.tmp / "Casks/egovframedev-latest.rb").read_text()
        self.assertEqual(latest, expected.replace('cask "egovframedev@5.0.3"', 'cask "egovframedev-latest"'))

        # Untouched casks stay byte-identical.
        for name in ("egovframedev@4.3.1.rb", "egovframedev@4.0.0.rb", "egovframedev@3.10.0.rb"):
            self.assertEqual((self.tmp / "Casks" / name).read_bytes(), before[f"Casks/{name}"])

    def test_readmes_follow_the_casks(self):
        self.maven.publish("5.0.3")
        self.run_update(page("5.0.3"))
        for name, _label, style in uc.READMES:
            flat = f"{style}.svg"
            text = (self.tmp / name).read_text()
            self.assertIn("brew install egovframedev@5.0.3\nbrew install egovframedev@4.3.1\n", text)
            self.assertNotIn("egovframedev@5.0.2", text)
            self.assertIn(f"/badges/5.0.3/{flat})", text)
            self.assertNotIn("/badges/5.0.2/", text)
            self.assertIn("5.0.3](https://raw", text)

    def test_all_six_localized_readmes_are_updated(self):
        self.assertEqual([name for name, _label, _style in uc.READMES],
                         [f"docs/README.{lang}.md" for lang in ("en", "ko", "es", "vi", "ar", "fr")])
        self.maven.publish("5.0.3")
        self.run_update(page("5.0.3"))
        for name, _label, _style in uc.READMES:
            self.assertIn("brew install egovframedev@5.0.3\n", (self.tmp / name).read_text(), name)
        self.assertFalse((self.tmp / "docs/README.md").exists())

    def test_root_readme_is_regenerated_with_the_update(self):
        before = (self.tmp / "README.md").read_text()
        self.assertNotIn("egovframedev@5.0.3", before)
        self.maven.publish("5.0.3")
        self.run_update(page("5.0.3"))
        root = (self.tmp / "README.md").read_text()
        self.assertIn("brew install egovframedev@5.0.3\nbrew install egovframedev@4.3.1\n", root)
        self.assertIn("/badges/5.0.3/flat.svg)", root)
        self.assertIn("](docs/README.en.md)", root)
        config = sync_readme.load_config(self.tmp)
        self.assertEqual(root, sync_readme.render_entry(self.tmp, config, "languages"))

    def test_dry_run_leaves_root_readme_untouched(self):
        self.maven.publish("5.0.3")
        before = (self.tmp / "README.md").read_bytes()
        self.run_update(page("5.0.3"), dry_run=True)
        self.assertEqual((self.tmp / "README.md").read_bytes(), before)

    def test_new_minor_series_keeps_previous_series(self):
        self.maven.publish("5.1.0")
        result = self.run_update(page("5.0.2", "5.1.0"))
        self.assertEqual(result["removed"], [])
        self.assertIn("egovframedev@5.0.2.rb", self.casks())
        self.assertIn("egovframedev@5.1.0.rb", self.casks())
        self.assertIn('version "5.1.0"', (self.tmp / "Casks/egovframedev-latest.rb").read_text())
        readme = (self.tmp / "docs/README.en.md").read_text()
        self.assertIn("brew install egovframedev@5.1.0\nbrew install egovframedev@5.0.2\n", readme)

    def test_release_without_both_dmgs_is_skipped_and_changes_nothing(self):
        self.maven.publish("5.0.3", arches=("arm",))
        before = self.snapshot()
        result = self.run_update(page("5.0.2", "5.0.3"))
        self.assertEqual(result, {"added": [], "removed": [], "skipped": ["5.0.3"]})
        self.assertEqual(self.snapshot(), before)

    def test_up_to_date_and_second_run_are_no_ops(self):
        before = self.snapshot()
        self.assertEqual(self.run_update(page("5.0.2"))["added"], [])
        self.assertEqual(self.snapshot(), before)

        self.maven.publish("5.0.3")
        self.run_update(page("5.0.3"))
        after_first = self.snapshot()
        self.assertEqual(self.run_update(page("5.0.3"))["added"], [])
        self.assertEqual(self.snapshot(), after_first)

    def test_two_new_releases_in_one_run_end_at_the_newest(self):
        self.maven.publish("5.0.3")
        self.maven.publish("5.0.4")
        result = self.run_update(page("5.0.3", "5.0.4"))
        self.assertEqual(result["added"], ["5.0.3", "5.0.4"])
        self.assertEqual(sorted(result["removed"]), ["5.0.2", "5.0.3"])
        self.assertIn('version "5.0.4"', (self.tmp / "Casks/egovframedev-latest.rb").read_text())
        self.assertEqual([c for c in self.casks() if c.startswith("egovframedev@5.")], ["egovframedev@5.0.4.rb"])

    def test_dry_run_detects_without_downloading_or_writing(self):
        self.maven.publish("5.0.3")
        before = self.snapshot()
        result = self.run_update(page("5.0.3"), dry_run=True)
        self.assertEqual(result["added"], ["5.0.3"])
        self.assertEqual(self.snapshot(), before)

    def test_versions_older_than_automation_floor_are_ignored(self):
        # An old release that is somehow newer than the latest cask must not be generated
        # from the 5.x template (different DMG naming before 5.0.0).
        (self.tmp / "Casks/egovframedev-latest.rb").write_text(
            (self.tmp / "Casks/egovframedev-latest.rb").read_text().replace('version "5.0.2"', 'version "4.3.0"'))
        self.maven.publish("4.3.2")
        self.assertEqual(self.run_update(page("4.3.2"))["added"], [])

        readme = self.tmp / "docs/README.en.md"
        text = readme.read_text().replace("brew install egovframedev@4.3.1\n", "brew install egovframedev@4.3.1\n\n", 1)
        readme.write_text(text)
        self.maven.publish("5.0.3")
        with self.assertRaises(SystemExit):
            self.run_update(page("5.0.3"))

    def test_transient_server_errors_are_retried(self):
        shas = self.maven.publish("5.0.3")
        for path in self.maven.files:
            self.maven.fail_next[path] = 2  # first HEAD and first GET of each DMG answer 503
        result = self.run_update(page("5.0.3"))
        self.assertEqual(result["added"], ["5.0.3"])
        self.assertIn(shas["arm"], (self.tmp / "Casks/egovframedev@5.0.3.rb").read_text())

    def test_missing_dmg_is_an_answer_not_retried(self):
        calls = []
        original = uc.http
        uc.http = lambda url, *a, **k: (calls.append(url), original(url, *a, **k))[1]
        self.addCleanup(setattr, uc, "http", original)
        self.assertFalse(uc.exists(self.maven.base + "/nope.dmg"))
        self.assertEqual(len(calls), 1)

    def test_persistent_server_errors_surface_after_retries(self):
        self.maven.publish("5.0.3")
        for path in self.maven.files:
            self.maven.fail_next[path] = 99
        with self.assertRaises(Exception) as ctx:
            self.run_update(page("5.0.3"))
        self.assertTrue(uc.transient(ctx.exception))

    def test_discover_versions_dedupes_and_sorts_numerically(self):
        html = page("5.0.2", "4.3.1", "5.0.10", "5.0.2", "3.10.0")
        self.assertEqual(uc.discover_versions(html), ["3.10.0", "4.3.1", "5.0.2", "5.0.10"])


class RepositoryConsistencyTest(unittest.TestCase):
    """The checked-in tap must satisfy what the update script assumes."""

    def test_latest_cask_is_the_newest_versioned_cask(self):
        versions = uc.cask_versions(REPO / "Casks")
        newest = max(versions, key=uc.vtuple)
        self.assertEqual(uc.latest_version(REPO / "Casks"), newest)
        latest = (REPO / "Casks/egovframedev-latest.rb").read_text()
        self.assertEqual(latest.replace('cask "egovframedev-latest"', f'cask "egovframedev@{newest}"', 1),
                         versions[newest].read_text())

    def test_readmes_list_every_versioned_cask_newest_first(self):
        expected = uc.render_install_list(list(uc.cask_versions(REPO / "Casks")))
        for name, _label, _style in uc.READMES:
            listed = [l for l in (REPO / name).read_text().split("\n") if uc.INSTALL_LINE.match(l)]
            self.assertEqual(listed, expected, name)

    def test_readme_badges_show_the_latest_version(self):
        latest = uc.latest_version(REPO / "Casks")
        for name, _label, style in uc.READMES:
            block = uc.BADGE_BLOCK.search((REPO / name).read_text())
            self.assertIsNotNone(block, name)
            self.assertIn(f"/badges/{latest}/{style}.svg", block.group(0), name)

    def test_template_cask_is_recognised_by_the_generator(self):
        text = (REPO / "Casks/egovframedev-latest.rb").read_text()
        self.assertIsNotNone(uc.SHA_BLOCK.search(text))
        urls = uc.dmg_urls(text, "9.8.7", uc.DOWNLOAD_BASE)
        self.assertEqual(urls["arm"], f"{uc.DOWNLOAD_BASE}/egovframework_v9.8/2_DevelopmentEnvironment/"
                                      "eGovFrame-Dev/9.8.7/eGovFrameDev-9.8.7-macOS-AArch64.dmg")
        self.assertTrue(urls["intel"].endswith("eGovFrameDev-9.8.7-macOS-x86_64.dmg"))


if __name__ == "__main__":
    unittest.main()
