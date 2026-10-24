# Recon-Sync button: scope and safety contract

## Purpose

Add an explicit, confirmation-gated button to the existing Windows HTA control center. The UI invokes the existing PowerShell engine; it does not introduce a second synchronization engine.

## Verified scope at implementation baseline

- Canonical repository: `phakphum12345/ENTERPRISE_API_ARCHITECTURE_LOGIC_TH`.
- Baseline `main` commit: `81b030060b316deadc405751a0cb7c2b1ff7bb08`.
- Existing engine: `platform/recon-sync/recon-sync-engine.ps1`.
- Existing engine `sync` fetches `canonical/main`, preserves dirty work by creating a preservation branch, and creates a detached worktree. It is Git reconciliation, not a Google Drive file transfer.
- Existing workflow `.github/workflows/recon-continuous-reconciliation.yml` checks out and verifies the exact target SHA and publishes reconciliation evidence.

## Button behavior

1. **PREFLIGHT (NO SYNC; WRITES EVIDENCE)** runs `status`, then `verify`; the existing engine writes evidence records for these commands, so this is not filesystem-read-only. A failed command yields HOLD/FAIL in the UI.
2. **SYNC CANONICAL GIT** requires an explicit confirmation and then invokes the existing `sync` command.
3. The UI displays the combined PowerShell output and process exit code and disables controls while a command is running.
4. The UI explicitly states that Google Drive is not synchronized and Drive permissions/quota are not verified.

## Safety boundaries

- No automatic conflict resolution.
- No `git reset --hard`, `git clean`, force-push, history rewrite, or file deletion is added.
- The UI does not claim a successful Google Drive sync.
- Google Drive connector is unavailable in this environment (disabled by administrator), and the user's local G: drive free space cannot be measured through GitHub. Drive integration must remain HOLD until authenticated access and quota checks can be performed on the actual machine/account.
- Existing canonical source remains authoritative; the button is not merge or release authority.

## Verification

The accompanying unit test checks the safety copy and control wiring statically. The existing Recon workflow runs that test against the exact checked-out revision. Runtime verification still requires launching the HTA on Windows with the repository's configured `canonical` remote.
