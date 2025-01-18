from dotenv import load_dotenv
import os
from phi.agent import Agent, RunResponse
from phi.model.groq import Groq
import pyttsx3
from pymongo import MongoClient
from phi.utils.pprint import pprint_run_response

# Load environment variables from .env file
load_dotenv()

# Get sensitive information from environment variables
mongo_uri = os.getenv("MONGO_URI")
api_key = os.getenv("API_KEY")

# Initialize Text-to-Speech Engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[2].id)  # Adjust based on available voices
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 20)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

# MongoDB Connection (Localhost)
client = MongoClient(mongo_uri)
db = client["natours-test"]  # Replace with your desired database name
collection = db["products"]  # Replace with your desired collection name

# Groq API Key and Agent Initialization
agent = Agent(
    model=Groq(id="llama-3.3-70b-versatile", api_key=api_key)
)

# User Input
user_input = input("How Can I Help You: ")
response: RunResponse = agent.run(user_input)

# Response Content
content = response.content
pprint_run_response(response, markdown=True)
speak(content)

# Example MongoDB Interaction
data_to_store = {
    "user_input": user_input,
    "model_response": content
}

# Insert Data into MongoDB
collection.insert_one(data_to_store)

print("Data stored in MongoDB successfully.")
