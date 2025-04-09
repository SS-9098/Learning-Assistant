from flask import Flask, request, jsonify
from flask_cors import CORS
import webbrowser
import sqlite3
import requests
import Voice
import Video
import os
from Search import search_query

app = Flask(__name__)
CORS(app)
# app = Flask(__name__)

# SQLite connection
def get_db_connection():
    conn = sqlite3.connect('Student_db.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/get_user_details', methods=['POST'])
def get_user_details():
    data = request.get_json()
    user_name = data.get("name").strip()  # Strip any whitespace

    conn = get_db_connection()

    # Check with case insensitivity
    user = conn.execute("SELECT * FROM students WHERE lower(name) = lower(?)", (user_name,)).fetchone()
    conn.close()
    if user is None:
        return jsonify({"error": "User not found"}), 404

    user_details = {
        "id": user[0],
        "name": user[1],
        "pq1": user[2],
        "pq2": user[3],
    }

    return jsonify(user_details), 200


@app.route('/pq_update', methods=['POST'])
def upd():
    data = request.get_json()
    user_name = data.get("name").strip()
    conn = get_db_connection()

    # Check with case insensitivity
    user = conn.execute("SELECT * FROM students WHERE lower(name) = lower(?)", (user_name,)).fetchone()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    user_details = {
        "id": user[0],
        "name": user[1],
        "pq1": user[2],
        "pq2": user[3],
    }

    question = data.get("ques")
    conn.execute(f'Update students set pq2="{user[2]}" where id={user[0]}')
    conn.execute(f'Update students set pq1="{question}" where id={user[0]}')
    conn.commit()
    conn.close()
    return jsonify(user_details), 200

# Define the URL and headers for GPT-4 API
url = "https://cheapest-gpt-4-turbo-gpt-4-vision-chatgpt-openai-ai-api.p.rapidapi.com/v1/chat/completions"
headers = {
    "X-RapidAPI-Key": "129f14a6famsh22282ee9f5122a2p14e6bcjsn6f2761a1d1b3",  # Replace with your actual API key
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
    webbrowser.open_new_tab(f'file://{os.getcwd()}/FrontEnd/index.html'.replace('BackEnd', ''))
    app.run(debug=False, port=10000, host="0.0.0.0")
