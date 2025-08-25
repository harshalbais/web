from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted

app = Flask(__name__)

# 🔑 Hardcode API Key directly (not using os.environ)
API_KEY = "AIzaSyCtk0gj9WUC2JJYHOz9hcKXm7X2fH_QDNQ"   # <-- yaha apna Gemini API key daalo
genai.configure(api_key=API_KEY)

# Gemini model
model = genai.GenerativeModel("gemini-1.5-flash")

SYSTEM_PROMPT = """
You are an AI Voice Course Consultant for an EdTech platform.
Guide students in choosing the right courses as per there potential and provided of nagpur college only(Eng + Hindi mix).
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "").strip()
    lang = data.get("lang", "en-US")

    if not user_msg:
        return jsonify({"reply": "Please say something 🙂", "lang": lang})

    try:
        print("🔹 User message:", user_msg)

        # 👇 Gemini doesn't support "system" role → include prompt as user prefix
        full_prompt = SYSTEM_PROMPT + "\n\nUser: " + user_msg

        resp = model.generate_content(full_prompt)

        print("🔹 Gemini raw response:", resp)

        # ✅ Extract text safely
        reply = ""
        if resp and resp.candidates:
            for c in resp.candidates:
                if c.content and c.content.parts:
                    for p in c.content.parts:
                        if hasattr(p, "text"):
                            reply += p.text.strip() + " "

        reply = reply.strip() or "Sorry, I couldn't generate a response."

    except ResourceExhausted:
        reply = "⚠ Daily AI quota khatam ho gaya. Apne interest aur budget batao, main course suggest karunga."
    except Exception as e:
        print("❌ Gemini error:", repr(e))
        reply = "Oops, kuch technical issue aa gaya. Human consultant se connect kara deta hoon."

    return jsonify({"reply": reply, "lang": lang})


if __name__ == "__main__":
    app.run( debug=True)
