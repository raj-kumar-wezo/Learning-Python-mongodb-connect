import os
from flask import Flask, render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET", "change-me")

# MongoDB Atlas setup
client = MongoClient(os.environ["MONGODB_URI"])
db = client[os.environ.get("MONGODB_DB", "mydb")]
collection = db[os.environ.get("MONGODB_COLLECTION", "submissions")]


@app.get("/form")
def form():
    return render_template("form.html")


@app.post("/form")
def submit_form():
    try:
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()

        if not name or not email:
            # show error on same page
            flash("Name and Email are required.", "error")
            return render_template("form.html", name=name, email=email), 400

        doc = {"name": name, "email": email}
        collection.insert_one(doc)

        # success → redirect to success page
        return redirect(url_for("success"))
    except Exception as e:
        # show error on same page (no redirect)
        flash(f"Error submitting data: {e}", "error")
        # Return 500 but keep user on the same form page
        return render_template("form.html"), 500


@app.get("/success")
def success():
    return render_template("success.html", message="Data submitted successfully")


if __name__ == "__main__":
    app.run(debug=True)
