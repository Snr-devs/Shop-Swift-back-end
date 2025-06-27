from flask import Blueprint, request, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity
from .extensions import db
from .models.task import Task
from .schemas.task_schema import TaskSchema

task_bp = Blueprint('tasks', __name__)
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


@task_bp.route('/api/tasks', methods=['POST'])
@jwt_required()
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('due_date') 
    user_id = get_jwt_identity()

    if not title:
        return make_response({'error': 'Title is required'}, 400)

    task = Task(title=title, description=description, due_date=due_date, user_id=user_id)
    db.session.add(task)
    db.session.commit()

    return make_response(task_schema.dump(task), 201)


@task_bp.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    user_id = get_jwt_identity()
    tasks = Task.query.filter_by(user_id=user_id).all()
    return make_response(tasks_schema.dump(tasks), 200)


@task_bp.route('/api/tasks/<int:id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return make_response({'error': 'Task not found'}, 404)

    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.due_date = data.get('due_date', task.due_date)
    task.completed = data.get('completed', task.completed)

    db.session.commit()
    return make_response(task_schema.dump(task), 200)


@task_bp.route('/api/tasks/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    user_id = get_jwt_identity()
    task = Task.query.filter_by(id=id, user_id=user_id).first()

    if not task:
        return make_response({'error': 'Task not found'}, 404)

    db.session.delete(task)
    db.session.commit()
    return make_response({'message': 'Task deleted successfully'}, 200)
