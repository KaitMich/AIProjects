"""
CLI chatbot: loads the trained intent classifier and responds to user input
by predicting an intent tag and picking a matching response from intents.json.

Run preprocess_and_train.py first if chatbot_model.keras doesn't exist yet.
"""

import json
import pickle
import random
import sys

import numpy as np
from tensorflow.keras.models import load_model

# Confidence below this falls back to a "didn't catch that" response instead
# of forcing a match into whichever intent scored highest.
CONFIDENCE_THRESHOLD = 0.6
FALLBACK_RESPONSE = "Sorry, I didn't quite catch that -- could you rephrase it?"

try:
    model = load_model("chatbot_model.keras")
    with open("vectorizer.pkl", "rb") as f:
        vectorizer = pickle.load(f)
    with open("label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    with open("intents.json", encoding="utf-8") as f:
        intents = json.load(f)
except FileNotFoundError as e:
    print(f"Missing file: {e.filename}")
    print("Run 'python preprocess_and_train.py' first to train the model.")
    sys.exit(1)


def chatbot_response(user_input: str) -> str:
    vector = vectorizer.transform([user_input]).toarray()
    prediction = model.predict(vector, verbose=0)[0]

    best_index = int(np.argmax(prediction))
    confidence = float(prediction[best_index])

    if confidence < CONFIDENCE_THRESHOLD:
        return FALLBACK_RESPONSE

    tag = label_encoder.inverse_transform([best_index])[0]
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])

    return FALLBACK_RESPONSE


def main() -> None:
    print("Handy Car Rental AI is online! (type 'quit' to exit)")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Goodbye!")
            break

        if not user_input:
            continue
        if user_input.lower() == "quit":
            print("Bot: Goodbye!")
            break

        print(f"Bot: {chatbot_response(user_input)}")


if __name__ == "__main__":
    main()
