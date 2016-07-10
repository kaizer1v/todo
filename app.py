import json
from flask import Flask
from flask import render_template
from flask import request

with open('data.json') as handle:
	data = json.load(handle)

app = Flask(__name__)


@app.route('/')
def get_all():
	return json.dumps(data)
	# return render_template('index.html')

@app.route('/todo')
def get_todo_all():
	return json.dumps(data['todo'])

@app.route('/todo/<task_id>')
def get_todo(task_id):
	# return json.dumps([ d for d in data['todo'] if d['id'] == task_id ])
	return task_id

@app.route('/todo/add', methods=['POST'])
def add_todo():
	# here todo_task is the 'name' attribute of the text field in the html form
	todo_task = request.form['todo_task'];
	return todo_task

## ============ COMPLETED

@app.route('/completed')
def get_completed_all():
	return json.dumps(data['completed'])

@app.route('/completed/<task_id>')
def get_completed(task_id):
	# return json.dumps([ d for d in data['completed'] if d['id'] == task_id ])
	return task_id

# print(data)
# suppose we have the data in the 'data' variable
#
# class get_todo_task:
# 	def GET(self, task_id):
# 		return [ d for d in data['todo'] if d['id'] == task_id ]
#
# class get_todo:
# 	def GET(self):
# 		return data['todo']
#
# class add_todo:
# 	def GET(self):
# 		return web.input()
#
# class get_completed_task:
# 	def GET(self, task_id):
# 		return [ d for d in data['completed'] if d['id'] == task_id ]
#
# class get_completed:
# 	def GET(self):
# 		return data['completed']
#
# class get_todo_count():
# 	def GET(self):
# 		return len(data['todo'])
#
# class get_completed_count():
# 	def GET(self):
# 		return len(data['completed'])
#
# # print(get_todo())
#
if __name__ == '__main__':
	# app = web.application(urls, globals())
	app.run()
