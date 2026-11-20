# Personal agent skills

Shared skills live in `/home/reagan/.agents/skills`. Codex reads that directory directly. Antigravity CLI (and App) reads it via `/home/reagan/.gemini/config/skills.json`. Claude Code gets an individual symlink for each shared skill in `/home/reagan/.claude/skills`.

| Location | Purpose |
| --- | --- |
| `~/.agents/skills/<name>/` | Shared skills for Codex, Claude Code, and Antigravity |
| `~/.codex/skills/<name>/` | Codex-only skills |
| `~/.claude/skills/<name>/` | Claude-only skills; shared skills appear here as links |
| `~/.gemini/config/skills/<name>/` | Antigravity-only skills (shared skills are loaded via `~/.gemini/config/skills.json`) |

This layout controls skill discovery. Both agents run as the same user and can still read other files on disk.

## Add a skill

To share a skill, put its whole folder at `~/.agents/skills/<name>/`, including `SKILL.md` and any supporting files. Run:

```sh
~/.local/bin/sync-agent-skills
```

Edit shared skills at their source in `~/.agents/skills`. Both agents will read the same files. Run the sync command again after adding or renaming a shared skill. It reports stale links and name conflicts without removing or replacing existing entries.

For a skill that only one agent should discover, put the whole folder directly in that agent's local skills directory. Keep shared and local skill names distinct.

Check the shared links without making changes:

```sh
~/.local/bin/sync-agent-skills --check
```

New agents need their own discovery path connected to the shared directory. The sync command currently connects Claude Code; Codex already reads the shared directory directly, and Antigravity loads it through `~/.gemini/config/skills.json`.

Restart a T3 agent session if its skill list has not refreshed after a change. Existing conversations can retain previously loaded skill instructions.

Codex's `.system` skills, plugin-managed skills, and Claude's `synced` skills remain managed by their original tools.

## Discovery documentation

- [Codex skill locations and symlink support](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills)
- [Claude Code skill locations and symlink support](https://code.claude.com/docs/en/skills#choose-where-skills-load)

The current Codex installation also loads `~/.codex/skills`, as confirmed by this session's skill catalog. The current public documentation lists `~/.agents/skills` as the user discovery location.
