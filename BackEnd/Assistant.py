# this file is just for Backend testing
import requests  # Importing the requests library to make HTTP requests
import Voice
import ref_data

# Define the URL for the API endpoint you’re using
url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"

# Set up the headers, including your API key for authentication
headers = {
    "X-RapidAPI-Key": "4c7c959ed8msh9ce6b3a18b16faap1deb54jsn33aa8f0eb27e",  # This is your unique API key
    "Content-Type": "application/json"  # Specifies that we're sending JSON data
}

q = Voice.getSpeech()
if q:
    ques=q.capitalize()+"?"
else:
    # print("Sorry,Couldn't hear")
    quit()
print(f"{ques}\n")
ques = ques + " in 70 words or less"

# Define the query or message you want to send
payload = {
    "messages": [
        {"role": "user", "content": ques}  # Message asking a question
    ],
    "model": "gpt-4",          # Specifies the model type
    "max_completion_tokens": 50,          # Controls the length of the response
    "temperature": 0.5,# Controls creativity in responses (higher is more creative)
    "name": "Study Buddy",
    "instructions": "You are a personal assistant named Study Buddy who helps students with their education"
}

# Send the request to the API
response = requests.post(url, headers=headers, json=payload)

# Check if the request was successful
if response.status_code == 200:
    # Extract the answer text
    answer = response.json()['choices'][0]['message']['content']

    # Remove unwanted formatting symbols
    cleaned_answer = answer.replace("**", "").replace("```", "").strip()
    print("Answer:", cleaned_answer)
else:
    # If there’s an error, print the error code and message
    print("Error:", response.status_code, response.text)