import tkinter as tk
from tkinter import messagebox


def check_ones_zeros(strg):
    return set(strg) <= set('01')


# Function for performing xor across two strings of 0's and 1's
def xor(a, b):

    if len(a) == len(b):
        result = []

        for i in range(0, len(a)):
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
            compute = xor(divisor, portion)
            portion = compute + dividend[extract]
        else:
            compute = xor('0'*len(divisor), portion)
            portion = compute + dividend[extract]
        portion = portion[1:]
        extract += 1

    # compute remainder
    if portion[0] == '1':
        remainder = xor(divisor, portion)
    else:
        remainder = xor('0'*len(divisor), portion)

    return remainder[1:]


def generator(msg, gen_seq, tx_seq, term):

    if msg and gen_seq:
        # Calculate padding length
        n = len(gen_seq) - 1

        # Pad Message bits with Zeros before converting to binary
        padding = '0' * n
        messagep = msg + padding
        fcs_bits = modulo_div(gen_seq, messagep)

        transmitted = msg + fcs_bits
        tx_seq.set(transmitted)
        term.configure(state="normal")
        term.insert('end', "\nFrom %s and %s, the FCS bits %s were generated\n" % (msg, gen_seq, fcs_bits))
        term.insert('end', "\nThe transmitted sequence is %s\n" % transmitted)
        term.see("end")
        term.configure(state="disabled")
    else:
        tk.messagebox.showwarning("Missing Parameter", "Please specify both a\nmessage and generator\nsequence.")
    return


def verifier(tx_seq, gen_seq, term):

    if tx_seq:

        success = (set(modulo_div(gen_seq, tx_seq)) <= set('0'))

        if success:
            term.configure(state="normal", fg="green")
            term.insert('end', "\nNo Error detected in received sequence\n")
            term.see("end")
            term.configure(state="disabled")
        else:
            term.configure(state="normal", fg="red")
            term.insert('end', "Error detected in received sequence\n")
            term.see("end")
            term.configure(state="disabled")

    else:
        tk.messagebox.showwarning("Missing Tx", "Please generate a transmitted sequence first.")
    return


def receiver(size_of_tx, rx_seq, gen_seq, term):
    if rx_seq and size_of_tx:
        if size_of_tx != len(rx_seq):
            term.configure(state="normal")
            term.insert('end', "\nError Occurred\nIncorrect number of bits were received\n")
            term.see("end")
            term.configure(state="disabled")
        else:
            check = (set(modulo_div(gen_seq, rx_seq)) == set('0'))
            if check:
                term.configure(state="normal")
                term.insert('end', "\nI was unable to detect error in the received Frame\n")
                term.see("end")
                term.configure(state="disabled")
            else:
                term.configure(state="normal")
                term.insert('end', "\nI have detected error in this frame\n")
                term.see("end")
                term.configure(state="disabled")
    else:
        tk.messagebox.showwarning("Missing Rx", "Please Specify a received sequence first.")

    return


def alter(gen, trans, error_seq, term):

    if not trans:
        tk.messagebox.showwarning("Missing Tx", "Please generate a transmitted sequence first.")
    elif not error_seq:
        tk.messagebox.showwarning("Missing Ex", "Enter your Error Sequence!")
    else:
        error_length = len(error_seq)
        trans_length = len(trans)
        gen_length = len(gen)
        flag = 0
        while flag == 0:
            if trans_length == error_length:
                flag = 1
            else:
                tk.messagebox.showwarning("Length Error!", "Enter an Error Sequence with length %d" % trans_length)
                return

        received_sequence = xor(trans, error_seq)
        term.configure(state="normal")
        term.insert('end', "\nThis error sequence produces the received sequence %s\n" % received_sequence)
        term.see("end")
        term.configure(state="disabled")

        remainder = modulo_div(gen, received_sequence)

        term.configure(state="normal")
        term.insert('end', "\nThe remainder obtained is %s\n" % remainder)
        term.see("end")
        term.configure(state="disabled")

        if remainder == '0'*(gen_length-1):
            term.configure(state="normal", fg="green")
            term.insert('end', "\nNo error detected in received sequence\n")
            term.see("end")
            term.configure(state="disabled")
        else:
            term.configure(state="normal", fg="red")
            term.insert('end', "\nError detected in received sequence\n")
            term.see("end")
            term.configure(state="disabled")
    return


