from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
from ibm_watsonx_ai.foundation_models import Model


load_dotenv()
app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return "Backend is running successfully"

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json

    electricity = int(data.get("electricity"))
    water = int(data.get("water"))
    transport = data.get("transport")

    suggestions = []

    if electricity > 300:
        suggestions.append("Your electricity usage is high. Consider using LED lights and energy-efficient appliances.")

    if water > 4000:
        suggestions.append("Your water usage is high. Try fixing leaks and using water-saving fixtures.")

    if transport == "Private Vehicle":
        suggestions.append("Using public transport or carpooling can reduce your carbon footprint.")

    if not suggestions:
        suggestions.append("Great job! Your lifestyle is already sustainable.")

    return jsonify({
        "suggestions": suggestions
    })

API_KEY = os.getenv("WATSONX_API_KEY")
PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
URL = "https://us-south.ml.cloud.ibm.com"

@app.route("/ai-test", methods=["POST"])
def ai_test():
    data=request.json
    user_input = request.json.get("text")

    model = Model(
        model_id="ibm/granite-3-8b-instruct",
        credentials={
            "apikey": API_KEY,
            "url": URL
        },
        project_id=PROJECT_ID
    )

    response = model.generate_text(
        prompt = f"""
        You are an AI sustainability advisor working on UN SDGs.

        User data:
        - Monthly electricity usage: {data.get('electricity')} units
        - Monthly water usage: {data.get('water')} liters
        - Primary transport mode: {data.get('transport')}

        Instructions:
        1. If electricity usage is high, give energy-saving advice (SDG 7).
        2. If water usage is high, give water conservation advice (SDG 6).
        3. If transport mode is "Private Vehicle", suggest greener alternatives like public transport, carpooling, or cycling (SDG 11 & SDG 13).
        4. If transport mode is already sustainable, appreciate and encourage it.
        5. Keep suggestions short, practical, and personalized.
        IMPORTANT: You MUST give at least one suggestion specifically about the transport mode.
        You MUST mention the transport mode in your response.
        you MUST Suggest or appreciate if transport is public or Walking

        Respond in 3–5 bullet points.
        
        """,
        params={
            "max_new_tokens": 100
        }
    )

    return jsonify({"suggestion": response})


if __name__ == "__main__":
    app.run(debug= True, host="0.0.0.0",port=5000)



