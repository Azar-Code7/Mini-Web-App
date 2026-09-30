from flask import Flask, render_template, request, redirect, session
import sqlite3
import re
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.secret_key = "mini-web-app-secret-key"


def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NUll,
            email TEXT NOT NULL
        )
    """)

    cursor.execute("PRAGMA table_info(users)")
    columns = [column[1] for column in cursor.fetchall()]

    if "password" not in columns:
        cursor.execute("ALTER TABLE users ADD COLUMN password TEXT")
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/form", methods=["GET", "POST"])
def form():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        if not name or not email or not password:
            return render_template(
                "form.html",
                message="Please Enter Both Name and Email, and Password."
            )
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return render_template(
                "form.html",
                message = "Please Enter a Valid Email address."
            )
        
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        password_hash = generate_password_hash(password)

        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, password_hash)
        )
        
        conn.commit()
        conn.close()

        print("Name: ", name)
        print("Email: ", email)

        return render_template("form.html", message=f"Welcome, {name}!")
    
    return render_template("form.html")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        email = request.form["email"].strip()
        password = request.form["password"].strip()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()

        conn.close()

        if user and user[3] and check_password_hash(user[3], password):
            session["user_id"] = user[0]
            session["user_name"] = user[1]
            return f"Welcome back, {user[1]}!"
        
        return render_template(
            "login.html",
            message="Invalid Email or Password."
        )
    
    return render_template("login.html")

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")
    
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT id, name, email FROM users WHERE id = ?",
        (session["user_id"],)
    )

    user = cursor.fetchone()

    conn.close()

    return render_template("dashboard.html", user = user)

@app.route("/logout")
def logout():
    session.clear()

    return redirect("/login")

@app.route("/users")
def users():
    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    conn.close()
    return render_template("users.html", users=users)

@app.route("/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM users WHERE id = ?",
        (user_id,)
    )
    conn.commit()
    conn.close()

    return redirect("/users")

@app.route("/edit/<int:user_id>", methods=["GET", "POST"])
def edit_user(user_id):

    if "user_id" not in session:
        return redirect("/login")

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = ?",
        (user_id,)
    )

    user = cursor.fetchone()

    conn.close()

    if not user:
        return redirect("/users")

    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip()

        if not name or not email:
            return render_template(
                "edit.html",
                user=user,
                message="Please Enter Both Name and Email."
            )

        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
            return render_template(
                "edit.html",
                user=user,
                message="Please Enter a Valid Email Address."
            )

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE users SET name = ?, email = ? WHERE id = ?",
            (name, email, user_id)
        )

        conn.commit()
        conn.close()

        return redirect("/users")

    return render_template("edit.html", user=user)

if __name__ == "__main__":
    app.run(debug=True)