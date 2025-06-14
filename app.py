from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import db
import config
import items

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/main")
def main():
    sql2 = "SELECT id FROM users WHERE username = ?"
    username = session.get("username")
    user_id = db.query(sql2, [username])
    visible_projects = items.get_all_projects(user_id[0]["id"])
    return render_template("main.html", items=visible_projects)

@app.route("/projects")
def projects():
    sql2 = "SELECT id FROM users WHERE username = ?"
    username = session.get("username")
    user_id = db.query(sql2, [username])
    visible_projects = items.get_all_projects(user_id[0]["id"])
    return render_template("projects.html", items=visible_projects)

@app.route("/projects/delete", methods=["POST"])
def delete_project():
    projectname = request.form["projectname"]
    print(projectname)

    items.delete_project_by_name(projectname)
    return redirect("/projects/manage")

@app.route("/projects/update_balance", methods=["POST"])
def update_balance():
    if request.method == "POST":
        newbalance = request.form["newbalance"]
        projectname = request.form["projectname"]
        items.update_balance_by_name(projectname, newbalance)
        return redirect("/projects/manage")

@app.route("/projects/search", methods=["GET", "POST"])
def search_project():
    if request.method == "POST":
        projectname = request.form["projectname"]

        sql2 = "SELECT id FROM users WHERE username = ?"
        username = session.get("username")
        user_id = db.query(sql2, [username])

        project_data = items.search_project_by_name(user_id[0]["id"], projectname)

        return render_template("manage.html", items=project_data)
    
@app.route("/projects/add")
def add_projects():
    return render_template("new_project.html")

@app.route("/projects/manage")
def manage_projects():
    return render_template("manage.html")

@app.route("/projects/addproject", methods=["POST"])
def addproject():


    projectname = request.form["project-name"]
    projectbalance = request.form["project-balance"]

    try:
        sql = "INSERT INTO projects (project_name, balance, project_owner_id) VALUES (?, ?, ?)"
        sql2 = "SELECT id FROM users WHERE username = ?"
        sql3 = "SELECT project_id FROM projects WHERE project_name = ?"
        sql4 = "INSERT INTO project_visibility (user_id, project_id, view_permission) VALUES (?, ?, ?)"
        username = session.get("username")
        user_id = db.query(sql2, [username])
        db.execute(sql, [projectname, projectbalance, user_id[0]["id"]])
        project_id = db.query(sql3, [projectname])[0]["project_id"]
        db.execute(sql4, [user_id[0]["id"], project_id, True])

    except sqlite3.IntegrityError:
        return "Something went wrong?"
    
    return redirect("/projects")

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        sql = "SELECT password_hash FROM users WHERE username = ?"
        password_hash = db.query(sql, [username])[0][0]

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/main")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

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