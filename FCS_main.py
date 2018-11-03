from tkinter import *


def Generator():
    print("You are a loser")
    return


def verifier():
    print("You are a winner")
    return


def toPoly():
    print("You are not nice")
    return


# create and format window
FCSProg = Tk()

FCSProg.winfo_toplevel().title("FCS Project")
FCSProg.winfo_toplevel().geometry("700x500")

topFrame = Frame(FCSProg, width=650, height=100)
topFrame.pack()
bottomFrame = Frame(FCSProg, width=650, height=350)
bottomFrame.pack(side=TOP)

titleLabel = Label(topFrame, text="ECE 562 FCS Project", fg="blue")

titleLabel.pack(fill=X)

button1 = Button(bottomFrame, text="Enter Generator Sequence", fg="blue", command=Generator)
button2 = Button(bottomFrame, text="Enter Received Sequence", fg="blue", command=verifier)
button3 = Button(bottomFrame, text="Enter Error Sequence", fg="blue", command=toPoly)

button1.pack(side=LEFT)
button2.pack(side=LEFT)
button3.pack(side=LEFT)

# run main loop
FCSProg.mainloop()