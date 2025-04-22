from flask import Flask, request, jsonify

from datetime import datetime
import uuid

app = Flask(__name__)
  # Enable CORS for all domains

# In-memory database (replace with real DB like SQLite/PostgreSQL in production)
tasks = []

# Utility to filter tasks based on query params
def filter_tasks(filters):
    filtered = tasks
    for key, value in filters.items():
        if value:
            filtered = [t for t in filtered if str(t.get(key, '')).lower() == value.lower()]
    return filtered

@app.route('/', methods=['GET'])
def home():
    return "hello"
@app.route('/tasks', methods=['GET'])
def get_tasks():
    filters = {
        'contact_person': request.args.get('contact_person', ''),
        'task_type': request.args.get('task_type', ''),
        'entity_name': request.args.get('entity_name', ''),
        'status': request.args.get('status', '')
    }
    filtered = filter_tasks(filters)
    return jsonify(filtered), 200

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = {
        'id': str(uuid.uuid4()),
        'entity_name': data['entity_name'],
        'task_type': data['task_type'],
        'task_time': data['task_time'],
        'contact_person': data['contact_person'],
        'note': data.get('note', ''),
        'status': data.get('status', 'open')
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.json
    for task in tasks:
        if task['id'] == task_id:
            task.update({
                'entity_name': data.get('entity_name', task['entity_name']),
                'task_type': data.get('task_type', task['task_type']),
                'task_time': data.get('task_time', task['task_time']),
                'contact_person': data.get('contact_person', task['contact_person']),
                'note': data.get('note', task.get('note', '')),
                'status': data.get('status', task['status'])
            })
            return jsonify(task), 200
    return jsonify({'message': 'Task not found'}), 404

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    app.run(debug=True)
