# encoding: utf-8
import model_backend
import model_exceptions


class Model(object):
    def __init__(self, file_name=None):
        '''
        parameters
        ----------
        file_name : str
            name for u json file (without .json extension); if None, 
            the file will receive the dafault name.
        '''
        self._file_name = file_name if file_name else model_backend.FILE_NAME
        self.load_file()
    
    def file(self):
        return self._file

    def file_name(self):
        return self._file_name

    def inser_task(self, task):
        model_backend.inser_task(self._file, task)
    
    def updat_task(self, task):
        model_backend.updat_task(self._file, task)
    
    def delet_task(self, task):
        model_backend.delet_task(self._file, task)
    
    def save_file(self):
        model_backend.save_file(self._file, self._file_name)
    
    def load_file(self):
        self._file = model_backend.load_file(self._file_name)

