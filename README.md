# todo

A minimalistic todo application written on python and jquery.

## Usage
On your shell or cmd, navigate to the source folder and type
```shell
python app.py
```
The app will by default run on `127.0.0.1:5000/index.html` location

## API
Make sure you do not commit un-necessary files onto github. For doing this, use the .gitignore file. Create a file called '.gitignore' in this directory and name all the
un-necesasry files in them. Have a look at the sample .gitignore file within this repository.

All todo items i.e. database is stored as .json file within your application (/) folder. 

### API Reference

*/*
By default you will get all the todo items, completed as well as yet to be completed ones.

*/tasks/<id>*
- GET = The url with the 'GET' http method will allow you to retreieve all tasks with the given 'id' wihtin the url.
- PUT = The url with the 'PUT' http method will allow you to update a given task with the given 'id' within the url.
- DELETE = The url with the 'DELETE' http method will allow you to delete a given task with the given 'id' within the url.

*/tasks/*
- POST = The url with the 'POST' http method will allow you to create a new task. The unique id will be auto generated in this case.

## Task JSON stucture
Every single task is an object (JSON) with the following structure

```javascript
{
    'id': <int>         # This will be auto-generated and unique.
    'title': <string>   # This will be the title (main todo item) of the todo item
    'desc': <string>    # This is an optional field with the description of the item.
    'status': <boolean> # 'true' means the item is done/completed. 'false' is otherwise.
}
```