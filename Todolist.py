import tkinter as tk
from tkinter import messagebox

def view_todo_list():
    try:
        with open("todo.txt", "r") as file:
            tasks = file.readlines()
            if not tasks:
                return "No tasks found."
            else:
                return "\n".join(tasks)
    except FileNotFoundError:
        return "No tasks found."

def add_task():
    task = entry_task.get()
    if task:
        with open("todo.txt", "a") as file:
            file.write(task + "\n")
        entry_task.delete(0, tk.END)
        messagebox.showinfo("Task Added", "Task added successfully.")
        update_task_listbox()
    else:
        messagebox.showwarning("Input Error", "Please enter a task.")

def mark_completed():
    selected_task = listbox_tasks.curselection()
    if selected_task:
        task_index = selected_task[0]
        with open("todo.txt", "r") as file:
            tasks = file.readlines()
            if 0 <= task_index < len(tasks):
                completed_task = tasks.pop(task_index)
                with open("completed.txt", "a") as completed_file:
                    completed_file.write(completed_task)
                with open("todo.txt", "w") as new_file:
                    new_file.writelines(tasks)
                messagebox.showinfo("Task Completed", "Task marked as completed.")
                update_task_listbox()
            else:
                messagebox.showwarning("Invalid Selection", "Invalid task selection.")
    else:
        messagebox.showwarning("No Selection", "Please select a task to mark as completed.")

def delete_task():
    selected_task = listbox_tasks.curselection()
    if selected_task:
        task_index = selected_task[0]
        with open("todo.txt", "r") as file:
            tasks = file.readlines()
            if 0 <= task_index < len(tasks):
                deleted_task = tasks.pop(task_index)
                with open("todo.txt", "w") as new_file:
                    new_file.writelines(tasks)
                messagebox.showinfo("Task Deleted", "Task deleted successfully.")
                update_task_listbox()
            else:
                messagebox.showwarning("Invalid Selection", "Invalid task selection.")
    else:
        messagebox.showwarning("No Selection", "Please select a task to delete.")

def update_task_listbox():
    listbox_tasks.delete(0, tk.END)
    tasks = view_todo_list().split("\n")
    for task in tasks:
        if task:
            listbox_tasks.insert(tk.END, task)

app = tk.Tk()
app.title("To-Do List Application")
app.configure(bg="#FFC107")

label_task = tk.Label(app, text="Enter Task:", bg="#FFC107")
entry_task = tk.Entry(app, width=50)
button_add = tk.Button(app, text="Add Task", command=add_task, bg="#4CAF50", fg="white")
button_complete = tk.Button(app, text="Mark Completed", command=mark_completed, bg="#2196F3", fg="white")
button_delete = tk.Button(app, text="Delete Task", command=delete_task, bg="#FF5733", fg="white")
listbox_tasks = tk.Listbox(app, selectmode=tk.SINGLE, width=50, height=10)

label_task.grid(row=0, column=0, pady=(10, 0), padx=10)
entry_task.grid(row=0, column=1, padx=10, pady=(10, 0))
button_add.grid(row=1, column=1, pady=10)
button_complete.grid(row=2, column=0, pady=10)
button_delete.grid(row=2, column=1, pady=10)
listbox_tasks.grid(row=3, column=0, columnspan=2, pady=10)

update_task_listbox()

screen_width = app.winfo_screenwidth()
screen_height = app.winfo_screenheight()
window_width = 500
window_height = 350
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
app.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

app.mainloop()
