"""Tests for scripts/release_notes.py against the checked-in casks."""
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import release_notes as rn  # noqa: E402
import update_casks as uc  # noqa: E402


class ReleaseNotesTest(unittest.TestCase):
    def test_notes_match_the_cask_hashes_and_urls(self):
        version = uc.latest_version(REPO / "Casks")
        cask = (REPO / "Casks" / f"egovframedev@{version}.rb").read_text()
        sha = uc.SHA_BLOCK.search(cask)
        notes = rn.render(REPO, version)
        self.assertIn(f"`{sha.group(3)}`", notes)
        self.assertIn(f"`{sha.group(6)}`", notes)
        self.assertIn(f"eGovFrameDev-{version}-macOS-AArch64.dmg", notes)
        self.assertIn(f"eGovFrameDev-{version}-macOS-x86_64.dmg", notes)
        major_minor = ".".join(version.split(".")[:2])
        self.assertIn(f"/egovframework_v{major_minor}/2_DevelopmentEnvironment/eGovFrame-Dev/{version}/", notes)
        self.assertIn(f"brew install egovframedev@{version}", notes)

    def test_latest_hint_only_for_the_latest_version(self):
        latest = uc.latest_version(REPO / "Casks")
        self.assertIn("egovframedev-latest", rn.render(REPO, latest))
        notes = rn.render(REPO / "tests/fixtures", "4.3.1")
        self.assertIn("eGovFrameDev-4.3.1-Mac-AArch64.dmg", notes)
        self.assertNotIn("egovframedev-latest", notes)

    def test_intel_only_3x_and_4x_notes_do_not_advertise_arm_downloads(self):
        fixtures = REPO / "tests/fixtures"
        expected = {
            "3.10.0": "c0b36911ba9e527d7f6f87481b183fcf2095756c0b84e36ce28c33c9094feb32",
            "4.0.0": "4ee5be1d0f67b35bfdf79194831a2b2b36a9836763821e80eebbccc94a711c06",
        }
        for version, digest in expected.items():
            with self.subTest(version=version):
                notes = rn.render(fixtures, version)
                self.assertIn(f"eGovFrameDev-{version}-Mac-64bit.dmg", notes)
                self.assertIn(f"`{digest}`", notes)
                self.assertIn("| Intel (x86_64) |", notes)
                self.assertNotIn("| Apple Silicon", notes)
                self.assertIn(f"brew install egovframedev@{version}", notes)

    def test_unknown_version_fails(self):
        with self.assertRaises(SystemExit):
            rn.render(REPO, "0.0.1")


if __name__ == "__main__":
    unittest.main()
