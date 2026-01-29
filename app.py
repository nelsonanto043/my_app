from flask import Flask, render_template, request, redirect, session
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("users.db")

# Create table (run once)
db = get_db()
db.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, password TEXT)")
db.commit()
db.close()

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = request.form["username"]
        p = request.form["password"]

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username=?", (u,)
        ).fetchone()
        db.close()

        if user and check_password_hash(user[1], p):
            session["user"] = u
            return redirect("/dashboard")
    return render_template("login.html")

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        u = request.form["username"]
        p = generate_password_hash(request.form["password"])

        db = get_db()
        db.execute("INSERT INTO users VALUES (?,?)", (u, p))
        db.commit()
        db.close()
        return redirect("/")
    return render_template("signup.html")

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html", user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
