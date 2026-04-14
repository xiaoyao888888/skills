---
name: git-repo-publish-sanitize
description: Initialize a local directory as a Git repository, prepare focused commits, publish it to GitHub with gh, remove tracked secrets from history, and delete/recreate remote repositories when a leaked file has already been pushed. Use when Codex needs to create or repair a Git/GitHub repo lifecycle end to end, especially for current-directory publishing, secret cleanup, visibility changes, or remote recreation without relying on /tmp work copies.
---

# Git Repo Publish Sanitize

## Overview

Use this skill to handle Git and GitHub repository lifecycle work from an existing local directory.

Keep the workflow in place inside the target repository. Do not copy the repo to `/tmp` or build a sanitized replacement there. If sandbox or permission limits block `.git` writes or network access, request the required approval and continue in the same repository.

## Tooling

- Prefer system `git`.
- Prefer system `gh` when it is installed and authenticated.
- If `gh` is missing, use the bundled CLI at `/home/xy/.codex/skills/git-repo-publish-sanitize/scripts/gh`.
- Do not use `gh` binaries from `/tmp`.

## Workflow

### 1. Inspect scope first

- Run `git status -sb` if the directory is already a repository.
- If it is not a repository, inspect the directory contents before initializing Git.
- Identify whether the user wants:
  - local initialization only
  - create and push a new GitHub repository
  - add docs like `README.md` or `AGENTS.md`
  - remove sensitive files from tracking
  - delete and recreate the remote repository
  - switch between private and public visibility

### 2. Initialize locally

- Run `git init -b main` when the directory is not already a repository.
- Configure or verify `git config user.name` and `git config user.email`.
- Stage only intended files.
- Add or update `.gitignore` before the first commit when local-only files should stay on disk but never be tracked.
- Commit with a terse message.

### 3. Audit sensitive files before pushing

- Inspect filenames for likely secrets before publishing:
  - `key`
  - `secret`
  - `token`
  - `credential`
  - `passwd`
  - `password`
  - project-specific private key names
- Treat private keys, tokens, and credential material as local-only files.
- Keep local-only secret paths in `.gitignore`.
- Update skill or repo docs if a path must exist locally but must never be committed.

### 4. Publish to GitHub

- Verify GitHub CLI auth with `gh auth status`.
- Run `gh auth setup-git` when HTTPS pushes need to reuse GitHub CLI credentials.
- If the repo does not exist, create it with `gh repo create ... --source=. --remote=origin --push`.
- Use `--private` or `--public` explicitly. Do not assume the correct visibility.
- After push, verify:
  - `git status -sb`
  - `git remote -v`
  - `gh repo view --json isPrivate,url,nameWithOwner`

### 5. Sanitize leaked history in place

If a sensitive file was already committed or pushed:

- Add the path to `.gitignore`.
- Remove it from the index with `git rm --cached <path>`.
- Update any docs that mention the file so they describe it as local-only.
- Rebuild clean history in the same repository. Prefer an orphan branch workflow:
  1. `git checkout --orphan sanitized-main`
  2. `git rm -rf --cached .`
  3. `git add -A`
  4. Verify the leaked path is no longer tracked with `git ls-files <path>`
  5. Commit the sanitized tree
- Replace the old branch name only after the sanitized commit is correct.
- Do not create a `/tmp` clone or alternate sanitized copy just to work around the cleanup.

### 6. Delete and recreate the remote when required

Use this only when the leaked history already reached GitHub and the user wants a clean remote history.

- Check whether the current `gh` token has enough scope.
- If deletion fails because of missing scope, run:
  - `gh auth refresh -h github.com -s delete_repo`
- For older `gh` versions, repository deletion uses `--confirm` rather than `--yes`.
- Delete the old remote:
  - `gh repo delete owner/name --confirm`
- Recreate the repo from the sanitized local checkout:
  - `gh repo create <name> --private|--public --source=. --remote=origin --push`

## Validation

- Confirm the sensitive path is absent from tracked files with `git ls-files <path>`.
- Confirm the working tree is clean with `git status -sb`.
- Confirm the remote URL and visibility with `gh repo view`.
- When recreating a repo, confirm the new HEAD commit is the sanitized commit you intended to publish.

## Read This Reference When Needed

- See `references/command-recipes.md` for concrete command sequences covering initialization, publish, in-place sanitization, and delete/recreate flows.
- See `references/setup-pitfalls-lessons.md` for environment setup, common failure modes, and operational lessons from real Git/GitHub publish and cleanup work.
