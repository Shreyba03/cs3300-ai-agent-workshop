from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

PRIORITIES = ("Low", "Medium", "High")


tasks = [
    {"id": 1, "title": "Project-1 Report", "priority": "Medium"},
    {"id": 2, "title": "Project-2 MMFs", "priority": "Medium"}
]
next_id = 3


@app.route('/')
def index():
    """Render the task tracker page."""
    return render_template('index.html')


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Return all tasks with a default priority when necessary."""
    task_list = []
    for task in tasks:
        task_with_priority = dict(task)
        task_with_priority['priority'] = task.get('priority', 'Medium')
        task_list.append(task_with_priority)
    return jsonify(task_list)


@app.route('/api/tasks', methods=['POST'])
def add_task():
    """Create a task with a validated priority."""
    global next_id
    data = request.get_json()

    if not data or not data.get('title'):
        return jsonify({"error": "Title is required"}), 400

    priority = data.get('priority') or 'Medium'
    if priority not in PRIORITIES:
        return jsonify({"error": "Invalid priority"}), 400

    new_task = {
        "id": next_id,
        "title": data['title'],
        "priority": priority
    }
    tasks.append(new_task)
    next_id += 1

    return jsonify(new_task), 201


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete the task matching the supplied task ID."""
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({"result": "success"}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
