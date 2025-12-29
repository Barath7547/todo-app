from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Each task has a name and completed status
tasks = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    status = request.args.get('status')   # all, completed, pending
    sort = request.args.get('sort')       # az, za

    filtered_tasks = tasks

    # Filtering
    if status == 'completed':
        filtered_tasks = [t for t in filtered_tasks if t['completed']]
    elif status == 'pending':
        filtered_tasks = [t for t in filtered_tasks if not t['completed']]

    # Sorting
    if sort == 'az':
        filtered_tasks = sorted(filtered_tasks, key=lambda x: x['name'])
    elif sort == 'za':
        filtered_tasks = sorted(filtered_tasks, key=lambda x: x['name'], reverse=True)

    return jsonify(filtered_tasks)

@app.route('/add', methods=['POST'])
def add_task():
    data = request.get_json()
    task_name = data.get('name')

    if task_name:
        tasks.append({
            'name': task_name,
            'completed': False
        })
        return jsonify({'message': 'Task added'})
    return jsonify({'message': 'Invalid task'}), 400

@app.route('/toggle', methods=['POST'])
def toggle_task():
    data = request.get_json()
    name = data.get('name')

    for task in tasks:
        if task['name'] == name:
            task['completed'] = not task['completed']
            return jsonify({'message': 'Task updated'})
    return jsonify({'message': 'Task not found'}), 404

@app.route('/delete', methods=['POST'])
def delete_task():
    data = request.get_json()
    name = data.get('name')

    global tasks
    tasks = [t for t in tasks if t['name'] != name]
    return jsonify({'message': 'Task deleted'})

if __name__ == '__main__':
    app.run(debug=True)
