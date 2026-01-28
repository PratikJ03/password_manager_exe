import os
import sys
from tkinter import *
from tkinter import messagebox
from tkinter import simpledialog
import random
import json

FONT_NAME = "Courier"
MASTER_PASSCODE="1234"

if not os.path.exists("master.txt"):
    with open("master.txt", "w") as file:
        file.write(MASTER_PASSCODE)

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)



# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_main=[]
    pass_word=[]
    pass_numbers=[]
    pass_symbols=[]
    pass_word=[random.choice(letters) for _ in range(nr_letters)]
    pass_numbers=[random.choice(symbols) for _ in range(nr_symbols)]
    pass_symbols=[random.choice(numbers) for _ in range(nr_numbers)]
    password_main=pass_word+pass_numbers+pass_symbols
    random.shuffle(password_main)
    pass1=''.join(password_main)

    #display password
    password.delete(0, END)
    password.insert(0,pass1)

    #copy password to clipboard of the pc
    window.clipboard_clear()
    window.clipboard_append(pass1)
    window.update()

    #disable button after generating
    generate_button.config(state="disabled")

# ---------------------------- VIEW PASSWORD ------------------------------- #
def get_master_passcode():
    with open("master.txt", "r") as file:
        return file.read()

def change_passcode_window():
    def save_new_passcode():
        old = old_entry.get()
        new = new_entry.get()

        if old != get_master_passcode():
            messagebox.showerror("Error", "Old passcode is incorrect")
            return

        if new == "":
            messagebox.showwarning("Error", "New passcode cannot be empty")
            return

        with open("master.txt", "w") as file:
            file.write(new)

        messagebox.showinfo("Success", "Passcode updated successfully")
        change_window.destroy()

    change_window = Toplevel(window)
    change_window.title("Change Passcode")
    change_window.config(padx=20, pady=20)

    Label(change_window, text="Old Passcode").grid(row=0, column=0)
    old_entry = Entry(change_window, show="*")
    old_entry.grid(row=0, column=1)

    Label(change_window, text="New Passcode").grid(row=1, column=0)
    new_entry = Entry(change_window, show="*")
    new_entry.grid(row=1, column=1)

    Button(change_window, text="Update", command=save_new_passcode)\
        .grid(row=2, column=0, columnspan=2, pady=10)


def view_pass():
    passcode = simpledialog.askstring(
        title="Authentication",
        prompt="Enter master passcode:",
        show="*"
    )

    if passcode != get_master_passcode():
        messagebox.showerror("Access Denied", "Wrong passcode")
        return

    try:
        with open("data.json", "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No passwords stored yet")
        return

    # 🔓 VIEW WINDOW
    view_window = Toplevel(window)
    view_window.title("Stored Passwords")
    view_window.config(padx=20, pady=20)

    text = Text(view_window, width=50, height=15)
    text.grid(row=0, column=0, columnspan=2)
    text.config(state="normal")

    for site, details in sorted(data.items()):
        text.insert(END, f"{site}\n")
        text.insert(END, f"  Email: {details['email']}\n")
        text.insert(END, f"  Password: {details['password']}\n\n")

    text.config(state="disabled")  # read-only

    # 🔑 CHANGE PASSCODE BUTTON
    Button(
        view_window,
        text="Change Passcode",
        command=change_passcode_window
    ).grid(row=1, column=0, columnspan=2, pady=10)



# ---------------------------- SAVE PASSWORD ------------------------------- #
def password_save():
    website_data=website.get()
    email_data=username.get()
    password_data=password.get()

    if website_data=="" or email_data=="" or password_data=="":
        messagebox.showwarning(title="Error", message="Please fill all fields")
        return
    is_ok=messagebox.askokcancel(title=website_data,message=f"These are the details:\nWebsite:{website_data}\nEmail:{email_data}\nPassword:{password_data}\nIs it ok to save")
    if is_ok:
        new_data = {
            website_data: {
                "email": email_data,
                "password": password_data
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
    messagebox.showinfo(title="Success", message="Password saved")


    website.delete(0, END)
    password.delete(0, END)
    website.focus()

    #renable generate button
    generate_button.config(state="normal")


# ---------------------------- UI SETUP ------------------------------- #


window= Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# LOGO
canvas = Canvas(width=200, height=200, highlightthickness=0)
img = PhotoImage(file=resource_path("logo.png"))
canvas.create_image(100, 100, image=img)
canvas.grid(column=0, row=0, columnspan=3, pady=(0, 20))  # 👈 FIX HERE

# LABELS
web = Label(text="Website:", font=(FONT_NAME, 15, "bold"))
web.grid(column=0, row=1, sticky="e")

Email = Label(text="Email:", font=(FONT_NAME, 15, "bold"))
Email.grid(column=0, row=2, sticky="e")

password1 = Label(text="Password:", font=(FONT_NAME, 15, "bold"))
password1.grid(column=0, row=3, sticky="e")

# ENTRIES
website = Entry(width=35)
website.grid(column=1, row=1, columnspan=2, sticky="w")
website.focus() #make it default value when launching the app to focus on

username = Entry(width=35)
username.insert(0, "sample@gmail.com")
username.grid(column=1, row=2, columnspan=2, sticky="w")

password = Entry(width=21)
password.grid(column=1, row=3, sticky="w")

# BUTTONS
generate_button = Button(text="Generate Password", width=15,command=generate_password)
generate_button.grid(column=2, row=3, sticky="w", padx=5)

add_button = Button(text="Add", width=36, command=password_save)
add_button.grid(column=1, row=4, columnspan=2, sticky="we", pady=10)

view= Button(text="View Password",width=40,command=view_pass)
view.grid(column=1, row=5, columnspan=2, sticky="w")

window.mainloop()

