import string
import random
from tkinter import *
from tkinter import messagebox
import sqlite3

with sqlite3.connect("users.db") as db:
    cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(Username TEXT NOT NULL, GeneratedPassword TEXT NOT NULL);")
cursor.execute("SELECT * FROM users")
db.commit()
db.close()

class GUI():
    def __init__(self, master):
        self.master = master
        self.username = StringVar()
        self.passwordlen = IntVar()
        self.generatedpassword = StringVar()
        self.n_username = StringVar()
        self.n_generatedpassword = StringVar()
        self.n_passwordlen = IntVar()
        
        root.title('Password Generator')
        root.geometry('660x500')
        root.config(bg='#F5F5F5')
        root.resizable(False, False)

        self.label = Label(text="Password Generator", anchor=N, fg='#333333', bg='#F5F5F5', font='Helvetica 20 bold')
        self.label.grid(row=0, column=1, pady=20)

        self.user = Label(text="Enter User Name: ", font='Helvetica 14 bold', bg='#F5F5F5', fg='#333333')
        self.user.grid(row=1, column=0, padx=20, pady=10)

        self.textfield = Entry(textvariable=self.n_username, font='Helvetica 14', bd=4, relief='solid', width=30)
        self.textfield.grid(row=1, column=1, padx=20, pady=10)
        self.textfield.focus_set()

        self.length = Label(text="Enter Password Length: ", font='Helvetica 14 bold', bg='#F5F5F5', fg='#333333')
        self.length.grid(row=2, column=0, padx=20, pady=10)

        self.length_textfield = Entry(textvariable=self.n_passwordlen, font='Helvetica 14', bd=4, relief='solid', width=30)
        self.length_textfield.grid(row=2, column=1, padx=20, pady=10)
        
        self.generated_password = Label(text="Generated Password: ", font='Helvetica 14 bold', bg='#F5F5F5', fg='#333333')
        self.generated_password.grid(row=3, column=0, padx=20, pady=10)

        self.generated_password_textfield = Entry(textvariable=self.n_generatedpassword, font='Helvetica 14', bd=4, relief='solid', width=30, fg='#DC143C')
        self.generated_password_textfield.grid(row=3, column=1, padx=20, pady=10)

        self.generate = Button(text="Generate Password", bd=3, relief='raised', padx=10, pady=5, font='Helvetica 14 bold', fg='#FFFFFF', bg='#4CAF50', command=self.generate_pass)
        self.generate.grid(row=4, column=1, pady=20)

        self.accept = Button(text="Accept", bd=3, relief='raised', padx=10, pady=5, font='Helvetica 14 bold', fg='#FFFFFF', bg='#2196F3', command=self.accept_fields)
        self.accept.grid(row=5, column=1, pady=10)

        self.reset = Button(text="Reset", bd=3, relief='raised', padx=10, pady=5, font='Helvetica 14 bold', fg='#FFFFFF', bg='#F44336', command=self.reset_fields)
        self.reset.grid(row=6, column=1, pady=10)

    def generate_pass(self):
        upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        lower = "abcdefghijklmnopqrstuvwxyz"
        chars = "@#%&()\"?!"
        numbers = "1234567890"
        upper = list(upper)
        lower = list(lower)
        chars = list(chars)
        numbers = list(numbers)
        name = self.textfield.get()
        leng = self.length_textfield.get()

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()

        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be a string")
            self.textfield.delete(0, 25)
            return

        length = int(leng)

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            self.length_textfield.delete(0, 25)
            return

        self.generated_password_textfield.delete(0, length)

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.n_generatedpassword.set(gen_passwd)

    def accept_fields(self):
        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(self.n_username.get())])

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username")
            else:
                insert = ("INSERT INTO users (Username, GeneratedPassword) VALUES (?, ?)")
                cursor.execute(insert, (self.n_username.get(), self.n_generatedpassword.get()))
                db.commit()
                messagebox.showinfo("Success", "Password generated successfully")

    def reset_fields(self):
        self.textfield.delete(0, 'end')
        self.length_textfield.delete(0, 'end')
        self.generated_password_textfield.delete(0, 'end')

if __name__ == '__main__':
    root = Tk()
    pass_gen = GUI(root)
    root.mainloop()
