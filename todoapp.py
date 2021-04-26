from flask import Flask, render_template, request, redirect, url_for, render_template_string
import random, re, json, uuid
from utilities import read_todo_file, run_validations, invalid_form_template, delete_todo_from_file

app = Flask(__name__)
todo_list = read_todo_file()

@app.route('/')
def index():
    """
    this is the index route for the todo app.
    and returns the index template
    """
    return render_template('index.html', todo_list=todo_list, cache_bust=random.random())


@app.route('/submit', methods=['POST'])
def submit():
    """
    this is the route for the submission for the todo app
    parameters include form value: task; email; priority
    returns: either index.html or error screen if any input is missing
    """
    form_data = request.form
    form_data_dict = dict(form_data)
    user_id = {'uuid': str(uuid.uuid1())}
    valid = run_validations(form_data_dict)
  
    if 'Incorrect' in valid.values():
        return render_template_string(invalid_form_template(), form=valid)

    todo_list.append({**form_data_dict, **user_id})
    return redirect(url_for('index'))


@app.route('/clear', methods=['POST'])
def clear():
    """
    rout to clear todo app
    return: clear todo object and return index
    """
    with open('todo-list.json', 'w') as file:
        json.dump([], file)
    
    todo_list.clear()

    return redirect(url_for('index'))


@app.route('/save', methods=['POST'])
def save():
    """
    route to save in todo app
    saves todo object in json format and return index
    """
    with open('todo-list.json', 'w') as file:
        json.dump(todo_list, file)

    return redirect(url_for('index'))


@app.route('/delete/<uuid>')
def delete(uuid):
    """
    delete route for todo app
    parameters: UUID to identify the todo app
    return: delete the task form the todo object and json file while returning index
    """
    todo = None

    for todo_item in todo_list:
        if todo_item['uuid'] == uuid:
            todo = todo_item
            todo_list.remove(todo)

    delete_todo_from_file(todo)    

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()
    todo_list = read_todo_file()
