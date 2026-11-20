---
name: implement
description: "Implement a piece of work based on a spec or set of tickets."
disable-model-invocation: true
---

Implement the work described by the user in the spec or tickets.

Use /tdd where possible, at pre-agreed seams.

Run typechecking regularly, single test files regularly, and the full test suite once at the end.

Once done, use /code-review to review the work.

Commit your work to the current branch.

After the implementation and any review fixes are committed, close each supplied
ticket in its tracker. Follow the tracker's documented closure convention. For a
local Markdown ticket when no convention exists:

- Check only acceptance criteria demonstrated by tests or review.
- Resolve the ticket only when every acceptance criterion is checked.
- Set `Status:` to `resolved` and append the implementation commit IDs plus a
  concise verification note under `## Comments`.
- Commit the ticket update separately so its comment can reference the exact
  implementation commits.
