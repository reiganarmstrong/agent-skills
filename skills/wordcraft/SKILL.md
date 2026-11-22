---
name: wordcraft
description: >-
  Interact with WordCraft documents using wordcraft-cli and its stdio MCP
  server (live app bridge or headless mode). Use when the user asks to read,
  inspect, write, format, render, convert, or edit a document in WordCraft or
  talk to an open WordCraft file.
---

# WordCraft CLI & MCP

Use `wordcraft-cli` to control a live running WordCraft window or process documents headlessly via the WordCraft MCP server over stdio.

## Connection Modes

### 1. Live App Mode (open WordCraft document)
Connects to a running WordCraft desktop app listening on its control port (default `127.0.0.1:7981`):

```bash
wordcraft-cli mcp --connect 127.0.0.1:7981
```

If WordCraft is not listening on port `7981`, launch it with:
```bash
/Applications/WordCraft.app/Contents/MacOS/WordCraft --control 7981 &
```

### 2. Headless Mode (no GUI window)
For background file operations without attaching to the desktop app:

```bash
wordcraft-cli mcp --automation-read-root <DIR> --automation-write-root <DIR>
```

Or use direct CLI subcommands for quick one-off tasks:
- `wordcraft-cli info <file>` — pages, words, paragraphs, properties (JSON)
- `wordcraft-cli text <file>` — plain text
- `wordcraft-cli inspect <file>` — document structure (JSON)
- `wordcraft-cli convert <in> <out>` — convert between docx, pdf, odt, rtf, html, md, tex, txt, json, png, xml
- `wordcraft-cli render <file> <out.png> [--page N]` — render a page to PNG
- `wordcraft-cli commands [--json]` — list all available command IDs

## Calling WordCraft MCP Tools

Use the bundled helper [mcp_call.py](./scripts/mcp_call.py) to run one or more MCP tool calls in a single session (JSON array on stdin, or a single tool + JSON args):

```bash
# Single tool call against the live app
python3 ~/.agents/skills/wordcraft/scripts/mcp_call.py list_documents

# Tool call with JSON arguments
python3 ~/.agents/skills/wordcraft/scripts/mcp_call.py type_text '{"text": "Hello"}'

# Multiple sequential calls in one MCP session (stdin JSON array)
python3 ~/.agents/skills/wordcraft/scripts/mcp_call.py --batch <<'EOF'
[
  {"tool": "execute", "args": {"command": "para.style", "params": {"style": "Heading 1"}}},
  {"tool": "type_text", "args": {"text": "Title"}},
  {"tool": "execute", "args": {"command": "text.newParagraph"}},
  {"tool": "execute", "args": {"command": "para.style", "params": {"style": "Normal"}}},
  {"tool": "type_text", "args": {"text": "Body text."}},
  {"tool": "inspect_document", "args": {}}
]
EOF
```

Pass `--headless` (instead of the default `--connect 127.0.0.1:7981`) or `--connect HOST:PORT` before the tool name when needed.

## Common MCP Tools

- **Documents:** `list_documents`, `new_document`, `open_document`, `save_document`
- **Reading & Inspection:** `inspect_document`, `get_text`, `render_page`, `ui_inspect`, `screenshot`
- **Editing:** `type_text`, `select_text`, `insert_table`, `execute`, `batch`
- **Discovery:** `list_commands` (pass `{"query": "..."}` to find command IDs and parameters)

## Workflow Guidelines

1. **Inspect first:** Call `list_documents` and `inspect_document` before editing an open file so you know its current content and active document ID.
2. **Batch edits:** Group related commands into a single `--batch` call (or use WordCraft's `batch` tool) to minimize round-trips.
3. **Verify:** Call `inspect_document` (or `render_page` for layout-sensitive changes) after editing to confirm the result.
4. **Save cautiously:** When editing an open file in the live app, do not overwrite the file on disk with `save_document` unless the user asks to save—leaving changes unsaved in the live window lets the user review or undo easily.
