from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin

import os

# initialize the flask module
app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

# database configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'db.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# to initialize database and marshmallow
db = SQLAlchemy(app)
ma = Marshmallow(app)


## MODELS
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(400))


    def __init__(self, title, description):
        # Add data to the instance. But why ??
        self.title = title
        self.description = description


## SCHEMAS
class TodoSchema(ma.Schema):
    class Meta:
        fields = ['id', 'title', 'description']

todo_schema = TodoSchema()
todos_schema = TodoSchema(many=True)

## ROUTES AND VIEWS
# why not required in django????
CORS(app,resources={r"/api": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


# Create a new todo 
@app.route('/api/todo', methods=['POST'])
@cross_origin(origin='*', headers=['content-type'])
def add_todo():
    title = request.json['title']
    description = request.json['description']

    # To create an instance
    new_todo = Todo(title, description)

    # save the instance in db
    db.session.add(new_todo)
    db.session.commit()

    # return json response
    return todo_schema.jsonify(new_todo)


# Get all todos
@app.route('/api/todo', methods=['GET'])
@cross_origin(origin='*', headers=['content-type'])
def get_todos():
    all_todos = Todo.query.all()

    # Try using jsonify
    response = todos_schema.dump(all_todos)
    return jsonify(response)


# Get a single todo with an id
@app.route('/api/todo/<id>', methods=['GET'])
@cross_origin(origin='*', headers=['content-type'])
def get_todo(id):
    todo = Todo.query.get(id)

    return todo_schema.jsonify(todo)


# update a todo
@app.route('/api/todo/<id>', methods=['PUT'])
@cross_origin(origin='*',headers=['Content-Type'])
def update_todo(id):
    todo = Todo.query.get(id)

    title = request.json['title']
    description = request.json['description']

    todo.title = title
    todo.description = description

    db.session.commit()

    return todo_schema.jsonify(todo)


# delete a todo
@app.route('/api/todo/<id>', methods=['DELETE'])
@cross_origin(origin='*',headers=['Content-Type'])
def delete_todo(id):
    todo = Todo.query.get(id)

    db.session.delete(todo)

    db.session.commit()

    # return success response
    return todo_schema.jsonify(todo)


if __name__ == '__main__':
    app.run(debug=True)