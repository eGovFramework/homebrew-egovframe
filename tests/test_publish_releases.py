import tempfile
import unittest
from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "scripts"))
import publish_releases as pr


class PublicationPolicyTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "Casks").mkdir()

    def add(self, *versions):
        for version in versions:
            (self.root / "Casks" / f"egovframedev@{version}.rb").write_text(
                f'cask "egovframedev@{version}" do\n  version "{version}"\nend\n')

    def test_final_patch_of_each_minor_not_just_highest_major(self):
        self.add("5.0.0", "5.0.1", "5.0.2", "4.3.0", "4.3.1", "4.2.0", "4.2.1",
                 "4.1.0", "4.1.1", "4.0.0", "3.10.0", "3.9.0", "3.9.1",
                 "5.1.0-beta", "5.1.0-rc1", "6.0.0", "2.7.0")
        self.assertEqual(pr.eligible_versions(self.root),
                         ["3.9.1", "3.10.0", "4.0.0", "4.1.1", "4.2.1", "4.3.1", "5.0.2"])

    def test_initial_release_is_allowed_only_until_a_patch_exists(self):
        self.add("3.10.0")
        self.assertEqual(pr.eligible_versions(self.root), ["3.10.0"])
        self.add("3.10.1")
        allowed = pr.eligible_versions(self.root)
        self.assertEqual(allowed, ["3.10.1"])
        with self.assertRaises(ValueError):
            pr.publication_plan(allowed, [], "3.10.0")

    def test_beta_does_not_replace_the_final_stable_version(self):
        self.add("5.0.2", "5.0.3-beta", "5.0.3-rc1")
        self.assertEqual(pr.eligible_versions(self.root), ["5.0.2"])

    def test_obsolete_releases_are_pruned_but_existing_finals_are_retained(self):
        releases = [{"id": 1, "tag_name": "5.0.0"}, {"id": 2, "tag_name": "5.0.1"},
                    {"id": 3, "tag_name": "5.0.2"}, {"id": 4, "tag_name": "4.1.0"}]
        plan = pr.publication_plan(["3.10.0", "4.1.1", "5.0.2"], releases)
        self.assertEqual(plan["create"], ["3.10.0", "4.1.1"])
        self.assertEqual(plan["remove"], [{"id": 1, "tag": "5.0.0"},
                                          {"id": 2, "tag": "5.0.1"},
                                          {"id": 4, "tag": "4.1.0"}])
        self.assertEqual(plan["promote"], [])

    def test_manual_backfill_cannot_bypass_final_policy(self):
        for requested in ("5.0.0", "5.0.1", "5.0.3-rc1", "6.0.0"):
            with self.subTest(requested=requested), self.assertRaises(ValueError):
                pr.publication_plan(["3.10.0", "4.1.1", "5.0.2"], [], requested)

    def test_selected_lower_series_can_be_published_without_other_creations(self):
        plan = pr.publication_plan(["3.10.0", "4.1.1", "5.0.2"], [], "3.10.0")
        self.assertEqual(plan["create"], ["3.10.0"])
        self.assertEqual(plan["allowed"], ["3.10.0", "4.1.1", "5.0.2"])

    def test_final_version_marked_as_prerelease_is_promoted(self):
        plan = pr.publication_plan(["5.0.2"], [{"id": 1, "tag_name": "5.0.2", "prerelease": True}])
        self.assertEqual(plan["create"], [])
        self.assertEqual(plan["promote"], ["5.0.2"])
        self.assertEqual(plan["remove"], [])

    def test_empty_inventory_cannot_delete_every_release(self):
        with self.assertRaises(ValueError):
            pr.eligible_versions(self.root)
        with self.assertRaises(ValueError):
            pr.publication_plan([], [{"id": 1, "tag_name": "5.0.2"}])


if __name__ == "__main__":
    unittest.main()
