# Commit message rules


## Assistant behavior

assistant:
infer_type_from_diff: true
summarize_by_files: true
refuse_empty_changes: true
ask_for_clarification_if:

- "diff is very large"
- "change purpose is ambiguous"
use_staged_files_only: true
max_total_message_length: 1200

**IMPORTANT**: Exclude unstaged/untracked files from the commit message.

- Derive the subject/body ONLY from staged changes (`git diff --cached`).
- Do NOT mention files listed under "Changes not staged for commit" or
  "Untracked files" in `git status`.

## General style rules

style:
language: "en"
tense: "imperative"          # e.g., "Add", "Fix", "Update"
max_subject_length: 72
max_body_line_length: 72
include_scope: true          # allow "feat(ui): ..." style
require_body_for_types:

- feat
- fix
- refactor

## Commit types and examples (Conventional Commits style)

types:
feat:    "A new feature for the user or system."
fix:     "A bug fix."
docs:    "Documentation-only changes."
style:   "Code style changes (formatting, missing semicolons, etc.)."
refactor:"Code changes that neither fix a bug nor add a feature."
test:    "Adding or adjusting tests."
chore:   "Maintenance tasks, tooling, configs."

examples:
good:

- "feat(api): add pagination to user endpoint"
- |
  fix(auth): handle expired refresh tokens

  - Return 401 when token is expired
  - Add integration test for refresh flow
  - |
      docs(readme): document local setup steps

      Clarify Node.js version and required env vars.
bad:
- "update stuff"
- "fixed it"
- "misc changes"

## Structure rules

structure:
subject:
required: true
pattern: "^(feat|fix|docs|style|refactor|test|chore)(\\([^)]+\\))?: .+$"
body:
bullet_points_preferred: true
explain_why_not_how: true
include_issue_reference: true  # e.g. "Refs #123" or "Closes #456"

## Issue and PR references

references:
keywords:
close:

- "Closes"
- "Fixes"

reference:

- "Refs"
- "See"

auto_link_issue_prefix: "#"

## Project-specific guidance

project:
mention_breaking_changes: true
breaking_change_format: |
BREAKING CHANGE: <short explanation>

    <optional detailed explanation>

avoid_words:

- "temp"
- "wip"
- "test commit"
