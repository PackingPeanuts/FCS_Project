import tkinter as tk
from tkinter import messagebox


# Logic implementation starts here
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
            term.configure(state="normal", fg="red")
            term.insert('end', "\nError Occurred\nIncorrect number of bits were received\n")
            term.see("end")
            term.configure(state="disabled")
        else:
            check = (set(modulo_div(gen_seq, rx_seq)) == set('0'))
            if check:
                term.configure(state="normal", fg="green")
                term.insert('end', "\nI was unable to detect error in the received Frame\n")
                term.see("end")
                term.configure(state="disabled")
            else:
                term.configure(state="normal", fg="red")
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


# code for GUI starts here
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
        self.about_menu = tk.Menu()
        self.configure(menu=self.about_menu)
        self.about_menu.add_command(label="About", command=about)

        # Define Container
        self.container = tk.Frame(self)
        self.container.grid(row=0, sticky="nsew")
        self.container.grid_rowconfigure(0, weight=1)

        self.frames = {}

        self.frame = MainPage(self.container, self)

        self.frames[MainPage] = self.frame

        self.frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainPage)

    def show_frame(self, cont):
        self.frame = self.frames[cont]
        self.frame.tkraise()


# Define Fonts to use throughout frames
LARGE_FONT = ("Default", 20, "bold")
OUTPUT_FONT = ("Default", 10)


