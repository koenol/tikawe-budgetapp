import db

def get_all_projects(user_id):
    sql = "SELECT project_name FROM projects WHERE project_id IN (SELECT project_id FROM project_visibility WHERE user_id = ? AND view_permission = TRUE)"
    visible_projects = db.query(sql, [user_id])
    project_names = [row["project_name"] for row in visible_projects]
    return project_names

def search_project_by_name(user_id, projectname):
    sql = "SELECT project_name, balance FROM projects WHERE project_name = ? AND project_id IN (SELECT project_id FROM project_visibility WHERE user_id = ? AND view_permission = TRUE)"
    search_result = db.query(sql, [projectname, user_id])
    project_info = [(row["project_name"], row["balance"]) for row in search_result]
    return project_info

def delete_project_by_name(projectname):
    sql = "DELETE FROM projects WHERE project_name = ?"
    db.execute(sql, [projectname])