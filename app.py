import json
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request
from flask import url_for
from flask import render_template

app = Flask(__name__, static_url_path="")

'''Open the data.json where all todo items are saved and load into an object'''
with open('data.json') as handle:
    data = json.load(handle)

# print(type(data), data)

@app.route('/sample', methods=['GET'])
def sample():
    return render_template('template.html', tasks=data)

# Get all tasks (default)
@app.route('/', methods=['GET'])
def get_tasks():
    '''
    Get all the tasks in the database
    '''
    # return jsonify({ 'tasks': [permalinks(task) for task in data] })
    sortedList = sorted(data, key=lambda task: task['id'], reverse=True)
    return render_template('template.html', tasks=[permalinks(task) for task in sortedList])

# Get a specific task by id
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = [task for task in data if task['id'] == task_id]
    if len(task) == 0: abort(404)
    return jsonify({'task': permalinks(task[0])})

# Add new task and get back the added task
@app.route('/tasks', methods=['POST'])
def create_task():
    '''
    Add a new task and update the database
    '''
    if data[-1]['id'] + 1 > 10: return 201
    if not request.get_json(force=True) or not 'title' in request.get_json(force=True):
        abort(404)
    new_task = {
        'id': data[-1]['id'] + 1,
        'title': request.json['title'],
        'desc': request.json.get('desc', ""),
        'status': False
    }
    data.append(new_task)
    with open('data.json', 'w') as handle:
        json.dump(data, handle)
    return jsonify({ 'tasks': permalinks(new_task) }), 201

# Update an existing task by id
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    '''
    Given a task id, update its fields with appropriate data
    '''
    task = [task for task in data if task['id'] == task_id]
    if len(task) == 0: abort(404)
    if not request.json: abort(404)
    if 'title' in request.json and type(request.json['title']) != unicode: abort(404)
    if 'desc' in request.json and type(request.json['desc']) is not unicode: abort(404)
    if 'status' in request.json and type(request.json['status']) is not bool: abort(404)
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['desc'] = request.json.get('desc', task[0]['desc'])
    task[0]['status'] = request.json.get('status', task[0]['status'])
    return jsonify({ 'task': permalinks(task[0]) })

# Delete an existing task by id
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    '''
    Given a task id, remove the task and update the database
    '''
    print(task_id)
    task = [task for task in data if task['id'] == task_id]
    if len(task) == 0: abort(404)
    data.remove(task[0])
    with open('data.json', 'w') as handle:
        json.dump(data, handle)
    return jsonify({ 'result': True })

# Error 404
# -> todo: redirect to a saperate page
@app.errorhandler(404)
def not_found(error):
    '''Generate a json object for 404 response as well'''
    return make_response(jsonify({ 'error': '404 Not Found' }))

# This is to generate perma-links
def permalinks(task):
    '''
    Given a task obj, replace its id
    with a permalink (url)
    '''
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['url'] = url_for('get_task', task_id=task['id'], _external=True)
        else:
            new_task[field] = task[field]
    return new_task

if __name__ == '__main__':
    app.run(debug = True)
