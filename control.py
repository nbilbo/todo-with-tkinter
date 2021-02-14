# coding: utf-8
import model
import model_exceptions
import view


class Control(object):
    def __init__(self, file_name=None):
        '''
        parameters
        ----------
        file_name : str
            name for u json file(without .json extension); if None, the
            file will receive the dafault name.
        '''
        self._model = model.Model(file_name)
        self._view = view.View(self, f'Todo {self._model.file_name()}')
        self._view.show_todos(self._model.file())
        

    def _save_and_show(func, *args, **kwargs):
        '''
        Decorator to save and update the view.
        
        parameters
        ----------
        func : function
        
        return
        ------
        inner_func : function
        '''
        def inner_func(self, *args, **kwargs):
            func(self, *args, **kwargs)
            self._model.save_file()
            self._view.show_todos(self._model.file())
              
        return inner_func
    
    @_save_and_show
    def inser_task(self, task):
        '''
        Will try insert a new task. 
        
        parameters
        ----------
        task : str 
        '''
        try:
            self._model.inser_task(task)
            self._view.current().set('')
            self._view.show_message(f'\"{task}\" added with success.')
            
        except model_exceptions.AlreadyStored:
            self._view.show_alert(f'{task} already stored.')
            
        except ValueError:
            self._view.show_alert('Must contain some value.')
    
    @_save_and_show
    def updat_task(self, *tasks):
        '''
        Will update the status for each selectioned task.
        
        paramaters
        ----------
        tasks : str        
        '''
        if tasks:
            try:
                for task in tasks:
                    self._model.updat_task(task)
                self._view.show_message('Update complete.')
                    
            except model_exceptions.NotStored:
                self._view.show_alert(f'{task} not stored.')
        else:
            self._view.show_alert('Must select some value.')
    
    @_save_and_show
    def delet_task(self, *tasks):
        '''
        Will delete each selectioned task.
        
        paramaters
        ----------
        tasks : str
        '''
        if tasks:
            if self._view.askquestion('Do u really wan\'t delete?'):
                for task in tasks:
                    try:
                        self._model.delet_task(task)
                
                    except model_exceptions.NotStored:
                        self._view.show_alert(f'{task} not stored.')
        else:
            self._view.show_alert('Must select some value.')
        
    def main(self):
        '''
        Initialize the gui.
        '''
        self._view.main()