def warn_invalid_entry():
    messagebox.showwarning("Invalid Entry",
                           "Please enter a valid binary sequence")
    return


def about():
    messagebox.showinfo("Program Authors",
                        "Adrian Martinez\nSimerjit Nagra\nHamed Seyedroudbari")
    return


def store_entry(destination, entry, remove_lead_zeros):
    content = entry.get()
    if remove_lead_zeros:
        content = content.lstrip("0")
    if content:
        if check_ones_zeros(content):
            destination.set(content)
        else:
            warn_invalid_entry()
    return


# Define Fonts to use throughout frames
LARGE_FONT = ("Default", 20, "bold")
OUTPUT_FONT = ("Default", 10)


# Define GUI and Frames
class FCSProg(tk.Tk):

    def __init__(self, *args, **kwargs):

        # Configure Window Dimensions and Visual Attributes
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="fcs_icon1.ico")
        tk.Tk.wm_title(self, "FCS Project")
        tk.Tk.wm_geometry(self, "740x500")
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
        self.grid_rowconfigure(1, minsize=10)
        self.grid_rowconfigure(4, minsize=10)
        self.grid_rowconfigure(6, minsize=10)
        title_label = tk.Label(self, text="ECE 562 FCS Project", fg="white", bg="gray30",
                               font=LARGE_FONT, relief="groove", bd=2, justify="center")
        title_label.grid(row=0, column=0, columnspan=10, pady=20, padx=225)

        output_terminal = tk.Text(self, fg="white", bg="black", font=OUTPUT_FONT,
                                  bd=2, height=8, width=55, wrap="word")
        output_terminal.grid(row=11, column=0, columnspan=10, rowspan=4, pady=10, padx=20)
        output_terminal.insert('end', "Hello Professor Zahid. Welcome to FCS project!\n")
        output_terminal.see("end")
        output_terminal.config(state="disabled")

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
        receive_entry = tk.Entry(self, width=width_entry_slot)
        alterer_entry = tk.Entry(self, width=width_entry_slot)

        message_entry.bind("<Return>", lambda x: store_entry(msg_seq, message_entry, 0))
        gensequ_entry.bind("<Return>", lambda x: store_entry(gsq_seq, gensequ_entry, 1))
        receive_entry.bind("<Return>", lambda x: store_entry(rx_seq, receive_entry, 0))
        alterer_entry.bind("<Return>", lambda x: store_entry(ex_seq, alterer_entry, 0))

        message_entry.grid(row=2, column=3, columnspan=2)
        gensequ_entry.grid(row=3, column=3, columnspan=2)
        receive_entry.grid(row=8, column=3, columnspan=2)
        alterer_entry.grid(row=9, column=3, columnspan=2)

        # Define Storage Buttons for Obtaining bit Sequences
        message_button = tk.Button(self, text="Store Message Bits",
                                   width=width_entry_buttons,
                                   bg="steel blue")
        message_button.bind("<ButtonRelease-1>", lambda x: store_entry(msg_seq, message_entry, 0))
        gensequ_button = tk.Button(self, text="Store Generator Bits",
                                   width=width_entry_buttons,
                                   bg="medium purple")
        gensequ_button.bind("<ButtonRelease-1>", lambda x: store_entry(gsq_seq, gensequ_entry, 1))
        receive_button = tk.Button(self, text="Store Received Bits",
                                   width=width_entry_buttons,
                                   bg="medium purple")
        receive_button.bind("<ButtonRelease-1>", lambda x: store_entry(rx_seq, receive_entry, 0))
        alterex_button = tk.Button(self, text="Store Alter Sequence",
                                   width=width_entry_buttons,
                                   bg="medium purple")
        alterex_button.bind("<ButtonRelease-1>", lambda x: store_entry(ex_seq, alterer_entry, 0))

        message_button.grid(row=2, column=1, pady=pady_entry_buttons, padx=padx_entry_buttons)
        gensequ_button.grid(row=3, column=1, pady=pady_entry_buttons, padx=padx_entry_buttons)
        receive_button.grid(row=8, column=1, pady=pady_entry_buttons, padx=padx_entry_buttons)
        alterex_button.grid(row=9, column=1, pady=pady_entry_buttons, padx=padx_entry_buttons)

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

        generat_button.bind("<ButtonRelease-1>", lambda x: generator(msg_seq.get(), gsq_seq.get(),
                                                                     tx_seq, output_terminal))
        verifie_button.bind("<ButtonRelease-1>", lambda x: verifier(tx_seq.get(), gsq_seq.get(),
                                                                    output_terminal))
        receive_button.bind("<ButtonRelease-1>", lambda x: receiver(len(tx_seq.get()), rx_seq.get(),
                                                                    gsq_seq.get(), output_terminal))
        alterer_button.bind("<ButtonRelease-1>", lambda x: alter(gsq_seq.get(), tx_seq.get(),
                                                                 ex_seq.get(), output_terminal))

        generat_button.grid(row=5, column=1, pady=pady_command_buttons, padx=padx_command_buttons)
        verifie_button.grid(row=5, column=3, pady=pady_command_buttons, padx=padx_command_buttons)
        receive_button.grid(row=5, column=5, pady=pady_command_buttons, padx=padx_command_buttons)
        alterer_button.grid(row=5, column=7, pady=pady_command_buttons, padx=padx_command_buttons)

        # Create containers for the binary sequences
        tx_seq = tk.StringVar()
        rx_seq = tk.StringVar()
        ex_seq = tk.StringVar()
        msg_seq = tk.StringVar()
        gsq_seq = tk.StringVar()

        # Create labels for displaying the sequences
        tx_label = tk.Label(self, textvariable=tx_seq, width=width_seq_label, bg="slategray3", relief="groove")
        rx_label = tk.Label(self, textvariable=rx_seq, width=width_seq_label, bg="slategray3", relief="groove")
        ex_label = tk.Label(self, textvariable=ex_seq, width=width_seq_label, bg="slategray3", relief="groove")
        msg_label = tk.Label(self, textvariable=msg_seq, width=width_seq_label, bg="slategray2", relief="groove")
        gsq_label = tk.Label(self, textvariable=gsq_seq, width=width_seq_label, bg="slategray2", relief="groove")

        msg_id = tk.Label(self, text="Stored Message:", width=width_seq_label, bg="mediumpurple4", fg="white")
        gsq_id = tk.Label(self, text="Stored Generator:", width=width_seq_label, bg="mediumpurple4", fg="white")
        tx_id = tk.Label(self, text="Tx Sequence:", width=width_seq_label, bg="mediumpurple4", fg="white")
        rx_id = tk.Label(self, text="Rx Sequence:", width=width_seq_label, bg="mediumpurple4", fg="white")
        ex_id = tk.Label(self, text="Ex Sequence:", width=width_seq_label, bg="mediumpurple4", fg="white")

        tx_id.grid(row=7, column=5, sticky="e", pady=pady_entry_buttons)
        tx_label.grid(row=7, column=7, sticky="w", pady=padx_entry_buttons)
        rx_id.grid(row=8, column=5, sticky="e", pady=pady_entry_buttons)
        rx_label.grid(row=8, column=7, sticky="w", pady=pady_entry_buttons)
        ex_id.grid(row=9, column=5, sticky="e", pady=pady_entry_buttons)
        ex_label.grid(row=9, column=7, sticky="w", pady=pady_entry_buttons)

        msg_id.grid(row=2, column=5, sticky="e")
        msg_label.grid(row=2, column=7, columnspan=2, sticky="w")
        gsq_id.grid(row=3, column=5, sticky="e")
        gsq_label.grid(row=3, column=7, columnspan=2, sticky="w")


app = FCSProg()
app.mainloop()
