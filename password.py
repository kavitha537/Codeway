import string
import random
import tkinter as tk
from tkinter import messagebox
import sqlite3
import hashlib

class GUI():
    def __init__(self, master):
        self.master = master
        self.username = tk.StringVar()
        self.passwordlen = tk.IntVar()
        self.generatedpassword = tk.StringVar()
        self.n_username = tk.StringVar()
        self.n_generatedpassword = tk.StringVar()
        self.n_passwordlen = tk.IntVar()

        master.title('Password Generator')
        master.geometry('660x500')
        master.config(bg='#FF8000')
        master.resizable(False, False)

        self.label = tk.Label(text=":PASSWORD GENERATOR:", anchor=tk.N, fg='darkblue', bg='#FF8000', font='arial 20 bold underline')
        self.label.grid(row=0, column=1)

        self.blank_label1 = tk.Label(text="")
        self.blank_label1.grid(row=1, column=0, columnspan=2)

        self.blank_label2 = tk.Label(text="")
        self.blank_label2.grid(row=2, column=0, columnspan=2)

        self.blank_label2 = tk.Label(text="")
        self.blank_label2.grid(row=3, column=0, columnspan=2)

        self.user = tk.Label(text="Enter User Name: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.user.grid(row=4, column=0)

        self.textfield = tk.Entry(textvariable=self.n_username, font='times 15', bd=6, relief='ridge')
        self.textfield.grid(row=4, column=1)
        self.textfield.focus_set()

        self.blank_label3 = tk.Label(text="")
        self.blank_label3.grid(row=5, column=0)

        self.length = tk.Label(text="Enter Password Length: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.length.grid(row=6, column=0)

        self.length_textfield = tk.Entry(textvariable=self.n_passwordlen, font='times 15', bd=6, relief='ridge')
        self.length_textfield.grid(row=6, column=1)

        self.blank_label4 = tk.Label(text="")
        self.blank_label4.grid(row=7, column=0)

        self.generated_password = tk.Label(text="Generated Password: ", font='times 15 bold', bg='#FF8000', fg='darkblue')
        self.generated_password.grid(row=8, column=0)

        self.generated_password_textfield = tk.Entry(textvariable=self.n_generatedpassword, font='times 15', bd=6, relief='ridge', fg='#DC143C')
        self.generated_password_textfield.grid(row=8, column=1)

        self.blank_label5 = tk.Label(text="")
        self.blank_label5.grid(row=9, column=0)

        self.blank_label6 = tk.Label(text="")
        self.blank_label6.grid(row=10, column=0)

        self.generate = tk.Button(text="GENERATE PASSWORD", bd=3, relief='solid', padx=1, pady=1, font='Verdana", 15 bold', fg='#68228B', bg='#BCEE68', command=self.generate_pass)
        self.generate.grid(row=11, column=1)

        self.blank_label5 = tk.Label(text="")
        self.blank_label5.grid(row=12, column=0)

        self.accept = tk.Button(text="ACCEPT", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.accept_fields)
        self.accept.grid(row=13, column=1)

        self.blank_label1 = tk.Label(text="")
        self.blank_label1.grid(row=14, column=1)

        self.reset = tk.Button(text="RESET", bd=3, relief='solid', padx=1, pady=1, font='Helvetica 15 bold italic', fg='#458B00', bg='#FFFAF0', command=self.reset_fields)
        self.reset.grid(row=15, column=1)


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

        if name == "":
            messagebox.showerror("Error", "Name cannot be empty")
            return

        if not name.isalpha():
            messagebox.showerror("Error", "Name must be alphabetic")
            self.textfield.delete(0, tk.END)
            return

        length = int(leng)

        if length < 6:
            messagebox.showerror("Error", "Password must be at least 6 characters long")
            return

        self.generated_password_textfield.delete(0, tk.END)

        u = random.randint(1, length - 3)
        l = random.randint(1, length - 2 - u)
        c = random.randint(1, length - 1 - u - l)
        n = length - u - l - c

        password = random.sample(upper, u) + random.sample(lower, l) + random.sample(chars, c) + random.sample(numbers, n)
        random.shuffle(password)
        gen_passwd = "".join(password)
        self.n_generatedpassword.set(gen_passwd)


    def accept_fields(self):
        username = self.n_username.get()
        generated_password = self.n_generatedpassword.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty")
            return

        if not generated_password:
            messagebox.showerror("Error", "Generated Password cannot be empty")
            return

        # Hash the password before storing in the database
        hashed_password = hashlib.sha256(generated_password.encode()).hexdigest()

        with sqlite3.connect("users.db") as db:
            cursor = db.cursor()
            find_user = ("SELECT * FROM users WHERE Username = ?")
            cursor.execute(find_user, [(username)])

            if cursor.fetchall():
                messagebox.showerror("Error", "This username already exists! Please use another username")
            else:
                insert = "INSERT INTO users(Username, GeneratedPassword) VALUES(?, ?)"
                cursor.execute(insert, (username, hashed_password))
                db.commit()
                messagebox.showinfo("Success!", "Password generated successfully")


    def reset_fields(self):
        self.textfield.delete(0, tk.END)
        self.length_textfield.delete(0, tk.END)
        self.generated_password_textfield.delete(0, tk.END)


if __name__ == '__main__':
    root = tk.Tk()
    pass_gen = GUI(root)
    root.mainloop()
