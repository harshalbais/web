from flask import Flask, request, jsonify, render_template
import google.generativeai as genai

app = Flask(__name__)

# 🔑 Configure Gemini
genai.configure(api_key="AIzaSyCGIgXgAGunFMwLkNmtv6ny0xMJZJm73jA")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_msg = data["message"]
    lang = data.get("lang", "en-US")  # default English

    # 🤖 Send message to Gemini
    response = model.generate_content(user_msg)

    return jsonify({"reply": response.text, "lang": lang})

if __name__ == "__main__":
    app.run(debug=True)
