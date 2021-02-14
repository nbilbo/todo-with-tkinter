# encoding: utf-8
import model_backend
import model_exceptions


class Model(object):
    def __init__(self, db_name=None):
        '''
        parameters
        ----------
        db_name : str
            name for u sqlite database(without .db extension); if None, 
            will receive the dafault name.
        '''
        self._db_name = db_name if db_name else model_backend.DB_NAME
        self._connection = model_backend.connect_to_db(self._db_name)
        model_backend.create_table(self._connection, self._db_name)
    
    def db_name(self):
        return self._db_name

    def inser_task(self, task):
        model_backend.inser_task(self._connection, self.db_name, task, 0)
    
    def updat_task(self, task):
        model_backend.updat_task(self._connection, self._db_name, task)
    
    def delet_task(self, task):
        model_backend.delet_task(self._connection, self._db_name, task)
    
    def selec_task(self, task):
        return model_backend.select_task(self._connection, self._db_name, task)
    
    def selec_tasks(self):
        return model_backend.selec_tasks(self._connection, self._db_name)
    
    def desconect_to_db(self):
        model_backend.desconect_to_db(self._connection)
    '''
    def save_file(self):
        model_backend.save_file(self._file, self._file_name)
    
    def load_file(self):
        self._file = model_backend.load_file(self._file_name)
    '''
    
if __name__ == '__main__':
    model = Model('teste')
    #model.inser_task('comprar pão')
    #model.inser_task('comprar coca-cola')
    #model.updat_task('comprar pão')
    #model.delet_task('comprar coca-cola')
    print(model.selec_tasks())
    model.desconect_to_db()