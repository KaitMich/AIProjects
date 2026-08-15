# AI Projects

A small set of focused AI projects practical builds, not experiments or notes.
Each targets a specific real-world use case and a specific skill: conversational
design grounded in an actual job, intent classification, and input sanitization
for privacy/security.

## [Bank Assistant](./Bank%20Assistant.md)

Design notes for a support-flow AI assistant, modeled directly on real IT
support experience at a bank. Focused on how the assistant should handle the
actual chaos of that environment unclear escalation paths, scattered
documentation, under-resourced support staff rather than a generic FAQ bot.

## [Handy Car Rental AI](./Handy%20Car%20Rental%20AI.md)

An intent-classification chatbot for a car rental scenario: pattern-based
intent detection (`intents.json`), templated responses, no LLM required. A
straightforward, deployable example of rule-based conversational AI.

## [PrivacyFilter](./PrivacyFilter)

Rewrites a user's input with synonym substitution before it reaches an LLM, so
the model never sees or stores verbatim user data - reduces both data
retention risk and prompt-injection surface. Includes an Ollama plugin.
See that folder's own README for details.
