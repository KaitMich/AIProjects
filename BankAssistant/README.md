# Bank Assistant

A local, LLM-powered IT support chat for a simulated bank helpdesk. It answers
support questions the way a calm, experienced coworker would ("why is my
phone unregistered?", "who handles port security violations?"), grounded in a
small simulated knowledge base of departments, contacts, and common issues so
it doesn't invent extension numbers or policies.

No real systems, accounts, or data are involved anywhere in this project.

## Why I built this

I worked IT support at a bank, and the actual day-to-day chaos of that job —
murky escalation paths, documentation that exists "somewhere," support staff
who are always underwater — is what this models. I wanted to see whether a
small local LLM, given a short persona prompt and a grounding knowledge base
instead of a big fine-tune or a hand-written decision tree, could hold that
tone and route questions correctly.

It also turned into a lesson in prompt design over hand-rolled logic: my
first sketch of this (see `Handy Car Rental AI` in this same repo) was a
tiny neural net trained to classify user input into a fixed list of
intents. That works, but every new question type means new training data
and a retrain. Here, the "knowledge" lives in `knowledge_base.json` as
plain data — adding a new department or issue means editing a file, not
retraining a model. That trade-off (retrain vs. re-prompt) was the main
thing I wanted to feel out hands-on.

## How it works

```
knowledge_base.json  →  flattened into the system prompt
                              ↓
User message  →  Ollama (llama3:8b, running locally)  →  Response
                              ↓
                    Conversation history kept in memory
                    for the length of the session
```

- The whole "environment" (departments, contacts, common issues) lives in
  [`knowledge_base.json`](knowledge_base.json) and gets folded into the
  system prompt at startup, so the model answers from that data rather than
  guessing.
- The system prompt sets the persona (calm coworker, not a corporate
  chatbot) and the ground rules (keep it short, acknowledge frustration
  briefly, don't invent details that aren't in the knowledge base, "open a
  ticket" for anything needing real escalation — simulated, nothing is
  actually contacted).
- Everything runs locally through [Ollama](https://ollama.com) — no data
  leaves the machine, no API key, no cost per message.

## Install

1. Install [Ollama](https://ollama.com/download) and make sure it's running.
2. Pull the model this project uses:
   ```bash
   ollama pull llama3:8b
   ```
3. Install the one Python dependency:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```bash
python bank_assistant.py
```

```
Bank Assistant is online. Type 'quit' to exit.

You: I can't log into the teller system after the update
Bank Assistant: No worries, we've seen this before. The recent update likely
changed the authentication method or reset cached credentials. I can walk
you through the new login, send you the password reset link, or open a
ticket with Branch Systems Support (typical response: 15-20 min). Which
works best?

You: who handles port security violations?
Bank Assistant: That's Network Security. Your contact is the IT Security
Liaison at ext. 4775, and for anything urgent the Security Operations
Center is staffed 24/7 at ext. 8000. Want me to log this one?
```

## Customizing

Everything domain-specific lives in `knowledge_base.json` — add a
department, an issue pattern, or change contact info there and it's picked
up automatically, no code changes needed. The persona and ground rules live
in the `SYSTEM_PROMPT` string at the top of `bank_assistant.py`.

## Limitations

- Answers are only as good as `knowledge_base.json` — it's a small seed set,
  not a real IT knowledge base.
- No real ticketing, authentication, or account systems are touched. Every
  "ticket" is simulated.
- Response quality depends on the local model; `llama3:8b` was chosen as a
  reasonable balance of quality and speed on consumer hardware, not because
  it's the best model available.
