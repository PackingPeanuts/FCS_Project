from tkinter import *
from tkinter import messagebox


# Define Helper Functions For Operating Procedures
def check_ones_zeros(strg):
    return set(strg) <= set('01')


# Function for performing xor across two strings of 0's and 1's
def xor(a, b):
    result = []

    for i in range(1, len(b)):
        if a[i] == b[i]:
            result.append('0')
        else:
            result.append('1')
    return ''.join(result)


# Function for performing Mod2 Division
def modulo_div(divisor, dividend):

    # length of divisor and portion of dividend must match
    extract = len(divisor)
    portion = dividend[0:extract]

    # work through the division
    while extract < len(dividend):
        if portion[0] == '1':
            portion = xor(divisor, portion) + dividend[extract]
        else:
            portion = xor('0'*extract, portion) + dividend[extract]
        extract += 1

    # compute remainder
    if portion[0] == '1':
        remainder = xor(divisor, portion)
    else:
        remainder = xor('0'*extract, portion)

    return remainder


# Resets all sequence entries
def reset_sequences():
    data_sequence.set("Empty")
    gen_sequence.set("Empty")
    received_sequence.set("Empty")
    err_sequence.set("Empty")
    return


# Computes FCSBits
def generator(msg, gen_seq):

    # Calculate padding length
    n = len(gen_seq) - 1

    # Pad Message bits with Zeros before converting to binary
    padding = '0' * n
    messagep = msg + padding

    transmitted = msg + modulo_div(gen_seq, messagep)

    print("The Generated Sequence is: ")
    print(transmitted)
    return


# Define Functions for GUI Functionality
def store_data(event):
    content = data_entry.get()
    if content:
        if check_ones_zeros(content):
            data_sequence.set(content)
        else:
            print('Invalid Entry')
    return


def store_generator(event):
    content = generator_entry.get()
    if content:
        if check_ones_zeros(content):
            gen_sequence.set(content)
        else:
            print('Invalid Entry')
    return


def store_received(event):
    content = received_entry.get()
    if content:
        if check_ones_zeros(content):
            received_sequence.set(content)
        else:
            print('Invalid Entry')
    return


def store_error(event):
    content = error_entry.get()
    if content:
        if check_ones_zeros(content):
            err_sequence.set(content)
        else:
            print('Invalid Entry')
    return


def about():
    messagebox.showinfo("Program Authors",
                        "Adrian Martinez\nSimerjit Nagra\nHamed Seyedroudbari")
    return


root = Tk()

# Format Window Appearance
root.winfo_toplevel().title("FCS Project")
root.winfo_toplevel().geometry("750x500")
root.configure(bg="gray20")
root.resizable(0, 0)

# Add Menu Items
about_menu = Menu()
root.configure(menu=about_menu)
about_menu.add_command(label="About", command=about)

# Add Main Title
title_label = Label(text="ECE 562 FCS Project",
                    fg="white",
                    font="default 20 bold",
                    bg="gray30",
                    relief=GROOVE, justify=CENTER)
title_label.grid(row=0, column=0, columnspan=10, pady=20)

# Checkboxes For Choosing Which Function To Run
bGenerate = IntVar()
Checkbutton(root, text="Generator",
            variable=bGenerate,
            bg="gray").grid(row=2, column=0, sticky=W, padx=5)
bVerify = IntVar()
Checkbutton(root, text="Verify",
            variable=bVerify,
            bg="gray").grid(row=2, column=3, sticky=W, padx=5)
bReceiver = IntVar()
Checkbutton(root, text="Receiver",
            variable=bReceiver,
            bg="gray").grid(row=2, column=4, sticky=W, padx=5)

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
button1 = Button(text="Enter data bits",
                 bg="steel blue",
                 width=22)
button2 = Button(text="Enter Generator sequence",
                 bg="medium purple",
                 width=22)
button3 = Button(text="Enter Received Sequence",
                 bg="medium sea green",
                 width=22)
button4 = Button(text="Enter Error Sequence",
                 bg="pale violet red",
                 width=22)
resetBu = Button(text="Reset Parameters",
                 bg="LightSteelBlue1",
                 width=22,
                 command=reset_sequences)

button1.bind("<Button-1>", store_data)
button2.bind("<Button-1>", store_generator)
button3.bind("<Button-1>", store_received)
button4.bind("<Button-1>", store_error)

# Place Widgets In Window
button1.grid(row=3, sticky=E, pady=5, padx=5)
button2.grid(row=4, sticky=E, pady=5, padx=5)
button3.grid(row=5, sticky=E, pady=5, padx=5)
button4.grid(row=6, sticky=E, pady=5, padx=5)
resetBu.grid(row=2, column=6, pady=5, padx=5)

data_entry.grid(row=3, column=3, columnspan=2, padx=5)
generator_entry.grid(row=4, column=3, columnspan=2, padx=5)
received_entry.grid(row=5, column=3, columnspan=2, padx=5)
error_entry.grid(row=6, column=3, columnspan=2, padx=5)

data_sequence = StringVar()
gen_sequence = StringVar()
received_sequence = StringVar()
err_sequence = StringVar()

show_dat_seq = Label(root, textvariable=data_sequence, width=40)
show_gen_seq = Label(root, textvariable=gen_sequence, width=40)
show_rec_seq = Label(root, textvariable=received_sequence, width=40)
show_err_seq = Label(root, textvariable=err_sequence, width=40)
show_dat_seq.grid(row=3,column=6, sticky=E, padx=15)
show_gen_seq.grid(row=4,column=6, sticky=E, padx=15)
show_rec_seq.grid(row=5,column=6, sticky=E, padx=15)
show_err_seq.grid(row=6,column=6, sticky=E, padx=15)
data_sequence.set("Empty")
gen_sequence.set("Empty")
received_sequence.set("Empty")
err_sequence.set("Empty")


generator("1101101", "10101")

# Run Main Loop
root.mainloop()
