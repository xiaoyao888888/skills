# Command Recipes

## Repo Initialization

Use this when the current directory is not yet a Git repository.

```bash
git init -b main
git config user.name
git config user.email
git status -sb
```

Stage intentionally:

```bash
git add -A
git diff --cached --stat
git commit -m "Initial import"
```

## Local-Only Secret Handling

Add local-only secret paths to `.gitignore` before committing:

```bash
git check-ignore -v rk-gerrit/config/robot_verifier
git ls-files rk-gerrit/config/robot_verifier
```

If the file is tracked already, remove it from the index but keep it on disk:

```bash
git rm --cached rk-gerrit/config/robot_verifier
git add .gitignore
git add README.md rk-gerrit/SKILL.md
```

## GitHub Auth and Publish

Check auth first:

```bash
gh auth status
```

If `gh` is not installed in `PATH`, use the bundled binary:

```bash
/home/xy/.codex/skills/git-repo-publish-sanitize/scripts/gh auth status
```

Create and push a private repo:

```bash
gh repo create skills --private --source=. --remote=origin --push
```

Create and push a public repo:

```bash
gh repo create skills --public --source=. --remote=origin --push
```

Verify:

```bash
git status -sb
git remote -v
gh repo view owner/name --json isPrivate,url,nameWithOwner
```

## In-Place History Sanitization

Use this when a sensitive file was already committed and you need a clean local history without using `/tmp`.

```bash
git checkout --orphan sanitized-main
git rm -rf --cached .
git add -A
git ls-files rk-gerrit/config/robot_verifier
git status -sb
git commit -m "Initial sanitized import"
```

After the sanitized commit is verified, move branch names as needed using normal branch commands.

## Delete and Recreate the Remote

Refresh scopes if deletion is blocked:

```bash
gh auth refresh -h github.com -s delete_repo
```

Delete the existing repository. Older `gh` versions use `--confirm`:

```bash
gh repo delete owner/name --confirm
```

Recreate and push the sanitized repository:

```bash
gh repo create skills --public --source=. --remote=origin --push
```

Verify the final state:

```bash
gh repo view owner/name --json isPrivate,url,nameWithOwner
git rev-parse HEAD
git status -sb
```
