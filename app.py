from flask import Flask, render_template, request, redirect
import time
import os

app = Flask(__name__)

messages = []

# Fake AI (no API needed)
def get_ai_response(text):
    time.sleep(1)
    return "AI (demo): " + text

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        user_input = request.form.get("message")

        if user_input:
            messages.append(("You", user_input))
            messages.append(("AI", get_ai_response(user_input)))

        return redirect("/")

    return render_template("index.html", messages=messages)

if __name__ == "__main__":
    # FIX FOR RENDER DEPLOYMENT
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
