from flask import Flask, request, jsonify
from models import db, Todo
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db.init_app(app)


# Create DB tables at startup
with app.app_context():
    db.create_all()


@app.route('/')
def home():
    return "Welcome to the Scalable Todo Backend!"


@app.route('/todos', methods=['GET'])
def get_todos():
    todos = Todo.query.all()
    return jsonify([todo.to_dict() for todo in todos])


@app.route('/todos', methods=['POST'])
def create_todo():
    data = request.json
    new_todo = Todo(task=data['task'])
    db.session.add(new_todo)
    db.session.commit()
    return jsonify(new_todo.to_dict()), 201


@app.route('/todos/<int:id>', methods=['PUT'])
def update_todo(id):
    todo = Todo.query.get_or_404(id)
    data = request.json
    todo.task = data.get('task', todo.task)
    todo.done = data.get('done', todo.done)
    db.session.commit()
    return jsonify(todo.to_dict())


@app.route('/todos/<int:id>', methods=['DELETE'])
def delete_todo(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
