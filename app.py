from flask import Flask
from flask import render_template, request, redirect, session, flash, abort
from werkzeug.security import check_password_hash, generate_password_hash
import db
import config
import service

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    project_id = int(request.form["project_id"])
    amount = int(request.form["amount"])
    type = request.form["type"]
    user_id = int(request.form["user_id"])
    print("?")


    try:
        print("?")
        service.create_transaction(project_id, amount, type, user_id)
    except:
        flash("Failed to create transaction")
        return redirect(f"/projects/{project_id}")

    return redirect(f"/projects/{project_id}")

@app.route("/add_view_permission", methods=["POST"])
def add_view_permissions():

    project_id = int(request.form["project_id"])
    username = request.form["username"]

    if not username:
        flash("Username is required")
        return redirect("/projects/manage")

    user_id = service.search_user_id_by_username(username)
    if not user_id:
        flash("User not found")
        return redirect("/projects/manage")

    try:
        service.add_view_permission(project_id, user_id)
    except:
        flash("Failed to add permissions for the project")
        return redirect("/projects/manage")
    return redirect("/projects/manage")


@app.route("/projects/<int:project_id>")
def project(project_id):
    if service.check_view_permission(project_id):
        project_data = service.get_project_data(project_id)
        project_owner = service.get_user_data(project_data[3])
        project_edit_rights = service.get_edit_permissions(project_id)
        return render_template("project.html", project=project_data, project_owner=project_owner, project_edit_rights=project_edit_rights)
    else:
        abort(403)

@app.route("/profile/<int:user_id>")
def profile(user_id):
    user_data = service.get_user_data(user_id)
    return render_template("profile.html", user=user_data)

@app.route("/main")
def main():
    user_id = service.get_user_id()
    visible_projects = service.get_all_projects(user_id)
    return render_template("main.html", projects=visible_projects)

@app.route("/projects")
def projects():
    user_id = service.get_user_id()
    visible_projects = service.get_all_projects(user_id)
    return render_template("projects.html", projects=visible_projects)

@app.route("/projects/delete", methods=["POST"])
def delete_project():
    projectname = request.form["projectname"]
    service.delete_project_by_name(projectname)
    return redirect("/projects/manage")

@app.route("/projects/update_balance", methods=["POST"])
def update_balance():
    if request.method == "POST":
        newbalance = request.form["newbalance"]
        projectname = request.form["projectname"]
        service.update_balance_by_name(projectname, newbalance)
        return redirect("/projects/manage")

@app.route("/projects/search", methods=["GET", "POST"])
def search_project():
    if request.method == "POST":
        projectname = request.form["projectname"]
        user_id = service.get_user_id()
        project_data = service.search_project_by_name(user_id, projectname)
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
    if not projectname:
        flash("Project name is required")
        return redirect("/projects/add")
    projectbalance = request.form["project-balance"]

    user_id = service.get_user_id()

    try:
        service.create_project(projectname, projectbalance, int(user_id))
    except:
        flash("Project already exists or invalid input")
        return redirect("/projects/add")

    try:
        project_id = service.get_project_id_by_name(projectname)
        service.add_permissions(project_id, user_id, True, True)
    except:
        flash("Failed to add permissions for the project")
        return redirect("/projects/add")

    return redirect("/projects")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if service.validate_user(username, password):
            session["username"] = username
            session["user_id"] = service.get_user_id()
            return redirect("/main")
        else:
            flash("Invalid username or password")
            return redirect("/")

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
    if not username or len(username) > 16:
        abort(403)
    password1 = request.form["password1"]
    password2 = request.form["password2"]

    if password1 != password2:
        flash("Passwords do not match")
        return redirect("/register")

    password_hashed = generate_password_hash(password1)

    try:
        service.create_user(username, password_hashed)
    except:
        flash("Username already exists")
        return redirect("/register")

    return redirect("/")