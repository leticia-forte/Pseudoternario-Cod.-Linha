import tkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import socket

import customtkinter

def stringToBinary(texto):
    return ' '.join(format(ord(char), '08b') for char in texto)

def beTheClient():
    beTheClient_button.configure(fg_color="#000000")
    beTheServer_button.configure(fg_color="#262626")
    isServer = False


def beTheServer():
    beTheClient_button.configure(fg_color="#262626")
    beTheServer_button.configure(fg_color="#000000")
    isServer = True


def setAddress():
    address = ip_entry.get()
    port = int(port_entry.get())
    print(f"{address}:{port}")


def validate_port_input(P):
    return (P.isdigit() or P == "" ) and P.__len__() < 6


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(("10.254.254.254", 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = "127.0.0.1"
    finally:
        s.close()
    return IP


def sendMessageCallback(event):
    print("Sending '%s'." % message_entry.get())


# function to add the contact
def add_contact():
    nome = name_entry.get()
    telefone = tel_entry.get()

    # Adds contact data to listbox
    contacts_listbox.insert(tkinter.END, nome + " - " + telefone)

    # Clears entries data
    name_entry.delete(0, tkinter.END)
    tel_entry.delete(0, tkinter.END)


isServer = False
address = get_ip()
port = 8080

# creates the main window
window = tkinter.Tk()
window.configure(bg="#262626")
window.title("Pseudo-Ternary AMI")

vcmd = window.register(validate_port_input)

# Creates a frame to hold the widgets
frame = tkinter.Frame(window, background="#262626")
frame.pack()

# IP/Port field
ip_label = customtkinter.CTkLabel(
    master=frame,
    text="IP:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
ip_label.grid(row=0, column=0, padx=7)
ip_entry = customtkinter.CTkEntry(
    master=frame,
    text_color="white",
    border_width=2,
    border_color="#d3d3d3",
    bg_color="#262626",
    fg_color="#262626",
    corner_radius=5,
)
ip_entry.grid(row=0, column=1, padx=7)
ip_entry.insert(0, address)

port_label = customtkinter.CTkLabel(
    master=frame,
    text="Port:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
port_label.grid(row=1, column=0, padx=7)
port_entry = customtkinter.CTkEntry(
    master=frame,
    text_color="white",
    border_width=2,
    border_color="#d3d3d3",
    bg_color="#262626",
    fg_color="#262626",
    corner_radius=5,
    validate="key",
    validatecommand=(vcmd, "%P"),
)
port_entry.grid(row=1, column=1, padx=7)
port_entry.insert(0, port.__str__())

# Button to set the server address in Client mode #
# or the server host in Server mode               #
setAddress_button = customtkinter.CTkButton(
    master=frame,
    command=setAddress,
    text="Set Address",
    text_color="white",
    hover=True,
    hover_color="black",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
setAddress_button.grid(row=2, column=0, columnspan=2)

# Message field
message_label = customtkinter.CTkLabel(
    master=frame,
    text="Message:",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
message_label.grid(row=3, column=0, padx=7)
message_entry = customtkinter.CTkEntry(
    master=frame,
    text_color="white",
    border_width=2,
    border_color="#d3d3d3",
    bg_color="#262626",
    fg_color="#262626",
    corner_radius=5,
)
message_entry.grid(row=3, column=1, padx=7)
message_entry.bind("<Return>", sendMessageCallback)

# Button to send a message #
sendMessage_button = customtkinter.CTkButton(
    master=frame,
    command=setAddress,
    text="Send message",
    text_color="white",
    hover=True,
    hover_color="black",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
sendMessage_button.grid(row=4, column=0, columnspan=2)


# Creates buttons to change the state of the application #
# to Client or to Server                                 #
beTheServer_button = customtkinter.CTkButton(
    master=frame,
    command=beTheServer,
    text="Be the server",
    text_color="white",
    hover=True,
    hover_color="black",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
beTheServer_button.grid(row=5, column=0)

beTheClient_button = customtkinter.CTkButton(
    master=frame,
    command=beTheClient,
    text="Be the client",
    text_color="white",
    hover=True,
    hover_color="black",
    height=40,
    width=120,
    border_width=2,
    corner_radius=20,
    border_color="black",
    bg_color="#262626",
    fg_color="#262626",
)
beTheClient_button.grid(row=5, column=1, columnspan=2)
beTheClient_button.configure(fg_color="#000000")

#Received message field
sendedMessage_label = customtkinter.CTkLabel(
    master=frame,
    text="Received Message",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
sendedMessage_label.grid(row=0, column=3, columnspan=2)

sendedMessage = customtkinter.CTkTextbox(
    master=frame,
    width=165,
    height=50,
)
sendedMessage.insert("0.0", "No message received yet.")  # insert at line 0 character 0
sendedMessage.configure(state="disabled")
sendedMessage.grid(row=1, column=3, columnspan=2)

encryptedReceivedMessage_label = customtkinter.CTkLabel(
    master=frame,
    text="Encrypted Received Message",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
encryptedReceivedMessage_label.grid(row=2, column=3, columnspan=2)

encryptedReceivedMessage = customtkinter.CTkTextbox(
    master=frame,
    width=165,
    height=50,
)
encryptedReceivedMessage.insert("0.0", "No message received yet.")  # insert at line 0 character 0
encryptedReceivedMessage.configure(state="disabled")
encryptedReceivedMessage.grid(row=3, column=3, columnspan=2)


#Received message in binary field
receivedMessageBinary_label = customtkinter.CTkLabel(
    master=frame,
    text="Received Message Binary",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
receivedMessageBinary_label.grid(row=4, column=3, columnspan=2)

receivedMessageBinary = customtkinter.CTkTextbox(
    master=frame,
    width=165,
    height=50,
)
receivedMessageBinary.insert("0.0", "No message received yet.")  # insert at line 0 character 0
receivedMessageBinary.configure(state="disabled")
receivedMessageBinary.grid(row=5, column=3, columnspan=2)


#Sended message field
sendedMessage_label = customtkinter.CTkLabel(
    master=frame,
    text="Sended Message",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
sendedMessage_label.grid(row=0, column=6, columnspan=2, padx=5)

sendedMessage = customtkinter.CTkTextbox(
    master=frame,
    width=165,
    height=50,
)
sendedMessage.insert("0.0", "No message sended yet.")  # insert at line 0 character 0
sendedMessage.configure(state="disabled")
sendedMessage.grid(row=1, column=6, columnspan=2, padx=5)

encryptedSendedMessage_label = customtkinter.CTkLabel(
    master=frame,
    text="Encrypted Sended Message",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
encryptedSendedMessage_label.grid(row=2, column=6, columnspan=2, padx=5)

encryptedSendedMessage = customtkinter.CTkTextbox(
    master=frame,
    width=165,
    height=50,
)
encryptedSendedMessage.insert("0.0", "No message sended yet.")  # insert at line 0 character 0
encryptedSendedMessage.configure(state="disabled")
encryptedSendedMessage.grid(row=3, column=6, columnspan=2, padx=5)





#Sended message in binary field
sendedMessageBinary_label = customtkinter.CTkLabel(
    master=frame,
    text="Sended Message Binary",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
sendedMessageBinary_label.grid(row=4, column=6, columnspan=2, padx=5)

sendedMessageBinary = customtkinter.CTkTextbox(
    master=frame,
    width=165,
    height=50,
)
sendedMessageBinary.insert("0.0", "No message sended yet.")  # insert at line 0 character 0
sendedMessageBinary.configure(state="disabled")
sendedMessageBinary.grid(row=5, column=6, columnspan=2, padx=5)






#fig, ax = plt.subplots(figsize=(3,2))
#x = [1, 2, 3, 4, 5]
#y = [10, 20, 25, 30, 40]
#ax.plot(x, y, marker='o', linestyle='-')
#ax.set_title("Exemplo de Gráfico")
#ax.set_xlabel("Eixo X")
#ax.set_ylabel("Eixo Y")
#
#canvas = FigureCanvasTkAgg(fig, master=window)
#canvas_widget = canvas.get_tk_widget()
#canvas_widget.pack(expand=True)



window.mainloop()
