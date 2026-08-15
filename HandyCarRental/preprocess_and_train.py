"""
Loads intents.json, vectorizes the training phrases, trains a small
feedforward classifier to map a phrase to an intent tag, and saves
everything the chatbot needs to run: chatbot_model.keras, vectorizer.pkl,
label_encoder.pkl.

Run this whenever you add or change intents in intents.json.
"""

import json
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

with open("intents.json", encoding="utf-8") as f:
    data = json.load(f)

# Flatten intents.json into parallel lists: one training phrase per row,
# paired with the intent tag it belongs to.
patterns, tags = [], []
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)
        tags.append(intent["tag"])

# Bag-of-words: each phrase becomes a vector of word counts.
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns).toarray()

# Intent tags ("greeting", "rental_info", ...) become integers 0..n-1.
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(tags)

print(f"Training phrases: {len(patterns)}")
print(f"Intent classes:   {list(label_encoder.classes_)}")
print(f"Input vector size: {X.shape[1]} (vocabulary size)")

model = Sequential([
    Dense(128, input_shape=(X.shape[1],), activation="relu"),
    Dropout(0.5),
    Dense(64, activation="relu"),
    Dropout(0.5),
    Dense(len(label_encoder.classes_), activation="softmax"),
])
model.compile(loss="sparse_categorical_crossentropy", optimizer="adam", metrics=["accuracy"])
model.fit(X, y, epochs=200, batch_size=5, verbose=0)

loss, acc = model.evaluate(X, y, verbose=0)
print(f"Final training accuracy: {acc:.2%}")

model.save("chatbot_model.keras")
with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)
with open("label_encoder.pkl", "wb") as f:
    pickle.dump(label_encoder, f)

print("\nSaved: chatbot_model.keras, vectorizer.pkl, label_encoder.pkl")
