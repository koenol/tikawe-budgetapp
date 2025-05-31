from flask import Flask
from flask import render_template, request, redirect, flash
from werkzeug.security import generate_password_hash
import sqlite3
import db

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/create", methods=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        return "Passwords do not match"

    password_hashed = generate_password_hash(password1)

    try:
        sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
        db.execute(sql, [username, password_hashed])
    except sqlite3.IntegrityError:
        return "Something went wrong?"
    
    return redirect("/")