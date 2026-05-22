from flask import Flask, render_template, request, redirect, session
import time
import os

app = Flask(__name__)
app.secret_key = "neoai_secret_key"

# TEMP STORAGE (demo only)
users = {}

# CHAT PER USER (fixes shared messages problem)
chat_history = {}

def get_ai_response(text):
    time.sleep(1)
    return "AI (demo): " + text


# ---------- HOME (CHAT) ----------
@app.route("/", methods=["GET", "POST"])
def home():
    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    if user not in chat_history:
        chat_history[user] = []

    if request.method == "POST":
        message = request.form.get("message")

        if message:
            chat_history[user].append(("You", message))
            chat_history[user].append(("AI", get_ai_response(message)))

        return redirect("/")

    return render_template(
        "index.html",
        messages=chat_history[user],
        user=user
    )


# ---------- REGISTER ----------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users:
            return "User already exists"

        users[username] = password
        return redirect("/login")

    return render_template("register.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in users and users[username] == password:
            session["user"] = username
            return redirect("/")
        return "Invalid credentials"

    return render_template("login.html")


# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# ---------- RUN SERVER ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)