from flask import Flask , render_template , url_for , request, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
import json


from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://wolf:wolf@localhost/portfolio'
db = SQLAlchemy(app)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)

# Create the database tables
with app.app_context():
    db.create_all()

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/myprojects')
def myProjects():
    projects = Project.query.all()
    return render_template('projects/projects.html',projects=projects)

@app.route('/create')#endpoint to the create dashboard
def create():
    return render_template('projects/add.html')

@app.route('/store', methods=['POST'])
def store():
    if request.method == 'POST':
        # Get the data from the form submission
        project_name = request.form.get('name')
        project_description = request.form.get('description')

        # Create a new Project object
        new_project = Project(name=project_name, description=project_description)

        # Add the new project to the database
        db.session.add(new_project)
        db.session.commit()

        # Use json.dumps to return a JSON response
        return redirect(url_for('myProjects'))

    return json.dumps({"message": "Invalid request method"}), 400



# Endpoint to delete a project by its ID
@app.route('/delete_project/<int:project_id>')
def delete_project(project_id):
    project = Project.query.get(project_id)

    if project:
        db.session.delete(project)
        db.session.commit()
        return redirect(url_for('myProjects', message="Project deleted successfully"))
    else:
        return jsonify({"message": "Project not found"}, 404)



@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    return 'form submitted.'

if __name__ == '__main__':
    app.run()