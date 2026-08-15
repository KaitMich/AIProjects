🧪 Step 1: Create intents.json
This file defines what kinds of things users might say, how to group those into "intents," and how the bot should respond.

📝 Code (Save as intents.json)
json

{
  "intents": [
    {
      "tag": "greeting",
      "patterns": ["Hi", "Hello", "Good morning", "Hey there"],
      "responses": ["Hello! How can I assist you with your car rental today?"]
    },
    {
      "tag": "rental_info",
      "patterns": ["How much is a rental?", "What are your prices?", "Rental cost"],
      "responses": ["Our rentals start at $29.99/day. What type of vehicle are you interested in?"]
    },
    {
      "tag": "return_policy",
      "patterns": ["What's your return policy?", "How do I return a car?", "Return process"],
      "responses": ["You can return your rental to any location. Just leave the keys in the dropbox."]
    },
    {
      "tag": "goodbye",
      "patterns": ["Bye", "See you", "Thanks, goodbye"],
      "responses": ["Thanks for choosing Handy Car Rentals! Have a safe trip."]
    }
  ]
}
💬 What this does:
"tag" - A label for each type of user question. This is what your model will predict.

"patterns" - Examples of what the user might say. These are the training examples.

"responses" - What the bot can say in return if that tag is detected. The bot will choose one at random.

---

🧠 Step 2A: Basic Preprocessing in Python
📝 Code (Save this as preprocess.py)
python

import json                  # for loading the JSON data
from sklearn.feature_extraction.text import CountVectorizer  # to convert text into numbers
from sklearn.preprocessing import LabelEncoder                # to convert string labels into integers

# Load the intents.json file
with open("intents.json") as file:
    data = json.load(file)  # Load JSON data into a Python dictionary

# Prepare lists to store training data
patterns = []  # sentences the user might say
tags = []      # labels for those sentences

# Loop through each intent
for intent in data["intents"]:
    for pattern in intent["patterns"]:
        patterns.append(pattern)       # add user phrase
        tags.append(intent["tag"])     # add the intent tag it maps to

# Vectorize the text (convert words into numbers)
vectorizer = CountVectorizer()
X = vectorizer.fit_transform(patterns).toarray()  # X will be a matrix of token counts

# Encode the labels (convert text labels into integers)
label_encoder = LabelEncoder()
y = label_encoder.fit_transform(tags)  # y will be an array of encoded intent tags

# Print results to confirm
print("Sample input (X):", X[0])
print("Sample label (y):", y[0])
print("Label classes:", label_encoder.classes_)
🔍 Line-by-Line Explanation:
json – We use this to read and parse your intents.json file.

CountVectorizer – This turns your sentences into a matrix where each column represents a word and each row a sentence.

LabelEncoder – Converts the intent tags (like "greeting" or "rental_info") into numbers the model can understand.

✅ What you’ll get when you run it:
bash

python preprocess.py
You’ll see:

A sample vector of one of the user inputs (e.g., [0 1 0 2 0 ...])

The encoded tag for that input (e.g., 1)

A list of all label classes (e.g., ['goodbye', 'greeting', 'rental_info', 'return_policy'])

🧭 Step 2B: Run the Preprocessing Script from PowerShell
✅ Navigate to your script location:
powershell

cd "C:\Users\<your_username>\Documents\Handy"
(Replace <your_username> with your actual Windows login name)

Tip: You can type just cd then drag-and-drop the folder into PowerShell and hit enter - it’ll autofill the path.

✅ Run the script:
powershell

py preprocess.py
If everything works, you’ll see some output like:

less

Sample input (X): [0 1 0 2 0 ...]
Sample label (y): 1
Label classes: ['goodbye' 'greeting' 'rental_info' 'return_policy']

---

🧠 Step 3: Build & Train the Model
📝 Code (Add to a new file: train_model.py)
python

import pickle                                  # for saving model components
import numpy as np                             # for array manipulation
import tensorflow as tf                        # for the neural network
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Load training data
X = pickle.load(open("vectorizer_X.pkl", "rb"))  # input matrix
y = pickle.load(open("labels_y.pkl", "rb"))      # target labels

# Define the neural network model
model = Sequential()
model.add(Dense(128, input_shape=(X.shape[1],), activation='relu'))  # first layer: 128 nodes
model.add(Dropout(0.5))                                               # drop 50% to prevent overfitting
model.add(Dense(64, activation='relu'))                               # second layer: 64 nodes
model.add(Dropout(0.5))                                               # another dropout
model.add(Dense(len(set(y)), activation='softmax'))                   # output layer: one node per intent

# Compile the model
model.compile(loss='sparse_categorical_crossentropy',
              optimizer='adam',
              metrics=['accuracy'])

# Train the model
model.fit(X, y, epochs=200, batch_size=5, verbose=1)

# Save the trained model
model.save("chatbot_model.h5")
🔍 Before You Run It:
To make this work, let’s save your X and y objects from Step 2 as .pkl files.

Add this to the bottom of preprocess.py (or run it as a one-time script):

python

import pickle

pickle.dump(X, open("vectorizer_X.pkl", "wb"))
pickle.dump(y, open("labels_y.pkl", "wb"))

