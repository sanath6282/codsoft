from tkinter import *
from tkinter import messagebox
import sqlite3 as sql

def add_task():  
    task_string = task_field.get()  
    if len(task_string) == 0:  
        messagebox.showinfo('Error', 'Field is Empty.')  
    else:    
        tasks.append(task_string)   
        the_cursor.execute('insert into tasks values (?)', (task_string ,))    
        list_update()    
        task_field.delete(0, 'end')  
    
def list_update():    
    clear_list()    
    for task in tasks:    
        task_listbox.insert('end', task)  
  
def delete_task():  
    try:  
        the_value = task_listbox.get(task_listbox.curselection())    
        if the_value in tasks:  
            tasks.remove(the_value)    
            list_update()   
            the_cursor.execute('delete from tasks where title = ?', (the_value,))  
    except:   
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')        
  
def delete_all_tasks():  
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')  
    if message_box == True:    
        while(len(tasks) != 0):    
            tasks.pop()    
        the_cursor.execute('delete from tasks')   
        list_update()  
   
def clear_list():   
    task_listbox.delete(0, 'end')  
  
def close():    
    print(tasks)   
    guiWindow.destroy()  
    
def retrieve_database():    
    while(len(tasks) != 0):    
        tasks.pop()    
    for row in the_cursor.execute('select title from tasks'):    
        tasks.append(row[0])  
   
if __name__ == "__main__":   
    guiWindow = Tk()   
    guiWindow.title("To-Do List")  
    guiWindow.geometry("665x400+550+250")   
    guiWindow.resizable(0, 0)  
    guiWindow.configure(bg="#F0F0F0")  # Light grey background for better readability
   
    the_connection = sql.connect('listOfTasks.db')   
    the_cursor = the_connection.cursor()   
    the_cursor.execute('create table if not exists tasks (title text)')  
    
    tasks = []  
        
    functions_frame = Frame(guiWindow, bg="#F0F0F0") 
    functions_frame.pack(side="top", expand=True, fill="both")  
 
    task_label = Label(
        functions_frame,
        text="TO-DO LIST\nEnter the Task Title:",
        font=("Arial", "16", "bold"),
        background="#F0F0F0", 
        foreground="#3B3B3B",  # Darker font color for contrast
    )    
    task_label.pack(pady=10)  # Padding for neat spacing
    
    task_field = Entry(
        functions_frame,
        font=("Arial", "14"),  
        width=50,  
        foreground="black",
        background="white",  
        relief=GROOVE  # Adds a subtle border
    )    
    task_field.pack(pady=5)  
    
    button_frame = Frame(functions_frame, bg="#F0F0F0")
    button_frame.pack(pady=10)
    
    add_button = Button(
        button_frame,
        text="Add",
        width=12,
        bg='#77DD77',
        fg="white",
        font=("Arial", "12", "bold"),
        command=add_task,
    )  
    del_button = Button(
        button_frame,
        text="Remove",
        width=12,
        bg='#FF6961',
        fg="white",
        font=("Arial", "12", "bold"),
        command=delete_task,
    )  
    del_all_button = Button(
        button_frame,
        text="Delete All",
        width=12,
        font=("Arial", "12", "bold"),
        bg='#FF6961',
        fg="white",
        command=delete_all_tasks  
    )
    
    exit_button = Button(
        functions_frame,
        text="Exit / Close",
        width=15,
        bg='#4682B4',
        fg="white",
        font=("Arial", "12", "bold"),
        command=close  
    )  
    
    add_button.grid(row=0, column=0, padx=5)
    del_button.grid(row=0, column=1, padx=5)
    del_all_button.grid(row=0, column=2, padx=5)
    exit_button.pack(pady=20)  # Centering and spacing
    
    task_listbox = Listbox(
        functions_frame,
        width=60,  # Reduced width
        height=8,  # Reduced height
        font=("Arial", 12),
        selectmode='SINGLE',  
        background="white",
        foreground="black",    
        selectbackground="#FF8C00",  
        selectforeground="black",
        relief=RIDGE  # Adds a subtle 3D border
    )    
    task_listbox.pack(pady=10)  
    
    retrieve_database()  
    list_update()    
    guiWindow.mainloop()    
    the_connection.commit()  
    the_cursor.close()
