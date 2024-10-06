from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import requests
import Voice
import Video
import ref_data
from Search import search_query  # Importing the search_query function from Search.py
# from sqlitin import pqUpd

app = Flask(__name__)
CORS(app)

# app = Flask(__name__)

# SQLite connection
def get_db_connection():
    conn = sqlite3.connect('Student_db.db')
    conn.row_factory = sqlite3.Row  # This allows you to access row values by column names
    return conn

# Rule-based classification function
def classify_text_rule_based(user_input, field_keywords):
    user_input = user_input.lower()

    # Iterate over each field in the dictionary
    for field, subjects in field_keywords.items():
        for subject, keywords in subjects.items():
            if any(keyword in user_input for keyword in keywords):
                return {"field": field, "subject": subject}

    return {"field": "Unknown", "subject": "Unknown"}

# Interest checker function
def interest_checker(result, user_name):
    conn = get_db_connection()

    # Query for the user's interests
    user_interests = conn.execute("SELECT interest FROM student_interest WHERE lower(name) = lower(?)",
                                  (user_name.lower(),)).fetchall()

    conn.close()

    # Loop through the interests and match against the result field
    for row in user_interests:
        interest_value = row['interest']
        print(result['field'])
        # Access the 'interest' column value
        print(interest_value)
        if result['field'].lower() == interest_value.lower():
            return "Found your interest"

    # If no match is found
    return "Not your interest, do you want to add it?"

# Route to get user details and check interests
@app.route('/get_user_details', methods=['POST'])
def get_user_details():
    data = request.get_json()
    user_name = data.get("name").strip()  # Strip any whitespace
    question = data.get("question", "").strip()  # Get the question from the frontend

    conn = get_db_connection()

    # Fetch user details
    user = conn.execute("SELECT * FROM students WHERE lower(name) = lower(?)", (user_name.lower(),)).fetchone()

    if user is None:
        return jsonify({"error": "User not found"}), 404

    user_id = user['id']

    # Fetch field-related data (assuming you import ref_data which contains field-related keywords)
    result = classify_text_rule_based(question, ref_data.field_keywords)
    if result['field'] != "Unknown":
        # Check user interests based on the result field
        interest_response = interest_checker(result, user_name)
        print(interest_response)
    else:
        interest_response=None
        print("field not found")
    # Prepare the user details to send back
    user_details = {
        "id": user['id'],
        "name": user['name'],
        "pq1": user['pq1'],
        "pq2": user['pq2'],
        "interests_check": interest_response  # Interest check result
    }

    conn.close()
    return jsonify(user_details), 200



@app.route('/pq_update', methods=['POST'])
def upd():
    data = request.get_json()
    user_name = data.get("name").strip()
    conn = get_db_connection()

    # Check with case insensitivity
    user = conn.execute("SELECT * FROM students WHERE lower(name) = lower(?)", (user_name,)).fetchone()

    if user is None:
        print("uiyhi")
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
