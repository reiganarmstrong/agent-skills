---
name: pr-walkthrough
description: Write a clear, plain-English PR title, description, and line-by-line inline walkthrough comments on a pull request so a human reviewer can read the diff top-to-bottom without hunting for context. Use only when the user explicitly requests pr-walkthrough by name, such as $pr-walkthrough or /pr-walkthrough.
disable-model-invocation: true
---

# PR Walkthrough

Turn a pull request diff into a guided tour for a human reviewer: a crisp title, a structured plain-English description, and short inline review comments anchored on each meaningful change.

Write for a teammate who knows the repository at a high level, not what was in the author's head while coding.

## Non-negotiable rules

- **Plain English, no hype.** Use short sentences, active voice, and concrete facts. Never use filler or AI clichés ("comprehensive", "seamlessly", "robust", "leverages", "ensures clean separation of concerns", "enhances maintainability", emojis, or "Note:" preambles).
- **Explain *why* and *behavior*, not syntax.** State what a piece of code does for its caller, why it is shaped that way, and what happens when it fails or when an option is omitted.
- **Be honest about limits and leftovers.** Call out deliberate exclusions, unaddressed edge cases, local-only runs, or unrelated lines inherited from earlier commits. Never invent test counts, metrics, or behavior you did not verify in the diff or by running a command.
- **Anchor only on diff lines.** Every inline comment must attach to an actual line present in the PR diff. Never guess line numbers from memory.
- **Preserve PR state.** Do not mark a draft PR ready for review, do not merge, and do not modify code unless the user asked you to.
- **Use the available PR tool.** Prefer dedicated PR tools if available; otherwise use the repository's CLI (such as `gh`).

---

## 1. Inspect the PR, stack, and diff first

Before writing anything:

1. Read the current PR's title, body, base branch, head branch, head SHA, draft status, and any existing review comments (so you don't duplicate them).
2. Check if this PR is stacked on or split from another PR (check the base branch and recent PRs). Note the related PR numbers (`#N`) so you can reference them accurately.
3. Read the full diff against the PR's base branch (`git diff <base>..HEAD` or the PR diff). Read new files in full so you understand how the pieces fit together.
4. Check if the repository has a PR template or contribution guide; honor any required fields while keeping the voice and structure below.

---

## 2. Write the PR title

Keep the title to one plain-English line with no trailing period:

- **Scoped to one area/subsystem:** `<area>: <lowercase verb phrase>`
  - Good: `http-client: add retry backoff and per-request timeout overrides`
  - Bad: `HttpClient: Comprehensive Retry Backoff & Timeout Enhancement.`
- **New top-level feature:** plain sentence case
  - Good: `Add offline CSV export for monthly usage reports`
  - Bad: `Feat: Implement Offline CSV Export Feature for Monthly Usage Reports`

Avoid awkward Title Case for internal terms mid-title.

---

## 3. Write the PR description

Skip rigid boilerplate templates (like "Blast Radius" or empty checklists) unless the repo requires them. Build the body from only the sections that actually help a reviewer understand this PR:

```markdown
## Summary

[If stacked or split, one line here: e.g. "Stacked on #12. Review #12 first." or "Split out of #12 so the shared client changes can be reviewed separately."]

[1-2 sentences in plain English: what this PR adds or changes, and why.]

[Optional: bullet links to new or updated docs on this branch.]

### What this PR does

1. **[Bold lead-in sentence.]** [2-4 sentences explaining the concrete behavior, inputs, outputs, and guardrails.]
2. **[Bold lead-in sentence.]** [Same structure. Aim for 2-5 numbered items total.]

[Optional: 1-2 compact `text` or `diff` blocks (5-15 lines each) showing a changed call tree, command flow, or file layout when it is faster to scan than prose.]

## How it connects to existing code   <!-- or "How it builds on #N" -->

[Optional section when the PR integrates with existing modules or earlier PRs.]

- **[Component or seam]** in [`path/to/file.py`](https://github.com/<org>/<repo>/blob/<headSha>/path/to/file.py#L42). [1-2 sentences on how it reuses or extends it, and what stays unchanged.]

[Optional 1 sentence on deliberate exclusions or differences from existing paths.]

## [Optional focused section: e.g. "What <concept> is and why it was added", "Defaults", or "Scoring"]

[Include only if there is a non-obvious concept, default choice, or small reference table (2-4 columns) the reviewer needs.]

## Other changes

- `path/to/config`: [one-line reason for supporting edits like dependencies, packaging, CI, `.gitignore`, lockfiles, or tests.]
```

### Description rules

- **Lead with the stack note** if this PR builds on another PR.
- **Link to exact commit SHAs** (`.../blob/<headSha>/path#L<line>`) when citing specific functions or lines in the body, so links don't drift later.
- **Keep diagrams small.** Use plain `text` or `diff` fences, never sprawling diagrams.
- **Omit sections that don't earn their space.** A small PR may only need `## Summary` and `## Other changes`.

