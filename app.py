from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os

app = Flask(__name__)

# 🔑 Configure Gemini API
genai.configure(api_key = 'AIzaSyCtk0gj9WUC2JJYHOz9hcKXm7X2fH_QDNQ')
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data["message"]
    lang = data.get("lang", "en-US")  # default English

    # 🤖 Get response from Gemini
    response = model.generate_content(user_msg)

    return jsonify({"reply": response.text, "lang": lang})

if __name__ == "__main__":
    app.run(debug=True)
