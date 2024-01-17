from tkinter import *
import random
from PIL import Image, ImageTk
import pyperclip
from tkinter import messagebox
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_generator():
    pw_entry.delete(0, END)
    password = ""
    for i in range(0, 14):
        password += chr(random.randint(33, 126))
    pw_entry.insert(0, password)
    pyperclip.copy(password)
# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_password():
    website = website_entry.get()
    email = email_entry.get()
    password = pw_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    is_ok = messagebox.askokcancel(title=website, message=f"Please Confirm Before Saving: \nEmail: {email} \nPassword: {password} \nDo you want to save?")

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        canvas.itemconfig(message_text, text="Please fill out all fields!", fill="red")
    elif is_ok:
        try:
            with open("pw_manager_v1/data.json", "r") as data_file:
                data = json.load(data_file)
                data.update(new_data)

            with open("pw_manager_v1/data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)

        except FileNotFoundError:
            with open("pw_manager_v1/data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            email_entry.delete(0, END)
            pw_entry.delete(0, END)
            canvas.itemconfig(message_text, text="Password saved!", fill="green")

# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = website_entry.get()
    try:
        with open("pw_manager_v1/data.json", "r") as data_file:
            data = json.load(data_file)
            email = data[website]["email"]
            password = data[website]["password"]
            pyperclip.copy(password)
            messagebox.showinfo(title=website, message=f"Email: {email} \nPassword: {password}")
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No Data File Found")
# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Local Password Manager")

og_lock = Image.open("pw_manager_v1/lock1.png")
resized_lock_img = og_lock.resize(size=(512, 512))

canvas = Canvas(width = 512, height=512)
background = ImageTk.PhotoImage(resized_lock_img)
canvas.create_image(256, 256, image = background)
canvas.pack()

#create labels
website_text = canvas.create_text(100, 410, text = "Website:", font=("Courier", 20, "bold"), fill="black")
email_text = canvas.create_text(100, 445, text = "Email/Username:", font=("Courier", 18, "bold"), fill="black")
pw_text = canvas.create_text(100, 480, text = "Password:", font=("Courier", 20, "bold"), fill="black")

#create entry boxes
website_entry = Entry(window, font=("Courier", 15))
canvas.create_window(300, 410, window=website_entry)
email_entry = Entry(window, font=("Courier", 15))
canvas.create_window(300, 445, window=email_entry)
pw_entry = Entry(window, font=("Courier", 15))
canvas.create_window(300, 480, window=pw_entry)

# This was a cool idea but didn't work...
button_radius = 25
button_center_x = 256
button_center_y = 217
button_left = button_center_x - button_radius
button_top = button_center_y - button_radius
button_right = button_center_x + button_radius
button_bottom = button_center_y + button_radius
submit_button = canvas.create_oval(button_left, button_top, button_right, button_bottom,fill="red", outline="white", width=4)
message_text = canvas.create_text(256, 380, text="", font=("Courier", 20, "bold"), fill="black")
canvas.tag_bind(submit_button, "<Button-1>", save_password)
canvas.tag_bind(submit_button, "<ButtonRelease-1>", lambda event: submit_button.itemconfig(submit_button, fill='white'))  

#Save Button
save_pass_button = Button(text = "Save", font=("Courier", 10, "bold"), width = 4, height = 2, command=save_password, highlightthickness=0)
save_pass_button.place(x=227, y=201)

#Search Button
search_button = Button(text = "Search", font=("Courier", 15, "bold"), width = 7, height = 2, command=find_password)
search_button.place(x=410, y=390)

#Generate Password Button
new_pass_button = Button(text = "Generate", font=("Courier", 15, "bold"), width = 7, height = 2, command=password_generator)
new_pass_button.place(x=410, y=460)





window.mainloop()