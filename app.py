import json
from flask import Flask
from flask import request
from flask import jsonify
from flask import abort
from flask import make_response
from flask import request

app = Flask(__name__)

with open('data.json') as handle:
	data = json.load(handle)

# print(type(data), data)

# Get all tasks (default)
@app.route('/', methods=['GET'])
def get_tasks():
	return jsonify({ 'tasks': data })

# Get a specific task by id
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
	task = [task for task in data if task['id'] == task_id]
	if len(task) == 0: abort(404)
	return jsonify({'task': task[0]})

# Error 404
# -> todo: redirect to a saperate page
@app.errorhandler(404)
def not_found(error):
	return make_response(jsonify({ 'error': '404 Not Found' }))

# Add new task and get back the added task
@app.route('/tasks', methods=['POST'])
def create_task():
	if not request.json or not 'title' in request.json:
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
	return jsonify({ 'tasks': new_task }), 201

# Update an existing task by id
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
	task = [task for task in data if task['id'] == task_id]
	if len(task) == 0: abort(404)
	if not request.json: abort(404)
	if 'title' in request.json and type(request.json['title']) != unicode: abort(404)
	if 'desc' in request.json and type(request.json['desc']) is not unicode: abort(404)
	if 'status' in request.json and type(request.json['status']) is not bool: abort(404)
	task[0]['title'] = request.json.get('title', task[0]['title'])
	task[0]['desc'] = request.json.get('desc', task[0]['desc'])
	task[0]['status'] = request.json.get('status', task[0]['status'])
	return jsonify({ 'task': task[0] })

# Delete an existing task by id
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
	task = [task for task in data if task['id'] == task_id]
	if len(task) == 0: abort(404)
	data.remove(task[0])
	with open('data.json', 'w') as handle:
		json.dump(data, handle)
	return jsonify({ 'result': True })

if __name__ == '__main__':
	app.debug = True
	app.run()
