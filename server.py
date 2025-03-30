from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

# Configure your Gemini API key
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY") # Ensure GOOGLE_API_KEY is set in your environment variables.
if not GOOGLE_API_KEY:
    raise ValueError("Please set the GOOGLE_API_KEY environment variable.")

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-1.5-pro-latest')

def get_gemini_response(prompt):
    """Generates a response from the Gemini API."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"Error generating response: {e}")
        return "Sorry, I encountered an error. Please try again later."

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json['user_input']
    prompt = f"You are an expert agricultural advisor. Answer the following question:\n{user_input}"
    response = get_gemini_response(prompt)
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(debug=True)