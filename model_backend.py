# encoding: utf-8
import sqlite3
from json import load, dump, JSONDecodeError
import model_exceptions


DB_NAME = ':memory:'


def tuple_to_dict(tuple):
    return dict(idtasks=tuple[0], name=tuple[1], status=tuple[2])

def connect_to_db(db_name):
    '''
    Initialize a connetion to sqlite db.
    
    paramaters
    ----------
    db_name : str
        data base name (without .db extension)
    
    return
    ------
    sqlite3.Connecition : object connection.
    '''
    if db_name != DB_NAME:
        db_name += '.db'
    print(f'connection in {db_name}')
        
    return sqlite3.connect(db_name)

def desconect_to_db(conn):
    '''
    Close connetion to data base.
    
    paramaters
    ----------
    conn : sqlite3.Connection
        object connection
    '''
    print('closing connection.')
    conn.close()

def connect(func):
    '''
    Decorator to reconnect to database.
    
    parameters
    ----------
    func : function
    
    return
    ------
    inner_func : funciton
    '''
    def inner_func(conn, db_name, *args, **kwargs):
        try:
            conn.execute('SELECT name FROM sqlite_temp_master WHERE type="table";')
            
        except (AttributeError, ProgrammingError):
            conn = connect_to_db(db_name)
            
        return func(conn, db_name, *args, **kwargs)
    
    return inner_func

@connect
def create_table(conn, db_name):
    '''
    Execute query to create the tables.
    
    paramaters
    ----------
    conn : sqlite3.Connection
        object connection
    
    db_name : str
        database nome (without .db extension).
    '''
    query = """
    create table if not exists tasks(
        idtasks integer primary key autoincrement,
        name char(127) not null unique,
        status integer default 0
    );
    """
    conn.execute(query)

@connect
def inser_task(conn, db_name, name, status):
    '''
    Insert a new register in database.

    parameters
    ----------
    conn: sqlite3.Connection
        object connection
    
    db_name : str
    
    name : str
    
    status : int
    '''
    query = 'insert into tasks (name, status) values (?, ?);'
    register = select_task(conn, db_name, name)
    if register:
        raise model_exceptions.AlreadyStored(f'{name} already stored.')
    else:
        conn.execute(query, (name, status))
        conn.commit()

@connect
def select_task(conn, db_name, name):
    '''
    Select a register from database.
    
    parameters
    ----------
    conn: sqlite3.Connection
        object connection
    
    db_name : str
    
    name : str
    
    returns
    -------
    dict : if find the register.
    
    None : if not find the register.
    '''
    query = 'select idtasks, name, status from tasks where name=?;'
    cursor = conn.execute(query, (name, ))
    register = cursor.fetchone()
    register = tuple_to_dict(register) if register else None
    
    return register

@connect
def selec_tasks(conn, db_name):
    '''
    Select all register from database.
    
    parameters
    ----------
    conn: sqlite3.Connection
        object connection
    
    db_name : str
    
    return
    ------
    list
    '''
    query = 'select idtasks, name, status from tasks order by status desc;'
    cursor = conn.execute(query)
    registers = [tuple_to_dict(register) for register in cursor.fetchall()]
    
    return registers

@connect
def updat_task(conn, db_name, name):
    '''
    Invert the status from a task.
    
    parameters
    ----------
    conn: sqlite3.Connection
        object connection
    
    db_name : str
    
    name : str
    '''
    sql = 'update tasks set status=? where name=?;'
    register = select_task(conn, db_name, name)
    
    if not register:
        raise model_exceptions.NotStored(f'{name} not stored.')
    else:
        new_status = not register['status']
        conn.execute(sql, (new_status, name))
        conn.commit()

@connect
def delet_task(conn, db_name, name):
    '''
    delete the register from database.
    
    parameters
    ----------
    conn: sqlite3.Connection
        object connection
    
    db_name : str
    
    name : str    
    '''
    sql = 'delete from tasks where name=?;'
    register = select_task(conn, DB_NAME, name)
    
    if not register:
        raise model_exceptions.NotStored(f'{name} not stored.')
    else:
        conn.execute(sql, (name,))
        conn.commit()
    

if __name__ == '__main__':
    conn = connect_to_db(DB_NAME)
    create_table(conn, DB_NAME)
    inser_task(conn, DB_NAME, 'comprar pão', 0)
    inser_task(conn, DB_NAME, 'comprar coca-cola', 0)
    updat_task(conn, DB_NAME, 'comprar pão')
    delet_task(conn, DB_NAME, 'comprar coca-cola')
    print(selec_tasks(conn, DB_NAME))
    desconect_to_db(conn)
        
    



