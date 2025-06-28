from flask import Flask
from flask import render_template, request, redirect, session, flash, abort
import config
import service

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    session["csrf_token"] = service.create_csrf_token()
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":
        service.check_csrf()
        username = request.form["username"]
        password = request.form["password"]

        if service.valid_login(username, password):
        
            if service.validate_user(username, password):
                return redirect("/main")
        
        flash("Invalid username or password")
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "GET":
        session["csrf_token"] = service.create_csrf_token()
        return render_template("register.html", filled={})


    if request.method == "POST":
        service.check_csrf()

        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if not service.valid_username(username):
            flash("Username must be between 3 and 12 characters and it must contain only letters")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        if password1 != password2:
            flash("Passwords do not match")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        if len(password1) < 6:
            flash("Password must be at least 6 characters long")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        try:
            service.create_user(username, password1)
        except:
            flash(f"Username {username} already exists")
            return redirect("/register")

        return redirect("/")
    

@app.route("/main")
def main():
    service.require_login()

    project_offset = request.args.get("offset", 0, type=int)
    limit = 10

    projects = service.get_latest_projects(session["user_id"], project_offset, limit + 1)

    return render_template(
        "main.html",
        active_page="main",
        projects=projects[:limit],
        has_more=len(projects) > limit,
        next_offset=project_offset + limit
    )

@app.route("/logout", methods=["POST"])
def logout():
    service.check_csrf()
    session.clear()
    return redirect("/")

@app.route("/projects")
def projects():
    service.require_login()

    project_offset = request.args.get("offset", 0, type=int)
    limit = 10

    projects = service.get_latest_projects(session["user_id"], project_offset, limit + 1)

    return render_template(
        "projects.html",
        active_page="projects",
        projects=projects[:limit],
        has_more=len(projects) > limit,
        next_offset=project_offset + limit,
        search_projects=None,
        search_has_more=False,
        next_search_offset=0,
    )

@app.route("/projects/search")
def search_project():
    service.require_login()

    project_offset = request.args.get("offset", 0, type=int)
    limit = 10
    projects = service.get_latest_projects(session["user_id"], project_offset, limit + 1)

    projectname = request.args.get("projectname")
    project_offset_search = request.args.get("project_search_offset", 0, type=int)
    search_limit = 20

    searched_projects = service.search_project_by_name(
        session["user_id"], projectname, offset=project_offset_search, limit=search_limit + 1
    )

    return render_template(
        "projects.html",
        active_page="projects",
        projects=projects[:limit],
        has_more=len(projects) > limit,
        next_offset=project_offset + limit,
        search_projects=searched_projects[:search_limit],
        search_has_more=len(searched_projects) > search_limit,
        next_search_offset=project_offset_search + search_limit,
    )

@app.route("/projects/<int:project_id>")
def project(project_id):
    service.require_login()

    if service.check_view_permission(project_id):
        project_offset = request.args.get("offset", 0, type=int)
        limit = 10

        projects = service.get_latest_projects(session["user_id"], project_offset, limit + 1)
        fetched_project_data = service.get_project_data(project_id)
        project_owner_name = service.get_user_data(fetched_project_data["project_owner_id"])

        return render_template(
            "project.html",
            active_page="projects",
            projects=projects[:limit],
            has_more=len(projects) > limit,
            next_offset=project_offset + limit,
            project_data=fetched_project_data,
            project_owner_name=project_owner_name,
            limited_view=False
    )
    else:
        project_offset = request.args.get("offset", 0, type=int)
        limit = 10

        projects = service.get_latest_projects(session["user_id"], project_offset, limit + 1)
        fetched_project_data = service.get_project_data_limited(project_id)
        project_owner_name = service.get_user_data(fetched_project_data["project_owner_id"])


        return render_template(
            "project.html",
            active_page="projects",
            projects=projects[:limit],
            has_more=len(projects) > limit,
            next_offset=project_offset + limit,
            project_data=fetched_project_data,
            project_owner_name=project_owner_name,
            limited_view=True
    )

@app.route("/projects/add-project")
def add_projects():
    service.require_login()

    project_offset = request.args.get("offset", 0, type=int)
    limit = 10

    projects = service.get_latest_projects(session["user_id"], project_offset, limit + 1)

    return render_template(
        "new_project.html",
        active_page="projects",
        projects=projects[:limit],
        has_more=len(projects) > limit,
        next_offset=project_offset + limit,
        search_projects=None,
        search_has_more=False,
        next_search_offset=0,
    )




@app.route("/create_transaction", methods=["POST"])
def create_transaction():
    project_id = int(request.form["project_id"])
    amount = int(request.form["amount"])
    transaction_type = request.form["type"]
    user_id = int(request.form["user_id"])

    try:
        service.create_transaction(project_id, amount, transaction_type, user_id)
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

@app.route("/profile/<int:user_id>")
def profile(user_id):
    user_data = service.get_user_data(user_id)
    return render_template("profile.html", user=user_data)

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