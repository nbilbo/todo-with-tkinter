# coding: utf-8
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class View(Tk):
    PADX = PADY = 10
    
    def __init__(self, control, title, *args, **kwargs):
        '''
        parameters
        ----------
        control : control.Control
            object Control
        
        title : str
            windows title.
        '''
        super(View, self).__init__(*args, **kwargs)
        self._control = control
        self._title = title
        self._current = StringVar()

        self._create_btn_style()
        self._create_table_style()
        
        self._create_entry()
        self._create_btn_add()
        self._create_table()
        self._create_btn_upd()
        self._create_btn_del()
        self._config_table()

    def _create_entry(self):
        entry = ttk.Entry(self, textvariable=self._current, 
                          font=('Arial', 12, 'normal'))
        entry.pack(fill='x', padx=self.PADX)
        
        # commands
        entry.bind('<Return>', lambda event: self._call_inser_task())
    
    def _create_btn_add(self):
        self._btn_add = ttk.Button(self, text='Add', style='Todo.TButton')
        self._btn_add.pack(fill='x', padx=self.PADX)
        
        # commands
        self._btn_add['command'] = self._call_inser_task
    
    def _create_btn_upd(self):
        self._btn_upd = ttk.Button(self, text='Update', style='Todo.TButton')
        self._btn_upd.pack(fill='x', padx=self.PADX)
        
        # commands
        self._btn_upd['command'] = self._call_updat_task
    
    def _create_btn_del(self):
        self._btn_del = ttk.Button(self, text='Delete', style='Todo.TButton')
        self._btn_del.pack(fill='x', padx=self.PADX, pady=self.PADY)
        
        # commands
        self._btn_del['command'] = self._call_delet_task
        
    def _create_table(self):
        frame = Frame(self)
        self._table = ttk.Treeview(frame, style='Todo.Treeview')
        
        frame.pack_propagate(False)
        frame.pack(fill='both', expand=True, padx=self.PADX, pady=self.PADY)
        self._table.pack(fill='both', expand=True)
    
    def _config_table(self):
        self._table['columns'] = ('#todo', '#status')
        self._table.heading('#todo', text='Todo')
        self._table.heading('#status', text='Status')
        self._table.column('#0', minwidth=0, width=0, stretch=False)
        self._table.column('#status', minwidth=60, width=60, stretch=False)
    
    def _create_btn_style(self):
        style = ttk.Style()
        style.configure('Todo.TButton', font=('Arial', 12, 'normal'))
    
    def _create_table_style(self):
        style = ttk.Style()
        style.configure('Todo.Treeview', font=('Arial', 12, 'normal'))
        style.configure('Todo.Treeview.Heading', font=('Arial', 12, 'normal'))
    
    def _selections(self):
        '''
        Get every selection in table.
        
        return
        ------
        list
        '''
        selects = self._table.selection()
        return [self._table.item(select)['values'][0] for select in selects]
        
    def _call_inser_task(self):
        self._control.inser_task(self._current.get())
    
    def _call_updat_task(self):
        self._control.updat_task(*self._selections())
    
    def _call_delet_task(self):
        self._control.delet_task(*self._selections())
    
    def current(self):
        '''
        return
        ------
        tkinter.StringVar
        '''
        return self._current
    
    def show_todos(self, todos):
        '''
        Will isert the values in table.
        
        parameters
        ----------
        todos : list
        '''
        self._table.delete(*self._table.get_children())
        
        for key, value in todos.items():
            self._table.insert('', 'end', values=(key, value))
    
    def show_alert(self, alert):
        '''
        Open a new window showing an alert.
        
        parameters
        ----------
        message : str
        '''        
        messagebox.showwarning('Alert', alert)
    
    def show_message(self, message):
        '''
        Open a new window showing a message.
        
        parameters
        ----------
        message : str
        '''
        messagebox.showinfo('Info', message)
    
    def askquestion(self, question):
        '''
        Open a new window asking a question.
        
        parameters
        ----------
        question: str
        
        return
        ------
        bool
        '''
        return messagebox.askokcancel('Confirmation', question)
        
    def main(self):
        self.title(self._title)
        self.geometry('600x300+220+100')
        self.mainloop()
        

    
    