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
    "X-RapidAPI-Key": "4c7c959ed8msh9ce6b3a18b16faap1deb54jsn33aa8f0eb27e",  # Replace with your actual API key
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
            return jsonify({'title1': search_results[0]['title'], 'link1': search_results[0]['url'],
                            'title2': search_results[1]['title'], 'link2': search_results[1]['url']}), 200
        else:
            return jsonify({'error': 'No articles found.'}), 404
    else:
        return jsonify({'error': 'No search query provided.'}), 400


if __name__ == "__main__":
    app.run(debug=True)