# Default Program Frame
class MainPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent, bg="gray20")
        self.pack(fill="both", expand="true")
        self.grid_rowconfigure(1, minsize=10)
        self.grid_rowconfigure(4, minsize=10)
        self.grid_rowconfigure(6, minsize=10)
        self.title_label = tk.Label(self, text="ECE 562 FCS Project", fg="white", bg="gray30",
                                    font=LARGE_FONT, relief="groove", bd=2, justify="center")
        self.title_label.grid(row=0, column=0, columnspan=10, pady=20, padx=225)

        self.output_terminal = tk.Text(self, fg="white", bg="black", font=OUTPUT_FONT,
                                       bd=2, height=8, width=55, wrap="word")
        self.output_terminal.grid(row=11, column=0, columnspan=10, rowspan=4, pady=10, padx=20)
        self.output_terminal.insert('end', "Hello Professor Zahid. Welcome to FCS project!\n")
        self.output_terminal.see("end")
        self.output_terminal.config(state="disabled")

        self.width_entry_slot = 30
        self.width_entry_buttons = 22
        self.pady_entry_buttons = 5
        self.padx_entry_buttons = 5

        self.width_command_buttons = 22
        self.pady_command_buttons = 10
        self.padx_command_buttons = 10

        self.width_seq_label = 20

        # Define Entries for Obtaining bit Sequences
        self.message_entry = tk.Entry(self, width=self.width_entry_slot)
        self.gensequ_entry = tk.Entry(self, width=self.width_entry_slot)
        self.receive_entry = tk.Entry(self, width=self.width_entry_slot)
        self.alterer_entry = tk.Entry(self, width=self.width_entry_slot)

        self.message_entry.bind("<Return>", lambda x: store_entry(self.msg_seq, self.message_entry, 0))
        self.gensequ_entry.bind("<Return>", lambda x: store_entry(self.gsq_seq, self.gensequ_entry, 1))
        self.receive_entry.bind("<Return>", lambda x: store_entry(self.rx_seq, self.receive_entry, 0))
        self.alterer_entry.bind("<Return>", lambda x: store_entry(self.ex_seq, self.alterer_entry, 0))

        self.message_entry.grid(row=2, column=3, columnspan=2)
        self.gensequ_entry.grid(row=3, column=3, columnspan=2)
        self.receive_entry.grid(row=8, column=3, columnspan=2)
        self.alterer_entry.grid(row=9, column=3, columnspan=2)

        # Define Storage Buttons for Obtaining bit Sequences
        self.message_button = tk.Button(self, text="Store Message Bits",
                                        width=self.width_entry_buttons,
                                        bg="steel blue")
        self.message_button.bind("<ButtonRelease-1>", lambda x: store_entry(self.msg_seq, self.message_entry, 0))
        self.gensequ_button = tk.Button(self, text="Store Generator Bits",
                                        width=self.width_entry_buttons,
                                        bg="medium purple")
        self.gensequ_button.bind("<ButtonRelease-1>", lambda x: store_entry(self.gsq_seq, self.gensequ_entry, 1))
        self.receive_button = tk.Button(self, text="Store Received Bits",
                                        width=self.width_entry_buttons,
                                        bg="medium purple")
        self.receive_button.bind("<ButtonRelease-1>", lambda x: store_entry(self.rx_seq, self.receive_entry, 0))
        self.alterex_button = tk.Button(self, text="Store Alter Sequence",
                                        width=self.width_entry_buttons,
                                        bg="medium purple")
        self.alterex_button.bind("<ButtonRelease-1>", lambda x: store_entry(self.ex_seq, self.alterer_entry, 0))
        self.clearal_button = tk.Button(self, text="Clear All Stored Sequences",
                                        width=self.width_entry_buttons,
                                        bg="tomato")
        self.clearal_button.bind("<ButtonRelease-1>", lambda x: self.reset_seqs())

        self.message_button.grid(row=2, column=1, pady=self.pady_entry_buttons, padx=self.padx_entry_buttons)
        self.gensequ_button.grid(row=3, column=1, pady=self.pady_entry_buttons, padx=self.padx_entry_buttons)
        self.receive_button.grid(row=8, column=1, pady=self.pady_entry_buttons, padx=self.padx_entry_buttons)
        self.alterex_button.grid(row=9, column=1, pady=self.pady_entry_buttons, padx=self.padx_entry_buttons)
        self.clearal_button.grid(row=7, column=1, pady=self.pady_entry_buttons, padx=self.padx_entry_buttons)

        # Define Command Buttons to Execute Programs
        self.generat_button = tk.Button(self, text="Generate Tx",
                                        width=self.width_command_buttons,
                                        bg="medium sea green")
        self.verifie_button = tk.Button(self, text="Verify Tx",
                                        width=self.width_command_buttons,
                                        bg="pale violet red")
        self.receive_button = tk.Button(self, text="Receiver",
                                        width=self.width_command_buttons,
                                        bg="light steel blue3")
        self.alterer_button = tk.Button(self, text="Alter",
                                        width=self.width_command_buttons,
                                        bg="indian red2")

        self.generat_button.bind("<ButtonRelease-1>", lambda x: generator(self.msg_seq.get(), self.gsq_seq.get(),
                                                                          self.tx_seq, self.output_terminal))
        self.verifie_button.bind("<ButtonRelease-1>", lambda x: verifier(self.tx_seq.get(), self.gsq_seq.get(),
                                                                         self.output_terminal))
        self.receive_button.bind("<ButtonRelease-1>", lambda x: receiver(len(self.tx_seq.get()), self.rx_seq.get(),
                                                                         self.gsq_seq.get(), self.output_terminal))
        self.alterer_button.bind("<ButtonRelease-1>", lambda x: alter(self.gsq_seq.get(), self.tx_seq.get(),
                                                                      self.ex_seq.get(), self.output_terminal))

        self.generat_button.grid(row=5, column=1, pady=self.pady_command_buttons, padx=self.padx_command_buttons)
        self.verifie_button.grid(row=5, column=3, pady=self.pady_command_buttons, padx=self.padx_command_buttons)
        self.receive_button.grid(row=5, column=5, pady=self.pady_command_buttons, padx=self.padx_command_buttons)
        self.alterer_button.grid(row=5, column=7, pady=self.pady_command_buttons, padx=self.padx_command_buttons)

        # Create containers for the binary sequences
        self.tx_seq = tk.StringVar()
        self.rx_seq = tk.StringVar()
        self.ex_seq = tk.StringVar()
        self.msg_seq = tk.StringVar()
        self.gsq_seq = tk.StringVar()

        # Create labels for displaying the sequences
        self.tx_label = tk.Label(self, textvariable=self.tx_seq, width=self.width_seq_label,
                                 bg="slategray3", relief="groove")
        self.rx_label = tk.Label(self, textvariable=self.rx_seq, width=self.width_seq_label,
                                 bg="slategray3", relief="groove")
        self.ex_label = tk.Label(self, textvariable=self.ex_seq, width=self.width_seq_label,
                                 bg="slategray3", relief="groove")
        self.msg_label = tk.Label(self, textvariable=self.msg_seq, width=self.width_seq_label,
                                  bg="slategray2", relief="groove")
        self.gsq_label = tk.Label(self, textvariable=self.gsq_seq, width=self.width_seq_label,
                                  bg="slategray2", relief="groove")

        self.msg_id = tk.Label(self, text="Stored Message:", width=self.width_seq_label,
                               bg="mediumpurple4", fg="white")
        self.gsq_id = tk.Label(self, text="Stored Generator:", width=self.width_seq_label,
                               bg="mediumpurple4", fg="white")
        self.tx_id = tk.Label(self, text="Tx Sequence:", width=self.width_seq_label,
                              bg="mediumpurple4", fg="white")
        self.rx_id = tk.Label(self, text="Rx Sequence:", width=self.width_seq_label,
                              bg="mediumpurple4", fg="white")
        self.ex_id = tk.Label(self, text="Ex Sequence:", width=self.width_seq_label,
                              bg="mediumpurple4", fg="white")

        self.tx_id.grid(row=7, column=5, sticky="e", pady=self.pady_entry_buttons)
        self.tx_label.grid(row=7, column=7, sticky="w", pady=self.padx_entry_buttons)
        self.rx_id.grid(row=8, column=5, sticky="e", pady=self.pady_entry_buttons)
        self.rx_label.grid(row=8, column=7, sticky="w", pady=self.pady_entry_buttons)
        self.ex_id.grid(row=9, column=5, sticky="e", pady=self.pady_entry_buttons)
        self.ex_label.grid(row=9, column=7, sticky="w", pady=self.pady_entry_buttons)

        self.msg_id.grid(row=2, column=5, sticky="e")
        self.msg_label.grid(row=2, column=7, columnspan=2, sticky="w")
        self.gsq_id.grid(row=3, column=5, sticky="e")
        self.gsq_label.grid(row=3, column=7, columnspan=2, sticky="w")

    def reset_seqs(self):
        self.tx_seq.set("")
        self.rx_seq.set("")
        self.ex_seq.set("")
        self.msg_seq.set("")
        self.gsq_seq.set("")
# code for GUI ends here


# execute program:
app = FCSProg()
app.mainloop()
