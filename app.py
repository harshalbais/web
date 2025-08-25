from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from google.api_core.exceptions import ResourceExhausted
import os

app = Flask(__name__)

# 🔑 Configure Gemini API
API_KEY = "AIzaSyCtk0gj9WUC2JJYHOz9hcKXm7X2fH_QDNQ"
if not API_KEY:
    raise RuntimeError("Missing Gemini API key.")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# 🎙️ System prompt for EdTech Voice Agent
SYSTEM_PROMPT = """
You are an AI Voice Course Consultant for an EdTech platform.
Your job is to guide students in choosing the right courses, just like a professional human consultant.

Responsibilities:
1) Provide Course Information (syllabus, fees, duration, eligibility, certifications, placement support) in simple language.
2) Personalized Guidance: ask background, goals, interests; suggest tailored courses.
3) Callback Option: offer to schedule a callback with a human consultant if needed.
4) Conversation Style: natural English + Hindi mix (clear Indian accent); polite, empathetic.
   Handle interruptions gracefully; keep replies short (2–4 sentences).
5) Fallback: if unsure, say you can connect to a human consultant.

Example Behaviors:
- Greeting: "Hi! 👋 I’m your course consultant. Aap kis field mein interested ho — technology, management, ya creative studies?"
- Recommendation: "Data Science interest ke basis par, main 6-month Data Analytics course suggest karta hoon. Isme Python, ML basics aur Tableau cover hota hai. Fees ~₹45,000 with placement support."
- Callback: "Kya aap quick callback schedule karna chahenge human consultant ke saath?"
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    user_msg = data.get("message", "").strip()
    lang = data.get("lang", "en-US")

    if not user_msg:
        return jsonify({"reply": "Please say something to begin. 🙂", "lang": lang})

    try:
        resp = model.generate_content([
            {"role": "system", "parts": [SYSTEM_PROMPT]},
            {"role": "user", "parts": [user_msg]}
        ])
        reply = (resp.text or "").strip() or "Sorry, I couldn't generate a response."
    except ResourceExhausted:
        reply = (
            "⚠️ I’ve reached my daily AI quota right now. "
            "Phir bhi main help kar sakta hoon: apne interest, budget aur duration batao; "
            "main suitable courses suggest karunga aur callback schedule kar dunga."
        )
    except Exception as e:
        print("Gemini error:", repr(e))
        reply = (
            "Oops, kuch technical issue aa gaya. "
            "Please try again, ya main aapko human consultant se connect kara deta hoon."
        )

    return jsonify({"reply": reply, "lang": lang})



if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render sets PORT dynamically
    app.run(host="0.0.0.0", port=port)

