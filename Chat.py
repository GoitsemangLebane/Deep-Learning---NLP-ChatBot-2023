import pyttsx3
import time
import openai
import webbrowser
import requests

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
'''
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

    response = "Sorry! I'm still in training...didn't quite catch that.\n    Could you rephrase or ask something else?"
    speak(response)  # Speak the default response
    return response
'''
def get_random_advice():
    try:
        # Define the API URL
        url = "https://api.adviceslip.com/advice"
        # Send an HTTP GET request to the API
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            advice_data = response.json()
            advice = advice_data.get("slip", {}).get("advice")
            if advice:
                return advice
            else:
                return "Sorry, I couldn't fetch any advice at the moment."
        else:
            return "Sorry, I couldn't fetch any advice at the moment."
    except Exception as e:
        print("Error fetching advice:", str(e))
        return "Sorry, there was an error fetching advice."

def get_random_dad_joke():
    try:
        # Define the API URL
        url = "https://icanhazdadjoke.com/"
        # Send an HTTP GET request to the API with the "Accept" header to specify JSON response
        headers = {"Accept": "application/json"}
        response = requests.get(url, headers=headers)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response
            joke_data = response.json()
            joke = joke_data.get("joke")
            if joke:
                return joke
            else:
                return "Sorry, I couldn't fetch a dad joke at the moment."
        else:
            return "Sorry, I couldn't fetch a dad joke at the moment."
    except Exception as e:
        print("Error fetching dad joke:", str(e))
        return "Sorry, there was an error fetching a dad joke."


def get_health_advice():
    try:
        # Define the API URL (replace with the actual health-related API URL)
        url = "https://api.healthprovider.com/advice"
        # Set any required headers or parameters
        #headers = {"Authorization": "Bearer YOUR_API_KEY"}
        # Send an HTTP GET request to the API
        response = requests.get(url)
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the JSON response and extract health advice or information
            health_data = response.json()
            advice = health_data.get("advice")
            if advice:
                return advice
            else:
                return "Sorry, I couldn't fetch health advice at the moment."
        else:
            return "Sorry, I couldn't fetch health advice at the moment."
    except Exception as e:
        print("Sorry, I couldn't fetch health advice at the moment.:", str(e))
        return "Sorry, I couldn't fetch health advice at the moment."

def get_response(msg):
    # Check if the user's message is related to a web search
    words_to_check = ["search", "senka", "batla", "bata"]
    # Convert the input message to lowercase
    msg_lower = msg.lower()
    #if "search" in msg.lower() or "senka" in msg.lower():
    if any(word in msg_lower for word in words_to_check):
        # Extract the search query from the user's message
        query = msg.split("search", 1)[-1].strip()
        if query:
            # Construct the search URL using a search engine (e.g., Google)
            search_url = f"https://www.google.com/search?q={query}"
            # Open the web browser and perform the search
            webbrowser.open(search_url)
            # Return a response indicating that the search is being performed
            response = f"Opening the web browser and searching for '{query}'..."
            speak(response)  # Speak the response
            return response

    elif "advice" in msg.lower() or "kgakololo" in msg.lower():
        # Call the get_random_advice function to fetch advice
        advice = get_random_advice()
        speak(advice)  # Speak the advice
        return advice

    elif "joke" in msg.lower() or "metlae" in msg.lower():
        # Call the get_random_dad_joke function to fetch a dad joke
        dad_joke = get_random_dad_joke()
        speak(dad_joke)  # Speak the dad joke
        return dad_joke

    elif "health" in msg.lower() or "sick" in msg.lower():
        # Call the get_health_advice function to fetch health advice
        health_advice = get_health_advice()
        speak(health_advice)  # Speak the health advice
        return health_advice

    # If not a web search, proceed with your existing chatbot logic
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

    response = "Sorry! I'm still in training...didn't quite catch that.\nCould you rephrase or ask something else?"
    speak(response)  # Speak the default response
    return response


