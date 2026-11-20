---
name: run-tickets
description: Run the ready tickets derived from a local spec or GitHub parent issue, one fresh implementation agent at a time, until no eligible tickets remain.
---

# Run tickets

Invoke with a local spec path or a GitHub parent issue number/URL after `to-tickets` has published its tickets. This skill orchestrates existing tickets; it does not create tickets or change the parent. One invocation keeps working until a fresh scan finds no eligible ticket.

## Prepare

1. Read the repo's agent instructions, `docs/agents/issue-tracker.md`, and its triage label mapping if present. Confirm that the input and tracker match. Read the installed `implement` skill, normally `../implement/SKILL.md`. If tracker setup or `implement` is missing, report what is missing and stop.
2. Check the current branch and worktree. For a local tracker, commit uncommitted input spec and ticket files as a separate setup commit after reviewing exactly which files will enter it. Preserve unrelated changes; if they could enter a ticket commit or make the branch unsafe to use, stop and report them. Keep all ticket work on the current branch. Do not create or merge a PR.
3. Require a way to launch a fresh subagent and wait for it. Run only one implementation agent at a time. If fresh agents are unavailable, explain that the requested execution model is unavailable and stop.

## Discover the queue

Rebuild the queue from the tracker before each selection, including after a failed ticket. Do not freeze the initial set.

- **Local Markdown:** The input is `.scratch/<feature>/spec.md`; inspect only its adjacent `issues/` directory. Read every ticket's `Status` and `Blocked by` fields. `resolved` means complete; `ready-for-agent` is eligible for consideration; `blocked` stays open for human attention.
- **GitHub:** The input is the parent issue. Find all issues linked as its native sub-issues or carrying an explicit `## Parent` reference to it. Search beyond CLI default page limits and include closed issues when building the complete set. Verify the parent of each candidate; flag conflicting native and textual parents instead of acting on that ticket. The parent's own state and labels do not decide child completion. A closed child is complete; only an open child with the configured `ready-for-agent` label is eligible for consideration.

For each open candidate, read native dependency edges where available and the ticket's `Blocked by` text. Treat both as blockers. Check each referenced blocker's actual state, including blockers outside the candidate set. An unresolved or unidentifiable blocker keeps the ticket out of the frontier. Report cycles and conflicting references. Do not infer completion from a checked box, an agent's message, or an assignee.

On GitHub, skip tickets assigned to someone else. Select the lowest local ticket number or oldest GitHub issue number among open, ready, unblocked tickets. Recheck its state and blockers immediately before work. Assign the GitHub ticket to `@me` and verify the claim before dispatch.

## Implement one ticket

Launch a fresh agent with the selected ticket, its source spec or parent, the repo path, and the starting commit. Instruct it to read and follow `implement` for **this ticket only**: implement, verify, review, make one implementation commit on the current branch, then close or resolve the ticket using the tracker's convention. Give the agent the ticket's full body and comments, or tell it to fetch them. Require a concise return of changed behavior, test commands/results, review result, implementation commit ID, tracker update, and any blocker. Wait for it to finish before starting another.

Independently inspect the resulting branch and tracker state. A ticket counts as complete only when its acceptance criteria are demonstrated, the `implement` checks and review are accounted for, the implementation commit exists, and the tracker shows closure. For local tickets, confirm all criteria are checked, `Status: resolved`, and a separate ticket update commit records the implementation commit ID and verification under `## Comments`. For GitHub, confirm the issue is closed with a completion comment per the tracker convention. If evidence is missing, treat the ticket as unfinished and reopen or restore its tracker state if the worker closed it early.

## Handle failure and continue

Allow ordinary fixes within the implementation attempt. Retry the orchestration once only for a clear transient tool failure. Do not repeat failing code or test attempts indefinitely.

For an unfinished ticket, leave it open and add a concise blocker note to its GitHub comments or local `## Comments`. For GitHub, remove `ready-for-agent`; use the configured `needs-info` label when an answer is needed, or `ready-for-human` when human implementation is needed. For local Markdown, set `Status: blocked` and commit the ticket update separately. Preserve any partial work and identify its location. Continue to independent tickets only after the current branch is safe and the worktree is clean enough for the next ticket; otherwise stop and report the state without discarding work.

Rescan after every completion or safe failure. Stop when no eligible ticket remains. Report completed ticket IDs and commits, blocked tickets and reasons, tickets assigned elsewhere, unresolved dependencies, and any remaining open tickets. Leave the source spec or parent issue unchanged.
