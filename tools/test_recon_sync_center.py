"""Static safety checks for the Recon-Sync HTA controls."""
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
HTA = ROOT / "platform" / "recon-sync" / "recon-sync-center.hta"
DOC = ROOT / "docs" / "RECON_SYNC_BUTTON.md"


class ReconSyncCenterTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = HTA.read_text(encoding="utf-8")
        cls.doc = DOC.read_text(encoding="utf-8")

    def test_sync_is_explicitly_confirmation_gated(self):
        self.assertIn('id="sync-button" onclick="run(\'sync\', true)"', self.html)
        self.assertIn("window.confirm(", self.html)

    def test_preflight_does_not_sync_and_checks_status_then_verify(self):
        self.assertIn('onclick="preflight()"', self.html)
        self.assertIn("PREFLIGHT (NO SYNC; WRITES EVIDENCE)", self.html)
        self.assertIn('invokeEngine("status")', self.html)
        self.assertIn('invokeEngine("verify")', self.html)

    def test_ui_does_not_claim_google_drive_sync_or_quota_check(self):
        self.assertIn("does <b>not</b> synchronize Google Drive", self.html)
        self.assertIn("quota/permissions", self.html)
        self.assertIn("Google Drive permissions and quota remain UNVERIFIED", self.html)

    def test_exit_code_and_busy_state_are_observed(self):
        self.assertIn("ex.ExitCode", self.html)
        self.assertIn("function setBusy(value)", self.html)
        self.assertIn("GetParentFolderName(fso.GetParentFolderName(fso.GetParentFolderName(p)))", self.html)
        self.assertIn("if (result.code !== 0)", self.html)

    def test_contract_documents_non_destructive_boundaries(self):
        self.assertIn("No automatic conflict resolution", self.doc)
        self.assertIn("Google Drive connector is unavailable", self.doc)
        self.assertIn("canonical source remains authoritative", self.doc.lower())


if __name__ == "__main__":
    unittest.main()
