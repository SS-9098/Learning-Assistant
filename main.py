from fastapi import FastAPI
from Voice import getSpeech
import requests  # For sending requests to OpenAI API

app = FastAPI()

# Set the OpenAI API details here
API_URL = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
HEADERS = {
    "X-RapidAPI-Key": "your-api-key",  # Replace this with your actual API key
    "Content-Type": "application/json"
}


@app.get("/")
def read_root():
    return {"message": "Welcome to the Voice Assistant"}


@app.post("/speech-to-text/")
async def process_speech():
    # Step 1: Capture speech input using the getSpeech function from utils
    recognized_text = getSpeech().capitalize() + "?"

    # Step 2: Send the recognized text to the OpenAI API to get a response
    payload = {
        "messages": [
            {"role": "user", "content": recognized_text}
        ],
        "model": "gpt-4",
        "max_completion_tokens": 100,
        "temperature": 0.5,
        "name": "Study Buddy",
        "instructions": "You are a personal assistant named Study Buddy who helps students with their education"
    }

    response = requests.post(API_URL, headers=HEADERS, json=payload)

    if response.status_code == 200:
        # Extract the answer text from the OpenAI response
        answer = response.json()['choices'][0]['message']['content']
        cleaned_answer = answer.replace("**", "").replace("```", "").strip()

        # Return both the recognized text and the AI response
        return {"recognized_text": recognized_text, "answer": cleaned_answer}
    else:
        # Handle the case where the API request fails
        return {"error": "Failed to connect to OpenAI API", "status_code": response.status_code}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)