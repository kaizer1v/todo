$(function () {
  // Keep focus on Textbox
  $('input[type=text]').focus();



  var Todo = function() {
    this.addItem = function(task) {
      return $.ajax('/tasks', {
        method: 'POST',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({
          title: task.title || 'Default Title',
          desc: task.desc || 'Default Description.'
        })
      });
    };

    this.updateItem = function(taskID, newStatus) {
      return $.ajax('/tasks/'+ taskID, {
        method: 'PUT',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ id: taskID, status: newStatus })
      });
    };

    this.deleteItem = function(taskID) {
      return $.ajax('/tasks/'+ taskID, {
        method: 'DELETE',
        dataType: 'json',
        contentType: 'application/json',
        data: JSON.stringify({ id: taskID })
      });
    };

    this.getItems = function() {

    };
  };

  // Instance of the todo application
  var todo = new Todo();
  var txtbox = $('#txt_newTask');
  var btnSubmit = $('button.addTask');
  var taskList = $('#todo-tasks');

  // Events
  btnSubmit.on('click', ui_addTask);
  taskList.on('click', '.glyphicon-trash', ui_deleteTask);
  taskList.on('click', 'input[type=checkbox]', ui_updateTask);
  txtbox.on('keydown', function(event) {
    // when user presses 'enter' key, trigger the add new item event
    if(event.keyCode === 13) $('button.addTask').trigger('click');
  });

  // Event Handlers
  function ui_addTask(event) {
    var newTask = {};
    newTask.title = txtbox.val();
    todo.addItem(newTask).done(function(result) {
      var check = (result.tasks.status === true) ? 'checked' : '';
      taskList.prepend('<li class="checkbox list-group-item" id="'+ result.tasks.id +'"><label><input type="checkbox" /><a href="'+ result.tasks.url +'">'+ result.tasks.title +'</a></label><span class="glyphicon glyphicon-trash align-right"></span></li>');
      txtbox.val("");
    }).fail(function(errMsg) {
      alert('An error occured while adding new item to your list. Please try again.');
      console.log(errMsg);
    });
  }

  function ui_updateTask(event) {
    var taskID = util_getID($(this).siblings('a').attr('href'));
    var taskStatus = $(this).is(':checked');
    if(taskStatus === true)
      $(this).siblings('a').addClass('strikethrough');
    else
      $(this).siblings('a').removeClass('strikethrough');
    todo.updateItem(taskID, taskStatus).done(function(result) {
      // Do Something
    }).fail(function(errMsg) {
      alert('An error occured while adding new item to your list. Please try again.');
      console.log(errMsg);
    });
  }

  function ui_deleteTask(event) {
    // extract id from the a href
    var listItem = $(this).parent('li').remove();
    var taskID = util_getID($(this).siblings('label').find('a').attr('href'));
    todo.deleteItem(taskID).done(function(result) {
      // remove the 'li' element form the ul
      // TODO ...
      // alert('Task successfully deleted.');
    }).fail(function(errMsg) {
      alert('An error occured while adding new item to your list. Please try again.');
      console.log(errMsg);
    });
  }

  function util_getID(taskURL) {
    return taskURL.split('/')[taskURL.split('/').length - 1];
  }

  function textRenderer(text) {
    var tarr1 = text.split('-'),
      tarr2 = tarr1[1].split('@'),
      title = tarr1[0],
      desc = tarr2[0],
      date = tarr2[1];
  }
});
