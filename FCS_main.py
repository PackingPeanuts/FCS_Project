from tkinter import *
from tkinter import messagebox


# define main variables for performing FCS procedures


# Define Functions for GUI Functionality
def store_data(event):
    if data_entry.get():
        print(data_entry.get())
    return


def store_generator(event):
    if generator_entry.get():
        print(generator_entry.get())
    return


def store_received(event):
    if received_entry.get():
        print(received_entry.get())
    return


def store_error(event):
    if error_entry.get():
        print(error_entry.get())
    return


def about():
    messagebox.showinfo("Program Authors",
                        "Adrian Martinez\nSimerjit Nagra\nHamed Seyedroudbari")
    return




root = Tk()

# Format Window Appearance
root.winfo_toplevel().title("FCS Project")
root.winfo_toplevel().geometry("600x500")
root.configure(bg="gray20")
root.resizable(0, 0)

# Add Menu Items
about_menu = Menu()
root.configure(menu=about_menu)
about_menu.add_command(label="About", command=about)

# Add Main Title
title_label = Label(text="ECE 562 FCS Project", fg="white", font="default 20 bold", bg="gray30")
title_label.grid(row=0, column=4, columnspan=5, sticky=W+E+N+S, pady=20)

# Entry Widgets For Entering Sequence Data
data_entry = Entry(width=40)
generator_entry = Entry(width=40)
received_entry = Entry(width=40)
error_entry = Entry(width=40)

data_entry.bind("<Return>", store_data)
generator_entry.bind("<Return>", store_generator)
received_entry.bind("<Return>", store_received)
error_entry.bind("<Return>", store_error)

# Buttons For Entering Sequence Data
button1 = Button(text="Enter data bits", bg="steel blue")
button2 = Button(text="Enter Generator sequence", bg="medium purple")
button3 = Button(text="Enter Received Sequence", bg="medium sea green")
button4 = Button(text="Enter Error Sequence", bg="pale violet red")

button1.bind("<Button-1>", store_data)
button2.bind("<Button-1>", store_generator)
button3.bind("<Button-1>", store_received)
button4.bind("<Button-1>", store_error)

button1.grid(row=3, sticky=E, pady=5, padx=2)
button2.grid(row=4, sticky=E, pady=5, padx=2)
button3.grid(row=5, sticky=E, pady=5, padx=2)
button4.grid(row=6, sticky=E, pady=5, padx=2)

data_entry.grid(row=3, column=3, columnspan=2)
generator_entry.grid(row=4, column=3, columnspan=2)
received_entry.grid(row=5, column=3, columnspan=2)
error_entry.grid(row=6, column=3, columnspan=2)

# Run Main Loop
root.mainloop()