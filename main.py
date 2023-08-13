from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT = ("Arial", 10, "bold")
# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def new_password():
    password_input.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    ran_letters = [random.choice(letters) for _ in range(nr_letters)]
    ran_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    ran_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = ran_numbers + ran_letters + ran_symbols
    random.shuffle(password_list)

    password = "".join(password_list)
    password_input.insert(0, f"{password}")
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = website_input.get()
    email = email_user_input.get()
    password = password_input.get()
    new_data = {website: {"email": email, "password": password}}
    if len(website) == 0 or len(password) == 0:
        messagebox.showerror(title="Data Missing", message="You've not added a website or password.Please correct this")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
                website_input.delete(0, END)
                password_input.delete(0, END)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
                website_input.delete(0, END)
                password_input.delete(0, END)

# ---------------------------- SEARCH DETAILS ------------------------------- #


def search():
    search_input = website_input.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
            details = data[search_input]
    except FileNotFoundError:
        messagebox.showerror(title="No Passwords Stored", message=f"No data source found")
    except KeyError:
        messagebox.showerror(title="Website not found", message=f"No details for {search_input} exist.")
    else:
        messagebox.showinfo(title=f"{search_input}", message=f"Email: {details['email']}\n"
                                                             f""f"Password: {details['password']}")

# ---------------------------- UI SETUP ------------------------------- #


window = Tk()
window.title("Password Manager")
window.minsize(width=200, height=200)
window.config(pady=10, padx=10)

#logo
canvas = Canvas()
app_logo = PhotoImage(file="logo.png")
canvas.create_image(140, 150, image=app_logo)
canvas.grid(row=0, column=1)

#labels
website_label = Label(text="Website:", font=FONT)
website_label.grid(row=1, column=0)

email_user_label = Label(text="Email/Username:", font=FONT)
email_user_label.grid(row=2, column=0)

password_label = Label(text="Password:", font=FONT)
password_label.grid(row=3, column=0)



#Inputs

website_input = Entry(width=40)
website_input.grid(row=1, column=0, columnspan=2)
website_input.focus()

email_user_input = Entry(width=40)
email_user_input.grid(row=2, column=0, columnspan=2)
email_user_input.insert(0, "first.last@gmail.com")

password_input = Entry(width=40)
password_input.grid(row=3, column=0, columnspan=2)

#Buttons

password_gen_but = Button(width=17, text="Generate Password", command=new_password)
password_gen_but.grid(row=3, column=1)

search_but = Button(width=17, text="Search", command=search)
search_but.grid(row=1, column=1)

add_but = Button(width=33, text="Add", command=save)
add_but.grid(row=4, column=0,columnspan=2)


window.mainloop()