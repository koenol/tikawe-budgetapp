import db

def get_all_projects(user_id):
    sql = "SELECT project_name FROM projects WHERE project_id IN (SELECT project_id FROM project_visibility WHERE user_id = ? AND view_permission = TRUE)"
    visible_projects = db.query(sql, [user_id])
    project_names = [row["project_name"] for row in visible_projects]
    return project_names