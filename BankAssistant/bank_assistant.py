"""
Bank Assistant - a local, LLM-powered IT support chat for a simulated bank
environment. See README.md for what this is and why it exists.

Requires Ollama running locally with a model pulled (default: llama3:8b).
"""

import json
import os
import random
import sys
from pathlib import Path

import ollama

MODEL = "llama3:8b"
KB_PATH = Path(__file__).parent / "knowledge_base.json"

# If OLLAMA_HOST is set to a bind-all address (0.0.0.0), that's valid for the
# server to listen on but not a connectable client target -- fall back to
# localhost so this doesn't fail on machines configured that way. Also make
# sure a port is always present (OLLAMA_HOST is sometimes just a bare host).
_host = os.environ.get("OLLAMA_HOST", "127.0.0.1:11434")
_host = _host.replace("0.0.0.0", "127.0.0.1")
if ":" not in _host.split("//")[-1]:
    _host = f"{_host}:11434"
if not _host.startswith("http"):
    _host = f"http://{_host}"
client = ollama.Client(host=_host)


def load_knowledge_base() -> str:
    """Flatten knowledge_base.json into plain text for the system prompt."""
    kb = json.loads(KB_PATH.read_text(encoding="utf-8"))

    lines = ["## Departments"]
    for dept in kb["departments"]:
        lines.append(
            f"- {dept['name']}: handles {', '.join(dept['handles'])}. "
            f"Contact: {dept['contact']}. Escalation: {dept['escalation']}."
        )

    lines.append("\n## Common issues")
    for issue in kb["common_issues"]:
        lines.append(
            f"- \"{issue['issue']}\" -- likely cause: {issue['likely_cause']} "
            f"Options to offer: {'; '.join(issue['options'])}."
        )

    return "\n".join(lines)


SYSTEM_PROMPT = f"""You are Bank Assistant, a calm, friendly internal IT support
coworker at a bank. You are NOT a generic customer service bot -- you talk like
a competent coworker who has seen this exact chaos before and isn't rattled by it.

Ground rules:
- Keep responses short (2-5 sentences, or a short numbered list of options).
- If someone sounds frustrated or stressed, briefly acknowledge that before
  jumping to the fix. Don't overdo it -- one sentence, then help.
- When you don't know something specific, say so plainly rather than
  inventing details (extensions, policies, procedures) that aren't below.
- When a real fix requires IT to get involved, offer to "open a ticket" and
  give a realistic estimated response time. This is a simulation -- no real
  ticketing system is contacted.
- This is a simulated environment: no real systems, accounts, or data exist
  behind any of this. Never claim to access, change, or view real records.

Here is the (simulated) environment map you can reference:

{load_knowledge_base()}
"""


def open_mock_ticket() -> str:
    return f"TCK-{random.randint(10000, 99999)}"


def main() -> None:
    print("Bank Assistant is online. Type 'quit' to exit.\n")
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBank Assistant: Take care!")
            break

        if not user_input:
            continue
        if user_input.lower() in {"quit", "exit"}:
            print("Bank Assistant: Take care!")
            break

        messages.append({"role": "user", "content": user_input})

        try:
            response = client.chat(model=MODEL, messages=messages)
        except Exception as e:
            print(f"\n[Could not reach Ollama -- is it running? ({e})]\n")
            print(f"Start it with: ollama serve   (and: ollama pull {MODEL})")
            sys.exit(1)

        reply = response["message"]["content"]
        messages.append({"role": "assistant", "content": reply})
        print(f"\nBank Assistant: {reply}\n")


if __name__ == "__main__":
    main()
