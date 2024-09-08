from flask import Flask, request, jsonify
import google.generativeai as genai
import os

app = Flask(__name__)

# Use environment variable for the API key to enhance security
genai_api_key = os.getenv("GENAI_API_KEY")
if not genai_api_key:
    raise ValueError("API key for Google Generative AI is not set")
genai.configure(api_key=genai_api_key)

@app.route('/', methods=['GET'])
def home():
    return jsonify({"message": "Welcome to the API"})

@app.route('/evaluate', methods=['POST'])
def evaluate_applicant():
    data = request.get_json()

    if not data or 'applicant' not in data:
        return jsonify({"error": "Invalid input data"}), 400

    applicant_data = data['applicant']

    try:
        # Generate response using the appropriate method
        response = genai.generate(
            model="models/gemini-1.5-pro-latest",
            prompt=f"Please score {applicant_data} out of 100 using the standard of tech companies. I know it is impossible but make the keys on {applicant_data} as standard and score it out of hundred. And give me your response as json format with only the score key along with its value. Have your own criteria, though. I don't need any explanation."
        )

        # Assuming the response contains a field 'generated_text'
        answer = response['generated_text']

        # Attempt to parse the JSON response
        try:
            result = json.loads(answer)
            return jsonify(result)
        except json.JSONDecodeError:
            return jsonify({"error": "Failed to parse JSON response"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
