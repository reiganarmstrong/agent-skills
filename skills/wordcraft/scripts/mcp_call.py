#!/usr/bin/env python3
"""Minimal stdio JSON-RPC client for `wordcraft-cli mcp`."""

import argparse
import json
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser(description="Call WordCraft MCP tools over stdio.")
    parser.add_argument(
        "--connect",
        default="127.0.0.1:7981",
        help="WordCraft control host:port (default: 127.0.0.1:7981)",
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run wordcraft-cli mcp in headless mode instead of --connect",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Read a JSON array of {\"tool\": ..., \"args\": ...} objects from stdin",
    )
    parser.add_argument("tool", nargs="?", help="MCP tool name (when not using --batch)")
    parser.add_argument("args_json", nargs="?", default="{}", help="JSON object of tool arguments")
    ns = parser.parse_args()

    if ns.batch:
        calls = json.load(sys.stdin)
    else:
        if not ns.tool:
            parser.error("Provide a tool name or --batch")
        calls = [{"tool": ns.tool, "args": json.loads(ns.args_json)}]

    cmd = ["wordcraft-cli", "mcp"]
    if not ns.headless:
        cmd.extend(["--connect", ns.connect])

    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    assert proc.stdin and proc.stdout and proc.stderr

    req_id = 0

    def send(obj: dict) -> None:
        proc.stdin.write(json.dumps(obj) + "\n")
        proc.stdin.flush()

    def rpc(method: str, params: dict | None = None) -> dict:
        nonlocal req_id
        req_id += 1
        payload: dict = {"jsonrpc": "2.0", "id": req_id, "method": method}
        if params is not None:
            payload["params"] = params
        send(payload)
        line = proc.stdout.readline()
        if not line:
            err = proc.stderr.read()
            raise RuntimeError(f"wordcraft-cli mcp closed unexpectedly. stderr:\n{err}")
        return json.loads(line)

    try:
        rpc(
            "initialize",
            {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "wordcraft-skill", "version": "1.0"},
            },
        )
        send({"jsonrpc": "2.0", "method": "notifications/initialized"})

        results = []
        for item in calls:
            res = rpc(
                "tools/call",
                {"name": item["tool"], "arguments": item.get("args", {})},
            )
            results.append(res)

        out = results[0] if len(results) == 1 and not ns.batch else results
        print(json.dumps(out, indent=2))
        return 0
    finally:
        proc.stdin.close()
        proc.wait(timeout=5)


if __name__ == "__main__":
    raise SystemExit(main())
