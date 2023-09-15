import pyttsx3
import time
import openai

import random
import json
import torch
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize
from gtts import gTTS
#import pygame
import os
import tempfile

# Initialize pygame mixer
#pygame.mixer.init()

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open('intents.json', 'r') as json_data:
    intents = json.load(json_data)

FILE = "data.pth"
data = torch.load(FILE)

input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "HelpR"

# Create a TTS engine
engine = pyttsx3.init()
engine_started = False  # Add this variable to track engine state

# Set the default speech rate and volume
default_rate = 150
default_volume = 0.6
engine.setProperty("rate", default_rate)
engine.setProperty("volume", default_volume)

def speak(text, rate=None, volume=None):
    # Set custom speech rate and volume if provided
    if rate is not None:
        engine.setProperty("rate", rate)
    if volume is not None:
        engine.setProperty("volume", volume)


    global engine_started  # Use the global variable

    # Start the engine's loop if it's not already running
    if not engine_started:
        engine.startLoop(False)
        engine_started = True

    # Speak the provided text
    engine.say(text)
    engine.iterate()  # Use iterate instead of runAndWait()

def get_response(msg):
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)

    output = model(X)
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]

    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    
    if prob.item() > 0.75:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                response = random.choice(intent['responses'])
                #speak(response)  # Speak the response
                return response

    response = "Sorry! I'm still in training...didn't quite catch that.\n    Could you rephrase?"
    speak(response)  # Speak the default response
    return response

