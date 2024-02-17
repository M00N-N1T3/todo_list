" a todo list cli application mde using the click module"

__auther__ = "Johnny Ilanga"

import click


@click.group
def mycommands(): # this section is the grouping of my click functions
    # it can be left empty
    pass

# The priority list. This dictionary contains the values that we want to compare the given args
# from click.choice() to
PRIORITIES = {
    "o" : "Optional",
    "l" : "Low",
    "m" : "Medium",
    "h" : "High",
    "c" : "Crucial"
}

@click.command()
# choice allows the given value to be checked against a set of predefined values
@click.argument('priority', type=click.Choice(PRIORITIES.keys()),default = 'm')
@click.argument('todofile',type=click.Path(exists=False),required = 0)
@click.option('-n','--name',prompt = 'Enter the todo name', help = 'The name of the todo item')
@click.option('-d','--description',prompt = "Describe the todo",help = 'The description of the todo')
# for every arg we have in the function that is a command the user needs to input we must connect to click
def add_todo(name, description, priority, todofile):
    # when adding parameters to a click function, all the parameters need to be connected with click
    # to do so we can use the @click.argument() for an argument that is mandatory\
    # or we can use @click.option() for an argument that is optional

    # if the todo file name is given by user make use of it else use this default one
    filename = todofile if todofile is not None else "mytodos.txt"

    with open(filename,'a+') as f:
        f.write(f'{name}: {description} [Priority: {PRIORITIES[priority]}]\n')

@click.command()
@click.argument('index',type=int, required=1)
def delete_todo(index):

    # this section deletes the given index 
    with open('mytodos.txt','r') as f:
        todo_list = f.read().splitlines() #splitlines() splits the lines after each line break
        todo_list.pop(index) # popping the given index
    
    with open('mytodos.txt','w') as f: # opening in w because we want to overwrite the data with new data
        f.write('\n'.join(todo_list))
        f.write('\n')


@click.command()
@click.option('-p','--priority',type=click.Choice(PRIORITIES.keys()))
# required = 0 means the arg is not required
@click.argument('todofile',type=click.Path(exists=True),required = 0) 
def list_todos(priority, todofile):
    filename = todofile if todofile is not None else "mytodos.txt"

    with open(filename, 'r') as f:
        todo_list = f.read().splitlines()
    if priority is None:
        for index, todo in enumerate(todo_list):
            print(f'({index}) - {todo}')
    else:
        for index, todo in enumerate(todo_list):
            if f'[Priority: {PRIORITIES[priority]}]' in todo:
                print(f'({index}) - {todo}')

# once you are done making your functions, you have to group them.
# grouping is done using a click function and it must be written right on top
# before you even start writing your function, so scroll up and look for 
# @click.group

# NB SCROLL UP BEFORE PROCEEDING
# once you have added the @click.group and you have created the empty function 
# you have to now add all your command functions to that empty function

# syntax: empty_func.add_command(the name of the command-function)
mycommands.add_command(add_todo) # add_todo is the name of a function i defined
mycommands.add_command(delete_todo)
mycommands.add_command(list_todos)


if __name__ == '__main__':
    # lastly we call our mycommands function    
    mycommands()