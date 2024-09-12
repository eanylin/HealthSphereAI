import os
from dotenv import load_dotenv

load_dotenv()

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from chatbot import ask_date_question, get_all_patient_names, get_all_hospital_names  # Updated import
import logging

logging.basicConfig(level=os.getenv('LOG_LEVEL', 'INFO'))
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='../templates', static_folder='../static')
CORS(app)  # This enables CORS for all routes

NEO4J_URI = os.getenv('NEO4J_URI')
USERNAME = os.getenv('NEO4J_USERNAME')
PASSWORD = os.getenv('NEO4J_PASSWORD')
DATABASE = os.getenv('NEO4J_DATABASE')

@app.route('/')
def home():
    return render_template('chat.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['message']
    logger.debug(f"Received user input: {user_input}")

    try:
        response = ask_date_question(user_input)
        logger.debug(f"Generated response: {response}")
        if not isinstance(response, dict):
            raise ValueError("Invalid response format")
        if 'answer' not in response:
            response['answer'] = "I'm sorry, I couldn't generate a proper answer."
        if 'date' not in response:
            response['date'] = None
        if 'confidence' not in response:
            response['confidence'] = 0
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}", exc_info=True)
        response = {
            "answer": "An error occurred while processing your request. Please try again later.",
            "date": None,
            "confidence": 0
        }
    return jsonify(response)

@app.route('/patients', methods=['GET'])
def get_patients():
    try:
        patient_names = get_all_patient_names()
        return jsonify(patient_names)
    except Exception as e:
        logger.error(f"Error fetching patient names: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred while fetching patient names"}), 500

@app.route('/hospitals', methods=['GET'])
def get_hospitals():
    try:
        organization_names = get_all_hospital_names()  # This function now returns all organizations
        return jsonify(organization_names)
    except Exception as e:
        logger.error(f"Error fetching organization names: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred while fetching organization names"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)