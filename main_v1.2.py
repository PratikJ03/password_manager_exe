import os
import sys
from tkinter import *
from tkinter import messagebox, simpledialog
import random
import json

FONT_NAME = "Courier"
MASTER_PASSCODE = "1234"

# ---------------------------- FILE SETUP ------------------------------- #
if not os.path.exists("master.txt"):
    with open("master.txt", "w") as file:
        file.write(MASTER_PASSCODE)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = list("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ")
    numbers = list("0123456789")
    symbols = list("!#$%&()*+")

    password_list = (
        [random.choice(letters) for _ in range(random.randint(8, 10))] +
        [random.choice(symbols) for _ in range(random.randint(2, 4))] +
        [random.choice(numbers) for _ in range(random.randint(2, 4))]
    )

    random.shuffle(password_list)
    pass1 = "".join(password_list)

    password.delete(0, END)
    password.insert(0, pass1)

    window.clipboard_clear()
    window.clipboard_append(pass1)
    window.update()

    generate_button.config(state="disabled")

# ---------------------------- PASSCODE HELPERS ------------------------------- #
def get_master_passcode():
    with open("master.txt", "r") as file:
        return file.read()

def change_passcode_window():
    def save_new_passcode():
        if old_entry.get() != get_master_passcode():
            messagebox.showerror("Error", "Old passcode incorrect")
            return
        if not new_entry.get():
            messagebox.showwarning("Error", "New passcode cannot be empty")
            return

        with open("master.txt", "w") as file:
            file.write(new_entry.get())

        messagebox.showinfo("Success", "Passcode updated")
        win.destroy()

    win = Toplevel(window)
    win.title("Change Passcode")
    win.config(padx=20, pady=20)

    Label(win, text="Old Passcode").grid(row=0, column=0)
    old_entry = Entry(win, show="*")
    old_entry.grid(row=0, column=1)

    Label(win, text="New Passcode").grid(row=1, column=0)
    new_entry = Entry(win, show="*")
    new_entry.grid(row=1, column=1)

    Button(win, text="Update", command=save_new_passcode)\
        .grid(row=2, column=0, columnspan=2, pady=10)

# ---------------------------- VIEW / EDIT / DELETE ------------------------------- #
def view_pass():
    if simpledialog.askstring("Authentication", "Enter master passcode:", show="*") != get_master_passcode():
        messagebox.showerror("Access Denied", "Wrong passcode")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No passwords saved")
        return

    view_win = Toplevel(window)
    view_win.title("Stored Passwords")
    view_win.config(padx=20, pady=20)

    listbox = Listbox(view_win, width=40)
    listbox.grid(row=0, column=0, columnspan=3, pady=10)

    for site in sorted(data.keys()):
        listbox.insert(END, site)

    def selected_site():
        try:
            return listbox.get(listbox.curselection())
        except:
            messagebox.showwarning("Select", "Select an entry first")
            return None

    def copy_email():
        site = selected_site()
        if site:
            window.clipboard_clear()
            window.clipboard_append(data[site]["email"])
            window.update()
            messagebox.showinfo("Copied", "Email copied")

    def copy_password():
        site = selected_site()
        if site:
            window.clipboard_clear()
            window.clipboard_append(data[site]["password"])
            window.update()
            messagebox.showinfo("Copied", "Password copied")

    def delete_entry():
        site = selected_site()
        if site and messagebox.askyesno("Delete", f"Delete {site}?"):
            del data[site]
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            listbox.delete(listbox.curselection())

    def edit_entry():
        site = selected_site()
        if not site:
            return

        edit_win = Toplevel(view_win)
        edit_win.title(f"Edit {site}")
        edit_win.config(padx=20, pady=20)

        Label(edit_win, text="Email").grid(row=0, column=0)
        email_e = Entry(edit_win, width=30)
        email_e.insert(0, data[site]["email"])
        email_e.grid(row=0, column=1)

        Label(edit_win, text="Password").grid(row=1, column=0)
        pass_e = Entry(edit_win, width=30)
        pass_e.insert(0, data[site]["password"])
        pass_e.grid(row=1, column=1)

        def save_edit():
            data[site]["email"] = email_e.get()
            data[site]["password"] = pass_e.get()
            with open("data.json", "w") as file:
                json.dump(data, file, indent=4)
            messagebox.showinfo("Updated", "Details updated")
            edit_win.destroy()

        Button(edit_win, text="Save", command=save_edit)\
            .grid(row=2, column=0, columnspan=2, pady=10)

    Button(view_win, text="Copy Email", command=copy_email).grid(row=1, column=0)
    Button(view_win, text="Copy Password", command=copy_password).grid(row=1, column=1)
    Button(view_win, text="Edit", command=edit_entry).grid(row=2, column=0)
    Button(view_win, text="Delete", command=delete_entry).grid(row=2, column=1)
    Button(view_win, text="Change Passcode", command=change_passcode_window)\
        .grid(row=3, column=0, columnspan=2, pady=10)

# ---------------------------- SAVE PASSWORD ------------------------------- #
def password_save():
    if not website.get() or not password.get():
        messagebox.showwarning("Error", "Fill all fields")
        return

    new_data = {
        website.get(): {
            "email": username.get(),
            "password": password.get()
        }
    }

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {}

    data.update(new_data)

    with open("data.json", "w") as file:
        json.dump(data, file, indent=4)

    messagebox.showinfo("Success", "Password saved")

    website.delete(0, END)
    password.delete(0, END)
    website.focus()
    generate_button.config(state="normal")

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file=resource_path("logo.png"))
canvas.create_image(100, 100, image=img)
canvas.grid(column=0, row=0, columnspan=3, pady=(0, 20))

Label(text="Website:", font=(FONT_NAME, 15, "bold")).grid(column=0, row=1, sticky="e")
Label(text="Email:", font=(FONT_NAME, 15, "bold")).grid(column=0, row=2, sticky="e")
Label(text="Password:", font=(FONT_NAME, 15, "bold")).grid(column=0, row=3, sticky="e")

website = Entry(width=35)
website.grid(column=1, row=1, columnspan=2, sticky="w")
website.focus()

username = Entry(width=35)
username.insert(0, "sample@gmail.com")
username.grid(column=1, row=2, columnspan=2, sticky="w")

password = Entry(width=21)
password.grid(column=1, row=3, sticky="w")

generate_button = Button(text="Generate Password", command=generate_password)
generate_button.grid(column=2, row=3)

Button(text="Add", width=36, command=password_save)\
    .grid(column=1, row=4, columnspan=2, pady=10)

Button(text="View Passwords", width=36, command=view_pass)\
    .grid(column=1, row=5, columnspan=2)

window.mainloop()