---

Step 3A: Install TensorFlow in PowerShell
In your terminal, run:

powershell

py -m pip install tensorflow
✅ This installs TensorFlow into the version of Python you're currently using with py. It might take a few minutes depending on your system.

🧠 Tip:
If you're using a virtual environment, activate it first:


.\venv\Scripts\activate
Then run:

powershell

py -m pip install tensorflow


Then run:

powershell

py preprocess.py
🏁 Now Run Training:
In PowerShell:

powershell

cd "C:\Users\<your_username>\Documents\Handy"
py train_model.py
Let it train for a few minutes - you’ll see accuracy stats printing out every epoch.

*** Must have Python 3.10 (or 3.11) (not yet supported for 3.13 as of May 1st).
https://www.python.org/downloads/release/python-31011/

It may say 🧠 HDF5 (.h5) is now considered a “legacy” format.
Keras recommends saving models in the newer .keras format instead.

.h5 file still works perfectly fine, especially for simple projects like this one. 

✅ If You Want to Future-Proof:
You can change this line:

python

model.save("chatbot_model.h5")
To:

python

model.save("chatbot_model.keras")
Both formats do the same thing in your case. It just changes how it's stored internally. The .keras format will eventually be the default in newer versions of TensorFlow.

---

🧪 Step 4: Build the CLI Chatbot

✅ Install scikit-learn (for Python 3.10)
In PowerShell, run:

powershell

py -3.10 -m pip install scikit-learn

✅ Fix: Save vectorizer.pkl and label_encoder.pkl after preprocessing
Open your preprocess.py and add these two lines at the bottom:

python

pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))         # Save the text vectorizer
pickle.dump(label_encoder, open("label_encoder.pkl", "wb"))   # Save the label encoder
Your full preprocess.py should now end like this:

python
Copy
Edit
pickle.dump(X, open("vectorizer_X.pkl", "wb"))
pickle.dump(y, open("labels_y.pkl", "wb"))
pickle.dump(vectorizer, open("vectorizer.pkl", "wb"))
pickle.dump(label_encoder, open("label_encoder.pkl", "wb"))


📄 Save as chatbot.py in your Handy folder
python

import json
import random
import pickle
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained model (h5 or keras)
model = load_model("chatbot_model.h5")  # or "chatbot_model.keras" if you changed formats

# Load the vectorizer and label encoder
vectorizer = pickle.load(open("vectorizer.pkl", "rb"))
label_encoder = pickle.load(open("label_encoder.pkl", "rb"))

# Load intents data
with open("intents.json") as file:
    intents = json.load(file)

# Function to get a response from the model
def chatbot_response(user_input):
    input_data = vectorizer.transform([user_input]).toarray()  # Vectorize input
    prediction = model.predict(input_data)                      # Predict intent
    tag = label_encoder.inverse_transform([np.argmax(prediction)])[0]  # Decode label

    # Find matching intent and return a random response
    for intent in intents["intents"]:
        if intent["tag"] == tag:
            return random.choice(intent["responses"])
    return "I'm not sure how to help with that."

# Run the chatbot loop
print("🤖 Handy Car Rental AI is online! (type 'quit' to exit)")
while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        print("🤖 Goodbye!")
        break
    response = chatbot_response(user_input)
    print(f"Bot: {response}")
▶️ Run it:
powershell
Copy
Edit
py -3.10 chatbot.py
Then test it with:

hi

how much is a rental

what's your return policy

bye

---

🤖 Handy Car Rental AI is online! (type 'quit' to exit)
You: hi
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 60ms/step
Bot: Hello! How can I assist you with your car rental today?
You: whats your return policy
1/1 ━━━━━━━━━━━━━━━━━━━━ 0s 26ms/step
Bot: You can return your rental to any location. Just leave the keys in the dropbox.
You: quit
🤖 Goodbye!
PS C:\Users\[users]\documents\Handy>

---

Handy AI – Feature Expansion Ideas
1. User Experience & Clarity
 Add fallback replies for unrecognized questions (“Sorry, could you rephrase that?”)

 Confidence score threshold to trigger fallback (e.g., if model isn’t 70%+ sure)

 Allow follow-up questions (simple memory of last intent)

 Typing simulation for more natural responses

2. Functional Enhancements
 Add more intents (e.g., insurance info, late returns, vehicle availability)

 Multi-intent recognition: respond when two questions are asked at once

 Integrate a mock calendar for pickup/dropoff suggestions

 Allow user name recognition and personalization (“Welcome back, Kaitlyn!”)

3. Management Features
 Log all questions to a CSV for training improvement

 “Hot phrases” dashboard: which questions are asked most often

 Admin mode to add new intents via the chat itself

4. Tone & Brand Control
 Switchable tone: “friendly”, “funny”, “serious”, “robotic”

 Custom emoji/sticker responses

 Add sentiment recognition to adjust tone dynamically

5. Long-Term Stretch Goals
 Small embedded memory file (remembers key user preferences or last session)

 Web interface using Flask (for browsers, internal use, or demos)

 Mobile-friendly command line version or chatbot APK

 GPT fallback with a restricted domain prompt: “Only talk about car rentals!”

