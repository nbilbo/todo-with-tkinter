# encoding: utf-8
from json import load, dump, JSONDecodeError
import model_exceptions


FILE_NAME = 'tasks'


def load_file(file_name):
    '''
    Read a json file to transform in a python dict.
    
    paramaters
    ----------
    file_name : str
        full name for u json file (without .json extension); 
    
    return
    ------
    dict
    '''
    file_name += '.json'
        
    try:
        with open(file_name, 'r', encoding='utf-8') as f:
            return load(f)
    
    except (FileNotFoundError, JSONDecodeError):
        return {}

def save_file(file, file_name):
    '''
    Trasform a python dict to a json file and save it.
    
    parameters
    ----------
    file_name : str
        full name for u json file (without .json extension); 
    file : dict
    '''
    file_name += '.json'
        
    with open(file_name, 'w', encoding='utf-8') as f:
        dump(file, f, indent=4, ensure_ascii=False)
 
def striper(func):
    '''
    Decorator to strip an string.
    
    parameters
    ----------
    func : function
    
    return
    ------
    inner_func : function
    '''
    def inner_func(file, task):
        task = task.strip()
        
        return func(file, task)
    
    return inner_func

@striper   
def inser_task(file, task):
    '''
    Insert a new task in the file.
    
    parameters
    ----------
    file : dict
    
    task : str
    '''
    if task == '':
        raise ValueError(f'Must contain some value.')
        
    elif task in file.keys():
        raise model_exceptions.AlreadyStored(f'{task} already stored.')

    elif task not in file.keys():
        file[task] = False    

@striper
def updat_task(file, task):
    '''
    Inverts the task value.
    
    parameters
    ----------
    file : dict
    
    task : str
    '''
    if task == '':
        raise ValueError(f'Must contain some value.')
    elif task not in file.keys():
        raise model_exceptions.NotStored(f'{task} not stored.')  
    else:
        file[task] = not file[task]

@striper
def delet_task(file, task):
    '''
    Delete a task in file.
    
    parameters
    ----------
    file : dict
    
    task : str
    '''
    if task == '':
        raise ValueError(f'Must contain some value.')
    elif task not in file.keys():
        raise model_exceptions.NotStored(f'{task} not stored.')
    else:
        file.pop(task)
    