---

## 4. Plan the inline walkthrough comments

Walk through the diff file by file and attach short comments directly on the code so the reviewer never has to guess *why* something is there.

### What to comment on vs. skip

| Target | Action | What to say |
| --- | --- | --- |
| New or changed class, public function, CLI command, or non-trivial helper | **Comment** on its `def` / `class` / declaration line | What it does, key invariants, failure behavior, and how callers use it. |
| Important constants, schemas, or default tables | **Comment** on the declaration line | Why these values were chosen and what breaks or changes if edited. |
| Small edits in existing files | **Comment** on the changed hunk line | Why this line changed and what stays unchanged for existing callers. |
| Deleted files or large deleted blocks | **Comment** on line 1 (or the removed declaration, `side: "old"`) | Why it is safe to delete or where the code moved. |
| Config, build, CI, `.gitignore`, lockfiles | **Comment** once per meaningful block | Why the dependency, rule, or packaging entry was added. |
| Templates, prompts, SQL/CSS/JS assets | **Comment** once at line 1 | What the file renders or instructs, and any key constraints (e.g., escaping, offline-only). |
| Test fixtures, helpers, and each test function | **Comment** on each helper and test `def` | What scenario it sets up, what is faked vs. real, and what regression makes it fail. |
| Mechanical boilerplate (imports, formatting-only edits) | **Skip** | No value added. |
| Prose docs (`README.md`, guides) | **Skip** | The prose already explains itself. |

### How to write each inline comment

- **Length:** 1 to 3 short sentences (roughly 15–60 words).
- **Start with a direct verb or noun phrase.** Do not start with *"This function..."*, *"Here we..."*, *"In this commit..."*, or *"Note that..."*.
- **Name concrete details:** exact filenames, flags, error conditions, exit codes, and related PR numbers (`#N`).
- **State failure and fallback behavior** whenever it matters (e.g., atomic writes, partial failure handling, backwards compatibility).

### Good vs. bad examples

**Production function**
- **Bad:** *"This function validates the config object to ensure everything is properly set up and raises a ValueError if there are any issues."*
- **Good:** *"Runs when a config is created and raises if settings conflict—for example, setting a temperature when thinking is enabled. Fails fast locally before any API request is sent."*

**Small edit to existing code**
- **Bad:** *"Made this function public so it can be imported elsewhere."*
- **Good:** *"Made public (was `_write_csv` in #5) so `exporter.py` writes CSVs with the same UTF-8 BOM formatting Excel expects."*

**Deleted code**
- **Bad:** *"Removed unused file."*
- **Good:** *"Deleted since nothing on `main` imports it. Template loading already lives in `templates.py`."*

**Config / dependency**
- **Bad:** *"Added `prompts/*.txt` to package data."*
- **Good:** *"Ships the reviewer instruction files with the installed package alongside the templates and price list."*

**Test function**
- **Bad:** *"Tests that the cost limit works properly."*
- **Good:** *"Sets the fake client to return 1,000,000 output tokens ($0.50 against a $0.01 limit), so the run must stop, exit 1, and record the limit reason in `run.json`."*

---

## 5. Verify line numbers and post safely

Follow these steps in order so comments never fail validation or get duplicated:

1. **Update the PR title and body** (keep `draft` status unchanged unless explicitly asked).
2. **Verify every `(path, line)` against the actual diff** before posting comments. Every `side: "new"` line must appear in a `+` or context line of `git diff <base>..HEAD` for that file (prefer the exact `+` line of the declaration or change).
3. **Post inline comments as a `comment` review** (verdict `comment`, no redundant summary review body).
4. **Batch large walkthroughs.** Never send more than **35 comments** in a single review API call—large single-review payloads frequently trigger HTTP 500 errors or tool item limits. Split into sequential batches (e.g., core/config files, then CLI/UI, then tests).
5. **Check before retrying on any error.** If a review submission returns a 500 or times out, read the PR's existing review threads first—GitHub sometimes commits the comments before returning an error. Only post comments that are actually missing.

---

## 6. Final check before replying

Verify all six before finishing:

- [ ] Title is plain English, matches the repo/stack convention, and has no trailing period.
- [ ] Body states stack/split context up front (if applicable) and contains no unverified claims or boilerplate fluff.
- [ ] Every changed code, config, template, and test file has concise walkthrough comments explaining *why* and *behavior*.
- [ ] No comments were posted on `README.md` or mechanical import-only lines.
- [ ] Zero duplicate comments (checked via PR threads if any call errored).
- [ ] Draft status was preserved unless the user asked to mark it ready.
