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
    render_template("register.html")

@app.route("/create", method=["POST"])
def create():
    username = request.form["username"]
    password1 = request.form["password1"]
    password2 = request.form["password2"]
    if password1 != password2:
        flash("VIRHE: Passwords do not match")
        return redirect("/register")

    return redirect("/")