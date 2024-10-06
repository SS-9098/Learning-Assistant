from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import Voice
import Video
from Search import search_query  # Importing the search_query function from Search.py

app = Flask(__name__)
CORS(app)

# Define the URL and headers for GPT-4 API
url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
headers = {
    "X-RapidAPI-Key": "7a86d10ba8mshac6a9d30c345183p1be452jsne2f259ea0591",  # Replace with your actual API key
    "Content-Type": "application/json"
}


@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.json  # Get the question from the frontend
    question = data.get("question", "")

    if question:
        # Create the payload for GPT-4 API
        payload = {
            "messages": [{"role": "user", "content": question}],
            "model": "gpt-4",
            "max_completion_tokens": 100,
            "temperature": 0.5,
            "name": "Study Buddy",
            "instructions": "You are a personal assistant named Study Buddy who helps students with their education"
        }

        # Send the request to the GPT-4 API
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 200:
            answer = response.json()['choices'][0]['message']['content']
            cleaned_answer = answer.replace("**", "").replace("```", "").strip()
            return jsonify({"answer": cleaned_answer}), 200
        else:
            print(response.text)
            return jsonify({"error": "API error", "details": response.text}), response.status_code
    else:
        return jsonify({"error": "No question provided"}), 400


@app.route('/voice', methods=['POST'])
def voice():
    result = Voice.getSpeech().capitalize() + '?'
    return jsonify({'speech': result})


@app.route('/video', methods=['POST'])
def video():
    data = request.json
    result = Video.youtube_search(data['question'])
    return jsonify({'name': result[0], 'link': result[1]})


@app.route('/search', methods=['POST'])  # New endpoint to handle search queries
def search():
    data = request.json
    if data:
        # Call the search_query function from Search.py
        search_results = search_query(data['question'])

        if search_results:
            return jsonify({'title': search_results[0]['title'], 'link': search_results[0]['url']}), 200
        else:
            return jsonify({'error': 'No articles found.'}), 404
    else:
        return jsonify({'error': 'No search query provided.'}), 400


if __name__ == "__main__":
    app.run(debug=True)
