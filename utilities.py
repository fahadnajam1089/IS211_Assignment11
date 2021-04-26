import json, re

def read_todo_file():
    """
    utility function to read json file returns list of todo or empty list
    """
    try:
        todo_list = json.loads(open('todo-list.json').read())

    except IOError:
        todo_list = []

    return todo_list

def delete_todo_from_file(todo):
    """
    utility function to read, delete, write to json file.
    parameters are identifying the todo task.
    """
    try:
        json_list = json.loads(open('todo-list.json').read())

    except IOError:
        json_list = False

    if json_list:
        if todo in json_list:
            json_list.remove(todo)
            with open('todo-list.json', 'w') as file:
                json.dump(json_list, file)

def validations_config():
    """
    utility function to validate and check inputs when submitted.
    returns validation dictionary
    """
    return {
        'task': lambda task: 'Correct' if task else 'Incorrect',
        'email': lambda email: 'Correct' if re.search('^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$', email) else 'Incorrect',
        'priority':  lambda p: 'Correct' if p.lower() == 'low' or p.lower() == 'hard' or p.lower() == 'medium' else 'Incorrect'
    }    

def run_validations(form_dict):
    validations = validations_config()
    d = {}
    for k, v in form_dict.items():
        d[k] = validations[k](v)
    return d

def invalid_form_template():

    return