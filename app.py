from flask import Flask, render_template, request, redirect

app = Flask(__name__)

messages = []

# Fake AI (no API needed)
def get_ai_response(text):
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
    app.run(debug=True)
