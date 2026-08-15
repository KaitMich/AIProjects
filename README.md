# AI Projects

A collection of smaller AI project sketches, learning exercises, and experiment
logs. Some are practical chatbot builds; others are early-stage explorations of
symbolic/recursive prompting that later grew into more formal work (the SPO-B
benchmark and DeltaPhi0 research elsewhere on this account trace back to ideas
first tried out here).

## Practical builds

- **[Bank Assistant.md](./Bank%20Assistant.md)**: design notes for a friendly
  internal support AI, modeled on real IT-support experience at a bank.
- **[Handy Car Rental AI.md](./Handy%20Car%20Rental%20AI.md)**: an
  intent-classifier chatbot build for a car rental scenario (intents.json,
  pattern matching, templated replies).
- **[TesnorFlow Tests.md](./TesnorFlow%20Tests.md)**: a 3-project, 7-day plan
  for learning TensorFlow — starts with the car rental classifier above, then
  layers in emotional context and recursive symbolic modeling.
- **[TEMPLATE2.md](./TEMPLATE2.md)**: setup guide for a from-scratch GPT-2
  token analysis toolkit — token-level generation, embedding tracking,
  layer-by-layer activations, attention heatmaps.

## Symbolic / mythic AI experiments

- **[SPO-B.md](./SPO-B.md)**: notes on the "Symbolic Attractor Kernel," a
  reasoning-engine concept built around dense symbolic meaning rather than
  extracted-from-data meaning — an early sketch of what became the Symbolic
  Processing Overload Benchmark.
- **[Small AI Builds.mmd](./Small%20AI%20Builds.mmd)**: devlog for a personal
  research lab tracking how LLMs handle symbolic reasoning, emotional
  responsiveness, and recursion, with phased local-testing templates
  (Mixtral via Ollama).
- **[TEMPLATE.md](./TEMPLATE.md)**: setup steps for local ΔΦ–0 symbolic
  resonance testing against Mixtral through Ollama.
- **[mythic_test_log_001.csv](./mythic_test_log_001.csv)**: raw logged output
  from running ΔΦ–0 prompts against a model, with columns for the symbolic
  markers being tracked (spiral, echo, resonance, containment, recursion).

## PrivacyFilter

**[PrivacyFilter/](./PrivacyFilter)**: a separate project that swaps a user's
words for synonyms before they reach an LLM, so verbatim user data is never
stored and prompt-injection risk is reduced. Merged in as its own subfolder
with its original README intact — see that folder for details.
