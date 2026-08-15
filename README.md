# AI Projects

A small set of focused AI projects practical builds, not experiments or notes.
Each targets a specific real-world use case and a specific skill: conversational
design grounded in an actual job, intent classification, and input sanitization
for privacy/security.

## [Bank Assistant](./BankAssistant)

A local, LLM-powered IT support chat for a simulated bank helpdesk, modeled
directly on real IT support experience at a bank. Grounded in a small
knowledge base of departments and common issues so it answers from that data
rather than the chaos of unclear escalation paths and scattered
documentation that inspired it in the first place.

## [Handy Car Rental AI](./HandyCarRental)

An intent-classification chatbot for a car rental scenario: a small neural
net trained from scratch to classify user input into one of a few intents
(bag-of-words → feedforward net → templated response), no LLM required. The
first hands-on build in this repo, and the one that motivated Bank
Assistant's different approach.

## [PrivacyFilter](./PrivacyFilter)

Rewrites a user's input with synonym substitution before it reaches an LLM, so
the model never sees or stores verbatim user data - reduces both data
retention risk and prompt-injection surface. Includes an Ollama plugin.
See that folder's own README for details.
