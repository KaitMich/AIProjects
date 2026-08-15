# Handy Car Rental AI

A small intent-classification chatbot for a car rental scenario. No LLM, no
API calls — a tiny neural network trained from scratch on a handful of
example phrases, classifying user input into one of a few fixed intents
(greeting, pricing, return policy, goodbye) and replying with a matching
canned response.

## Why I built this

This was my first hands-on pass at the classic supervised-learning chatbot
pattern: turn text into numbers (bag-of-words), train a small classifier on
labeled examples, predict a category, respond from a template. It's not
sophisticated — it's the "hello world" of conversational AI — but building
the whole pipeline by hand (vectorizing, encoding labels, training, saving
and reloading the model) is what actually taught me how the pieces fit
together, in a way that using a hosted chat API never would have.

The most useful lesson came from where this approach breaks: every new type
of question means new training examples and a retrain, and the model always
picks *something*, even for input that matches nothing — the original
version had no way to say "I don't know." I added a confidence threshold
here so it can now recognize when it's guessing and say so instead of
answering confidently wrong. That gap — and comparing this approach against
prompting a general-purpose LLM instead of training a classifier — is what
led directly into the `Bank Assistant` project in this same repo.

## How it works

```
intents.json  →  patterns vectorized (bag-of-words)  →  tiny neural net trained
                                                                  ↓
                                            saved: chatbot_model.keras,
                                            vectorizer.pkl, label_encoder.pkl
                                                                  ↓
User message  →  vectorized the same way  →  model predicts an intent  →  reply
                                                       ↓
                                    below-confidence predictions fall back
                                    to "didn't catch that" instead of guessing
```

- `intents.json` defines each intent as a tag, a handful of example phrases,
  and one or more possible responses.
- `preprocess_and_train.py` turns those phrases into a bag-of-words matrix
  (`CountVectorizer`), encodes the tags as integers, and trains a small
  feedforward network (128 → 64 → softmax) to map phrase-vector to tag.
- `chatbot.py` loads the trained model and, for each message, vectorizes it
  the same way, predicts a tag, and returns a random response from that
  intent — unless the model's confidence is below the threshold, in which
  case it asks the user to rephrase instead of forcing a match.

## Install

Requires **Python 3.10 or 3.11** (TensorFlow's Windows build did not support
3.13 as of this writing).

```bash
pip install -r requirements.txt
```

## Usage

A pre-trained model is included, so you can run the chatbot right away:

```bash
python chatbot.py
```

```
Handy Car Rental AI is online! (type 'quit' to exit)
You: hi
Bot: Hello! How can I assist you with your car rental today?
You: how much is a rental
Bot: Our rentals start at $29.99/day. What type of vehicle are you interested in?
You: asdkjaslkdj
Bot: Sorry, I didn't quite catch that -- could you rephrase it?
You: quit
Bot: Goodbye!
```

To retrain after editing `intents.json` (adding intents, more example
phrases, etc.):

```bash
python preprocess_and_train.py
```

## Limitations

- Only 4 intents, ~3 example phrases each — enough to demonstrate the
  pipeline, not a real product's worth of coverage.
- Adding a new intent means adding training examples and retraining, not
  just editing a prompt (see `Bank Assistant` for the alternative approach).
- No memory of previous turns — each message is classified independently.
