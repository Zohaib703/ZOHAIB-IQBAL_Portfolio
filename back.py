from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

@app.route("/")
def index():
    return "Welcome to ZOHAIB IQBAL Portfolio!"

@app.route("/projects", methods=["GET"])
def get_projects():
    projects = Project.query.all()
    return jsonify([{"id": p.id, "title": p.title, "description": p.description, "image_url": p.image_url} for p in projects])

@app.route("/projects", methods=["POST"])
def create_project():
    data = request.get_json()
    project = Project(title=data["title"], description=data["description"], image_url=data["image_url"])
    db.session.add(project)
    db.session.commit()
    return jsonify({"id": project.id})

@app.route("/projects/<int:project_id>", methods=["GET"])
def get_project(project_id):
    project = Project.query.get(project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404
    return jsonify({"id": project.id, "title": project.title, "description": project.description, "image_url": project.image_url})

@app.route("/projects/<int:project_id>", methods=["PUT"])
def update_project(project_id):
    project = Project.query.get(project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404
    data = request.get_json()
    project.title = data["title"]
    project.description = data["description"]
    project.image_url = data["image_url"]
    db.session.commit()
    return jsonify({"id": project.id})

@app.route("/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    project = Project.query.get(project_id)
    if project is None:
        return jsonify({"error": "Project not found"}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Project deleted"})

if __name__ == "__main__":
    app.run(debug=True)