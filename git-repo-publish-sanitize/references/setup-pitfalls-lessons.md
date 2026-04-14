# Setup, Pitfalls, and Lessons

## Contents

1. Environment setup
2. Pitfalls
3. Lessons

## Environment Setup

### Local tooling

- Prefer system `git`.
- Prefer system `gh` when it is installed and already authenticated.
- If `gh` is missing, use the bundled binary at `/home/xy/.codex/skills/git-repo-publish-sanitize/scripts/gh`.
- Do not depend on `/tmp` copies of `gh` or `/tmp` repo mirrors as part of the normal workflow.

### Local repo prerequisites

- Work in the target repository directly.
- Verify Git identity before the first commit:

```bash
git config user.name
git config user.email
```

- Initialize only when needed:

```bash
git init -b main
```

### GitHub auth prerequisites

- Check auth first:

```bash
gh auth status
```

- If login is missing or expired, re-authenticate:

```bash
gh auth login --hostname github.com --web
```

- If HTTPS pushes prompt for credentials, configure git to reuse `gh` credentials:

```bash
gh auth setup-git --hostname github.com
```

- If the terminal browser flow is unreliable, print the device-login URL instead of launching a browser helper:

```bash
BROWSER=echo gh auth login --hostname github.com --web
```

### Secret-handling prerequisites

- Treat key files, tokens, and credentials as local-only by default.
- Add local-only paths to `.gitignore` before the first publish.
- Verify both ignore state and tracked state:

```bash
git check-ignore -v path/to/secret
git ls-files path/to/secret
```

- If a secret file must exist locally for runtime, document that clearly in repo docs or skill docs.

### Remote-deletion prerequisites

- Repository deletion needs a token with `delete_repo` scope.
- If deletion fails for scope reasons, refresh the token:

```bash
gh auth refresh -h github.com -s delete_repo
```

## Pitfalls

### `.git` writes blocked by sandbox

Symptom:
- `fatal: Unable to create '.git/index.lock': Read-only file system`

Interpretation:
- Local repo metadata is blocked by sandbox policy even though the worktree is visible.

Action:
- Request approval for the specific `git add`, `git commit`, or related command.
- Continue in the same repository. Do not fork the workflow into a temporary clone just to avoid the permission issue.

### GitHub network calls blocked by sandbox

Symptom:
- `socket: operation not permitted`

Interpretation:
- Network access is blocked by sandbox policy, not by GitHub auth itself.

Action:
- Re-run the exact `gh` command with the required approval.
- Do not assume auth is broken until the same command fails outside sandbox.

### `gh` installed but token expired

Symptom:
- `gh auth status` reports the token in `hosts.yml` is no longer valid.

Action:
- Re-run `gh auth login --hostname github.com --web`.
- Re-check `gh auth status` before any destructive remote operation.

### Deletion denied despite valid login

Symptom:
- `HTTP 403` plus a message that `delete_repo` scope is required.

Interpretation:
- The current token is valid for ordinary repo operations but not for deletion.

Action:
- Run `gh auth refresh -h github.com -s delete_repo`.
- Retry deletion only after the scope refresh completes.

### Older `gh` versions use different flags

Symptom:
- `unknown flag: --yes` on `gh repo delete`.

Interpretation:
- The CLI is an older build.

Action:
- Use `gh repo delete owner/name --confirm`.
- Expect similar flag differences in older packaged versions and check `--help` when a familiar flag fails.

### Device login can be hijacked by terminal browsers

Symptom:
- `gh auth login --web` opens `w3m` or another terminal browser and never completes cleanly.

Action:
- Use `BROWSER=echo gh auth login --hostname github.com --web`.
- Open the printed `https://github.com/login/device` URL manually and enter the one-time code.

### `.gitignore` alone does not untrack an existing secret

Symptom:
- The file still appears in `git ls-files` after you add it to `.gitignore`.

Interpretation:
- Ignore rules do not remove files that are already tracked or already staged.

Action:
- Run `git rm --cached path/to/secret`.
- Re-check `git ls-files path/to/secret` before committing the sanitized tree.

### Local cleanup and remote cleanup are different problems

Symptom:
- The local branch is clean, but the leaked commit still exists on GitHub.

Interpretation:
- You fixed current tracking but not published history.

Action:
- Rebuild clean local history first.
- Delete and recreate the remote only if the user wants a clean public history and the sensitive commit already reached GitHub.

### Temporary sanitized copies hide the real problem

Symptom:
- Work drifts into `/tmp` mirrors, alternate clones, or duplicate repos.

Interpretation:
- The workflow is avoiding permission or history complexity instead of fixing it.

Action:
- Return to the real repository.
- Sanitize in place unless the user explicitly wants a separate permanent repo location.

## Lessons

### Publish from the real repo

- Keep the authoritative repo where the user is already working.
- Use the current directory as the source of truth for init, cleanup, and publish.

### Make visibility explicit

- Always pass `--private` or `--public`.
- Do not infer the desired visibility from prior state.

### Verify after every irreversible step

- After commits: run `git status -sb`.
- After secret removal: run `git ls-files path/to/secret`.
- After push or recreation: run `gh repo view --json isPrivate,url,nameWithOwner`.

### Separate local-only files from tracked files early

- The cheapest fix is to ignore secrets before the first commit.
- The expensive fix is rewriting history after the first push.

### Update docs when a file becomes local-only

- If a key path is required for runtime, say so explicitly.
- Pair the `.gitignore` change with doc updates so the next person does not re-add the file by accident.

### Recreate the remote only when history hygiene matters

- If the secret never left the local machine, local cleanup is enough.
- If the secret reached GitHub and the goal is a clean public history, clean the branch and then recreate the remote.
