from flask import session, abort
import db
from werkzeug.security import check_password_hash

def search_user_id_by_username(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    return result[0]["id"]

def check_view_permission(project_id):
    user_id = session.get("user_id")
    if not user_id:
        abort(404)

    sql = """
    SELECT view_permission
    FROM project_visibility
    WHERE user_id = ? AND project_id = ?
    """
    result = db.query(sql, [user_id, project_id])
    if not result:
        return False
    return result[0]["view_permission"]

def get_project_data(project_id):
    sql = """
    SELECT project_id, project_name, balance, project_owner_id
    FROM projects
    WHERE project_id = ?
    """
    result = db.query(sql, [project_id])
    if not result:
        return None
    return result[0]

def get_user_data(user_id):
    sql = "SELECT username  FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    if not result:
        return None
    return result[0]

def validate_user(username, password):
    sql = "SELECT password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return False
    password_hash = result[0]["password_hash"]
    return check_password_hash(password_hash, password)

def get_user_id():
    sql = "SELECT id FROM users WHERE username = ?"
    username = session.get("username")
    user_id = db.query(sql, [username])
    return user_id[0]["id"]

def create_project(projectname, projectbalance, user_id):
    sql = "INSERT INTO projects (project_name, balance, project_owner_id) VALUES (?, ?, ?)"
    db.execute(sql, [projectname, projectbalance, user_id])

def create_user(username, password_hash):
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def add_view_permission(project_id, user_id):
    sql = "INSERT INTO project_visibility (user_id, project_id, view_permission, edit_permission) VALUES (?, ?, ?, ?)"
    db.execute(sql, [user_id, project_id, True, False])

def add_permissions(project_id, user_id, view_permission, edit_permission):
    sql = "INSERT INTO project_visibility (user_id, project_id, view_permission, edit_permission) VALUES (?, ?, ?, ?)"
    db.execute(sql, [user_id, project_id, view_permission, edit_permission])

def get_all_projects(user_id):
    sql = """
    SELECT project_id, project_name
    FROM projects
    WHERE project_id IN (
        SELECT project_id
        FROM project_visibility
        WHERE user_id = ? AND view_permission = TRUE
    )
    """
    visible_projects = db.query(sql, [user_id])
    return visible_projects

def get_project_id_by_name(projectname):
    sql = "SELECT project_id FROM projects WHERE project_name = ?"
    result = db.query(sql, [projectname])
    return result[0]["project_id"]

def search_project_by_name(user_id, projectname):
    sql = """
    SELECT project_name, balance
    FROM projects
    WHERE project_name = ?
    AND project_id IN (
        SELECT project_id
        FROM project_visibility
        WHERE user_id = ? AND view_permission = TRUE
    )
    """
    search_result = db.query(sql, [projectname, user_id])
    project_info = [(row["project_name"], row["balance"]) for row in search_result]
    return project_info

def delete_project_by_name(projectname):
    sql = "DELETE FROM projects WHERE project_name = ?"
    db.execute(sql, [projectname])

def update_balance_by_name(projectname, newbalance):
    sql = "UPDATE projects SET balance = ? WHERE project_name = ?"
    db.execute(sql, [newbalance, projectname])