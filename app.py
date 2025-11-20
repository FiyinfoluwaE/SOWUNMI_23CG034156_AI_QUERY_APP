import os
import sqlite3
import google.generativeai as gen_ai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load secret keys
load_dotenv()

# Initialize Flask App
web_portal = Flask(__name__)

# Configure the AI Model
API_CREDENTIAL = os.getenv("GEMINI_API_KEY")
gen_ai.configure(api_key=API_CREDENTIAL)
# model_engine = gen_ai.GenerativeModel('gemini-pro')
model_engine = gen_ai.GenerativeModel('gemini-2.5-flash')

# Database Configuration
DB_FILENAME = 'queries.db'

def setup_local_db():
    """Creates the database table if it doesn't exist."""
    try:
        db_link = sqlite3.connect(DB_FILENAME)
        cursor = db_link.cursor()
        # Creating a table with unique column names
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS interaction_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_prompt TEXT NOT NULL,
                ai_reply TEXT NOT NULL
            )
        ''')
        db_link.commit()
        db_link.close()
    except Exception as e:
        print(f"Database Error: {e}")

setup_local_db() # Ensure DB exists on start

@web_portal.route('/')
def home_page():
    """Serves the frontend HTML."""
    return render_template('index.html')

@web_portal.route('/process_request', methods=['POST'])
def handle_ai_query():
    """Receives input, talks to AI, saves to DB, returns answer."""
    incoming_data = request.json
    raw_question = incoming_data.get('query_text')

    if not raw_question:
        return jsonify({"error": "Empty prompt received"}), 400

    try:
        # 1. Send to AI
        ai_result = model_engine.generate_content(raw_question)
        clean_response = ai_result.text

        # 2. Save to Database
        db_link = sqlite3.connect(DB_FILENAME)
        cursor = db_link.cursor()
        cursor.execute('INSERT INTO interaction_logs (user_prompt, ai_reply) VALUES (?, ?)', 
                       (raw_question, clean_response))
        db_link.commit()
        db_link.close()

        # 3. Return to Frontend
        return jsonify({"response_text": clean_response})

    except Exception as error_msg:
        return jsonify({"error": str(error_msg)}), 500

if __name__ == '__main__':
    setup_local_db() # Ensure DB exists on start
    web_portal.run(debug=True)