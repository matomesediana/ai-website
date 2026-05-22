from flask import Flask, render_template, request, redirect, session
import time
import os

app = Flask(__name__)

# 🔐 IMPORTANT: stable secret key
app.secret_key = "neoai_secret_key_12345"

# ---------------------------
# TEMP STORAGE (WARNING: resets on restart)
# ---------------------------
users = {}
chat_history = {}


# ---------------------------
# AI RESPONSE
# ---------------------------
def get_ai_response(text):
    time.sleep(1)
    return "AI (demo): " + text


# ---------------------------
# HOME (CHAT PAGE)
# ---------------------------
@app.route("/", methods=["GET", "POST"])
def home():
    # 🔐 must be logged in
    if "user" not in session:
        return redirect("/login")

    user = session["user"]

    # create chat space per user
    if user not in chat_history:
        chat_history[user] = []

    # send message
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


# ---------------------------
# REGISTER
# ---------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return "Missing fields"

        if username in users:
            return "User already exists"

        users[username] = password

        return redirect("/login")

    return render_template("register.html")


# ---------------------------
# LOGIN
# ---------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # validation
        if username in users and users[username] == password:
            session.clear()
            session["user"] = username
            return redirect("/")  # go to chat

        return "Invalid login"

    return render_template("login.html")


# ---------------------------
# LOGOUT
# ---------------------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


# ---------------------------
# FORCE ROUTE SAFETY (fix loops)
# ---------------------------
@app.before_request
def protect_routes():
    allowed_routes = ["login", "register", "static"]

    if request.endpoint not in allowed_routes:
        if "user" not in session and request.endpoint != "login":
            return redirect("/login")


# ---------------------------
# RUN SERVER (Render ready)
# ---------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)