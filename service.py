from flask import session, abort, request
import db
from werkzeug.security import check_password_hash, generate_password_hash
import re
import secrets

def valid_login(username, password):
    if not username or not password:
        return False
    username = sanitize(username)
    if len(username) < 3 or len(username) > 12 or len(password) < 6:
        return False
    return True

def sanitize(text):
    if not isinstance(text, str):
        return ""
    text = text.strip()
    text = re.sub(r'<.*?>', '', text)
    text = re.sub(r'on\w+=".*?"', '', text, flags=re.IGNORECASE)
    text = re.sub(r'(javascript:|data:|vbscript:)', '', text, flags=re.IGNORECASE)
    return text

def validate_user(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return False
    password_hash = result[0]["password_hash"]
    if check_password_hash(password_hash, password):
        session["user_id"] = result[0]["id"]
        session["username"] = username
        return True
    return False

def create_csrf_token():
    token = session.get("csrf_token")
    if not token:
        token = secrets.token_hex(16)
    return token

def check_csrf():
    form_token = request.form.get("csrf_token")
    session_token = session.get("csrf_token")
    if not form_token or form_token != session_token:
        abort(403)

def valid_username(username):
    if not username:
        return False
    username = sanitize(username)
    if len(username) < 3 or len(username) > 12 or not username.isalpha():
        return False
    return True

def create_user(username, password):
    password_hash = generate_password_hash(password)
    sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
    db.execute(sql, [username, password_hash])

def require_login():
    if "user_id" not in session:
        abort(403)

def get_latest_projects(user_id, offset=0, limit=10):
    sql = """
    SELECT project_id, project_name
    FROM projects
    WHERE project_id IN (
        SELECT project_id
        FROM project_visibility
        WHERE user_id = ? AND view_permission = TRUE
        LIMIT ? OFFSET ?
    )
    """
    visible_projects = db.query(sql, [user_id, limit, offset])
    return visible_projects

def search_project_by_name(user_id, projectname, offset=0, limit=20):
    projectname_sanitized = sanitize(projectname)
    projectname_like = f"%{projectname_sanitized}%"

    sql = """
    SELECT project_id, project_name
    FROM projects
    WHERE project_name LIKE ?
    LIMIT ? OFFSET ?
    """
    visible_projects = db.query(sql, [projectname_like, limit, offset])
    return visible_projects

def check_view_permission(project_id):
    user_id = session.get("user_id")
    if not user_id:
        abort(403)

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


def get_project_data_limited(project_id):
    sql = """
    SELECT project_id, project_name, project_owner_id
    FROM projects
    WHERE project_id = ?
    """
    result = db.query(sql, [project_id])
    if not result:
        return None
    return result[0]

def convert_to_cents(amount):
    if isinstance(amount, int):
        return amount * 100
    if isinstance(amount, str) and amount.isdigit():
        return int(amount) * 100
    return 0

def create_project(projectname, user_id, desc=None):
    sql = "INSERT INTO projects (project_name, project_owner_id, project_desc) VALUES (?, ?, ?)"
    db.execute(sql, [projectname, user_id, desc])

def init_project(projectname, user_id, balance=0):
    project_id = get_project_id_by_name(projectname)
    create_transaction(project_id, balance, "income", "lol", user_id)
    print("updating balance")
    update_project_balance(project_id, balance)

def get_project_id_by_name(projectname):
    sql = "SELECT project_id FROM projects WHERE project_name = ?"
    result = db.query(sql, [projectname])
    return result[0]["project_id"]

def create_transaction(project_id, amount, transaction_type, transaction_message, user_id):
    sql = """
    INSERT INTO transactions (user_id, amount, transaction_type, transaction_message, project_id, date)
    VALUES (?, ?, ?, ?, ?, datetime('now'))
    """
    db.execute(sql, [user_id, amount, transaction_type, transaction_message, project_id])

def update_project_balance(project_id):
    sql = """
    UPDATE projects
    SET balance = (
        SELECT SUM(amount)
        FROM transactions
        WHERE project_id = ?
    )
    WHERE project_id = ?
    """
    db.execute(sql, [project_id, project_id])

def get_all_transactions(project_id):
    sql = """
    SELECT transaction_id, amount, transaction_type, user_id, date
    FROM transactions
    WHERE project_id = ?
    """
    return db.query(sql, [project_id])

def search_user_id_by_username(username):
    sql = "SELECT id FROM users WHERE username = ?"
    result = db.query(sql, [username])
    if not result:
        return None
    return result[0]["id"]

def get_edit_permissions(project_id):
    sql = """
    SELECT user_id
    FROM project_visibility
    WHERE project_id = ? AND edit_permission = TRUE
    """
    result = db.query(sql, [project_id])

    return [row["user_id"] for row in result]

def get_user_data(user_id):
    sql = "SELECT username  FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    if not result:
        return None
    return result[0]



def get_user_id():
    sql = "SELECT id FROM users WHERE username = ?"
    username = session.get("username")
    user_id = db.query(sql, [username])
    if not user_id:
        return None
    return user_id[0]["id"]



def add_view_permission(project_id, user_id):
    sql = "INSERT INTO project_visibility (user_id, project_id, view_permission, edit_permission) VALUES (?, ?, ?, ?)"
    db.execute(sql, [user_id, project_id, True, False])

def add_permissions(project_id, user_id, view_permission, edit_permission):
    sql = "INSERT INTO project_visibility (user_id, project_id, view_permission, edit_permission) VALUES (?, ?, ?, ?)"
    db.execute(sql, [user_id, project_id, view_permission, edit_permission])

def delete_project_by_name(projectname):
    sql = "DELETE FROM projects WHERE project_name = ?"
    db.execute(sql, [projectname])

def update_balance_by_name(projectname, newbalance):
    sql = "UPDATE projects SET balance = ? WHERE project_name = ?"
    db.execute(sql, [newbalance, projectname])