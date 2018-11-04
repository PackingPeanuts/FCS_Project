import tkinter as tk
from tkinter import messagebox


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


def generator(msg, gen_seq, tx_seq):

    if msg and gen_seq:
        # Calculate padding length
        n = len(gen_seq) - 1

        # Pad Message bits with Zeros before converting to binary
        padding = '0' * n
        messagep = msg + padding

        transmitted = msg + modulo_div(gen_seq, messagep)
        tx_seq.set(transmitted)
    else:
        tk.messagebox.showwarning("Missing Parameter", "Please specify both a\nmessage and generator\nsequence.")
    return


def verifier(tx_seq, gen_seq):

    if tx_seq:
        # Calculate padding length
        n = len(gen_seq) - 1

        success = (set(modulo_div(gen_seq, tx_seq)) == set('0'))

        if success:
            print("All is good in the world")
        else:
            print("You have committed the ULTIMATE SIN")
    else:
        tk.messagebox.showwarning("Missing Tx", "Please generate a transmitted sequence first.")
    return


def warn_invalid_entry():
    messagebox.showwarning("Invalid Entry",
                           "Please enter a valid binary sequence")
    return


def about():
    messagebox.showinfo("Program Authors",
                        "Adrian Martinez\nSimerjit Nagra\nHamed Seyedroudbari")
    return


def store_entry(destination, entry):
    content = entry.get()
    if content:
        if check_ones_zeros(content):
            destination.set(content)
        else:
            warn_invalid_entry()
    return


# Define Fonts to use throughout frames
LARGE_FONT = ("Default", 20, "bold")


# Define GUI and Frames
class FCSProg(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Configure Window Dimensions and Visual Attributes
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="fcs_icon1.ico")
        tk.Tk.wm_title(self, "FCS Project")
        tk.Tk.wm_geometry(self, "750x500")
        self.configure(bg="gray20")
        self.rowconfigure(10, minsize=30)
        self.columnconfigure(14, minsize=30)
        self.resizable(0, 0)

        # Add Menu Items
        about_menu = tk.Menu()
        self.configure(menu=about_menu)
        about_menu.add_command(label="About", command=about)

        # Define Container
        container = tk.Frame(self)
        container.grid(row=0, sticky="nsew")
        container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        frame = MainPage(container, self)

        self.frames[MainPage] = frame

        frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


# Default Program Frame
class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="gray20")
        self.pack(fill="both", expand="true")
        title_label = tk.Label(self, text="ECE 562 FCS Project", fg="white", bg="gray30",
                               font=LARGE_FONT, relief="groove", bd=2, justify="center")
        title_label.grid(row=0, column=0, columnspan=10, pady=20, padx=225)

        width_entry_slot = 30
        width_entry_buttons = 22
        pady_entry_buttons = 5
        padx_entry_buttons = 5

        width_command_buttons = 22
        pady_command_buttons = 10
        padx_command_buttons = 10

        width_seq_label = 20

        # Define Entries for Obtaining bit Sequences
        message_entry = tk.Entry(self, width=width_entry_slot)
        gensequ_entry = tk.Entry(self, width=width_entry_slot)

        message_entry.bind("<Return>", lambda x: store_entry(msg_seq, message_entry))
        gensequ_entry.bind("<Return>", lambda x: store_entry(gsq_seq, gensequ_entry))

        message_entry.grid(row=2, column=3, columnspan=2)
        gensequ_entry.grid(row=3, column=3, columnspan=2)

        # Define Storage Buttons for Obtaining bit Sequences
        message_button = tk.Button(self, text="Message Bits",
                                   width=width_entry_buttons,
                                   bg="steel blue")
        message_button.bind("<ButtonRelease-1>", lambda x: store_entry(msg_seq, message_entry))
        gensequ_button = tk.Button(self, text="Generator Bits",
                                   width=width_entry_buttons,
                                   bg="medium purple")
        gensequ_button.bind("<ButtonRelease-1>", lambda x: store_entry(gsq_seq, gensequ_entry))


        message_button.grid(row=2, column=1, pady=pady_entry_buttons, padx=padx_entry_buttons)
        gensequ_button.grid(row=3, column=1, pady=pady_entry_buttons, padx=padx_entry_buttons)

        # Define Command Buttons to Execute Programs
        generat_button = tk.Button(self, text="Generate Tx",
                                   width=width_command_buttons,
                                   bg="medium sea green")
        verifie_button = tk.Button(self, text="Verify Tx",
                                   width=width_command_buttons,
                                   bg="pale violet red")
        receive_button = tk.Button(self, text="Receiver",
                                   width=width_command_buttons,
                                   bg="light steel blue3")
        alterer_button = tk.Button(self, text="Alter",
                                   width=width_command_buttons,
                                   bg="indian red2")

        generat_button.bind("<ButtonRelease-1>", lambda x: generator(msg_seq.get(), gsq_seq.get(), tx_seq))
        verifie_button.bind("<ButtonRelease-1>", lambda x: verifier(tx_seq.get(), gsq_seq.get()))

        generat_button.grid(row=5, column=1, pady=pady_command_buttons, padx=padx_command_buttons)
        verifie_button.grid(row=5, column=3, pady=pady_command_buttons, padx=padx_command_buttons)
        receive_button.grid(row=5, column=5, pady=pady_command_buttons, padx=padx_command_buttons)
        alterer_button.grid(row=5, column=7, pady=pady_command_buttons, padx=padx_command_buttons)

        tx_seq = tk.StringVar()
        rx_seq = tk.StringVar()
        ex_seq = tk.StringVar()

        msg_seq = tk.StringVar()
        gsq_seq = tk.StringVar()

        tx_label = tk.Label(self, textvariable=tx_seq, width=width_seq_label, bg="lavender", relief="groove")
        rx_label = tk.Label(self, textvariable=rx_seq, width=width_seq_label, bg="lavender", relief="groove")
        ex_label = tk.Label(self, textvariable=ex_seq, width=width_seq_label, bg="lavender", relief="groove")
        msg_label = tk.Label(self, textvariable=msg_seq, width=width_seq_label, bg="slategray2", relief="groove")
        gsq_label = tk.Label(self, textvariable=gsq_seq, width=width_seq_label, bg="slategray2", relief="groove")
        msg_id = tk.Label(self, text="Stored Message:", width=width_seq_label, bg="mediumpurple4")
        gsq_id = tk.Label(self, text="Stored Generator:", width=width_seq_label, bg="mediumpurple4")

        tx_label.grid(row=7, column=2, columnspan=2)
        rx_label.grid(row=7, column=5, columnspan=2)
        ex_label.grid(row=7, column=7, columnspan=2)
        msg_id.grid(row=2, column=5, sticky="e")
        msg_label.grid(row=2, column=7, columnspan=2, sticky="w")
        gsq_id.grid(row=3, column=5, sticky="e")
        gsq_label.grid(row=3, column=7, columnspan=2, sticky="w")


app = FCSProg()
app.mainloop()
