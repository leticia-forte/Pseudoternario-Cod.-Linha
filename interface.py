import socket
import threading
import tkinter

import customtkinter
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def setupServer(host="0.0.0.0", port=8080):
    global sock
    global client
    data_payload = 2048  # The maximum amount of data to be received at once
    # Create a TCP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Enable reuse address/port
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Bind the socket to the port
    server_address = (host, port)
    print("Starting up echo server  on %s port %s" % server_address)
    # Set socket timeout
    sock.settimeout(5)
    sock.bind(server_address)
    # Listen to clients, argument specifies the max no. of queued connections
    sock.listen(5)
    clients = []
    global shutdownApp
    while not shutdownApp:
        print("Waiting to receive message from client")
        try:
            client, address = sock.accept()
            clients.append(client)
        except socket.timeout:
            pass
        for client in clients:
            data = client.recv(data_payload)
            if data:
                onReceivedMessage(data)
        # client.send(data)


def setupClient(host="192.168.0.233", port=8080):
    global sock
    global client
    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Connect the socket to the server
    server_address = (host, port)
    print("Connecting to %s port %s" % server_address)
    sock.connect(server_address)
    # Receive data
    while not shutdownApp:
        try:
            data = sock.recv(1024)
            if data:
                onReceivedMessage(data)
        except socket.error as e:
            print("Socket error: %s" % str(e))
        except Exception as e:
            print("Other exception: %s" % str(e))


def onReceivedMessage(message):
    message = message.decode('utf-8')
    createGraph(graphFrame, message, 0, 0)

    print("received", message)
    binaryMessage = pseudoternaryToBinary(message)
    print("received", binaryMessage)
    encryptedMessage = binaryToString(binaryMessage)
    print("received", encryptedMessage)
    decryptedMessage = decrypt(encryptedMessage)
    print("received", decryptedMessage)

    receivedMessageBinary.configure(state="normal")
    receivedMessageBinary.delete("0.0", "end")
    receivedMessageBinary.insert("0.0", binaryMessage)
    receivedMessageBinary.configure(state="disabled")

    encryptedReceivedMessage.configure(state="normal")
    encryptedReceivedMessage.delete("0.0", "end")
    encryptedReceivedMessage.insert("0.0", encryptedMessage)
    encryptedReceivedMessage.configure(state="disabled")

    receivedMessage.configure(state="normal")
    receivedMessage.delete("0.0", "end")
    receivedMessage.insert("0.0", decryptedMessage)
    receivedMessage.configure(state="disabled")


def onSendedMessage(message):
    createGraph(graphFrame, message, 0, 1)

    print("Sended", message)
    binaryMessage = pseudoternaryToBinary(message)
    print("Sended", binaryMessage)
    encryptedMessage = binaryToString(binaryMessage)
    print("Sended", encryptedMessage)
    decryptedMessage = decrypt(encryptedMessage)
    print("Sended", decryptedMessage)

    sendedMessageBinary.configure(state="normal")
    sendedMessageBinary.delete("0.0", "end")
    sendedMessageBinary.insert("0.0", binaryMessage)
    sendedMessageBinary.configure(state="disabled")

    encryptedSendedMessage.configure(state="normal")
    encryptedSendedMessage.delete("0.0", "end")
    encryptedSendedMessage.insert("0.0", encryptedMessage)
    encryptedSendedMessage.configure(state="disabled")

    sendedMessage.configure(state="normal")
    sendedMessage.delete("0.0", "end")
    sendedMessage.insert("0.0", decryptedMessage)
    sendedMessage.configure(state="disabled")


def onCloseWindow():
    global shutdownApp
    if tkinter.messagebox.askokcancel("Close", "Do you wish to close the application?"):
        shutdownApp = True
        window.destroy()


def encrypt(message_in):
    key = 5
    alphabet = ''.join(chr(i) for i in range(256))  # jeito burro mas prestavel da tabela ASCII estendida
    message = ''

    for letter in message_in:
        if letter in alphabet:
            num = alphabet.find(letter)
            num = num + key
            if num >= len(alphabet):
                num = num - len(alphabet)
            message = message + alphabet[num]
        else:
            message = message + letter

    return message


def decrypt(message_in):
    key = 5
    alphabet = ''.join(chr(i) for i in range(256)) 
    message = ''

    for letter in message_in:
        if letter in alphabet:
            num = alphabet.find(letter)
            num = num - key
            if num < 0 :
                num = num + len(alphabet)
            message = message + alphabet[num]
        else:
            message = message + letter

    return message


def binaryToPseudoTernary(binStr):
    pseudoternary = ""
    lastSign = -1
    print(binStr)

    for bit in binStr:
        if bit == "1":
            pseudoternary += "0"
        elif bit == "0":
            lastSign *= -1
            pseudoternary += "-" if lastSign == -1 else "+"
        else:
            raise ValueError("The string must be binary.")

    return pseudoternary


def pseudoternaryToBinary(pseudoternary: str):
    binary = ""
    for value in pseudoternary:
        if value == "+" or value == "-":
            binary += "0"
        elif value == "0":
            binary += "1"
    return binary


def stringToBinary(texto):
    return "".join(format(ord(char), "08b") for char in texto)


def binaryToString(binStr):
    splittedBinary = [binStr[i : i + 8] for i in range(0, len(binStr), 8)]

    return "".join(chr(int(i, 2)) for i in splittedBinary)


def beTheClient():
    global isServer
    beTheClient_button.configure(fg_color="#000000")
    beTheServer_button.configure(fg_color="#262626")
    isServer = False


def beTheServer():
    global isServer
    beTheClient_button.configure(fg_color="#262626")
    beTheServer_button.configure(fg_color="#000000")
    isServer = True


def setAddress():
    global isServer
    global address
    global port
    global clientThread
    global serverThread
    address = ip_entry.get()
    port = int(port_entry.get())
    print(
        f"You are %s the address '{address}:{port}'" % "hosting at"
        if isServer
        else "connecting at"
    )
    if isServer:
        if serverThread is None:
            serverThread = threading.Thread(target=setupServer, args=(address, port))
            serverThread.start()
    else:
        if clientThread is None:
            clientThread = threading.Thread(target=setupClient, args=(address, port))
            clientThread.start()


def sendMessage(event=None):
    global sock
    global client
    if isServer:
        if client is not None:
            client.send(
                binaryToPseudoTernary(
                    stringToBinary(encrypt(message_entry.get()))
                ).encode("utf-8")
            )
    else:
        if sock is not None:
            sock.send(
                binaryToPseudoTernary(
                    stringToBinary(encrypt(message_entry.get()))
                ).encode("utf-8")
            )
    onSendedMessage(binaryToPseudoTernary(stringToBinary(encrypt(message_entry.get()))))


def validatePortInput(P):
    return (P.isdigit() or P == "") and P.__len__() < 6


def getIP():
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


# function to add the contact
def add_contact():
    nome = name_entry.get()
    telefone = tel_entry.get()

    # Adds contact data to listbox
    contacts_listbox.insert(tkinter.END, nome + " - " + telefone)

    # Clears entries data
    name_entry.delete(0, tkinter.END)
    tel_entry.delete(0, tkinter.END)


shutdownApp = False
customtkinter.deactivate_automatic_dpi_awareness()
isServer = False
address = getIP()
port = 8080
serverThread = None
clientThread = None
sock = None
client = None

# creates the main window
window = tkinter.Tk()
window.configure(bg="#262626")
window.title("Pseudo-Ternary AMI")

vcmd = window.register(validatePortInput)

window.protocol("WM_DELETE_WINDOW", onCloseWindow)

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
message_entry.bind("<Return>", sendMessage)

# Button to send a message #
sendMessage_button = customtkinter.CTkButton(
    master=frame,
    command=sendMessage,
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

# Received message field
receivedMessage_label = customtkinter.CTkLabel(
    master=frame,
    text="Received Message",
    text_color="black",
    width=120,
    height=25,
    fg_color=("white", "gray75"),
    bg_color="#262626",
    corner_radius=8,
)
receivedMessage_label.grid(row=0, column=3, columnspan=2)

receivedMessage = customtkinter.CTkTextbox(
    master=frame,
    width=165,
    height=50,
)
receivedMessage.insert(
    "0.0", "No message received yet."
)  # insert at line 0 character 0
receivedMessage.configure(state="disabled")
receivedMessage.grid(row=1, column=3, columnspan=2)

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
encryptedReceivedMessage.insert(
    "0.0", "No message received yet."
)  # insert at line 0 character 0
encryptedReceivedMessage.configure(state="disabled")
encryptedReceivedMessage.grid(row=3, column=3, columnspan=2)


# Received message in binary field
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
receivedMessageBinary.insert(
    "0.0", "No message received yet."
)  # insert at line 0 character 0
receivedMessageBinary.configure(state="disabled")
receivedMessageBinary.grid(row=5, column=3, columnspan=2)


# Sended message field
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
encryptedSendedMessage.insert(
    "0.0", "No message sended yet."
)  # insert at line 0 character 0
encryptedSendedMessage.configure(state="disabled")
encryptedSendedMessage.grid(row=3, column=6, columnspan=2, padx=5)


# Sended message in binary field
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
sendedMessageBinary.insert(
    "0.0", "No message sended yet."
)  # insert at line 0 character 0
sendedMessageBinary.configure(state="disabled")
sendedMessageBinary.grid(row=5, column=6, columnspan=2, padx=5)


graphFrame = customtkinter.CTkFrame(window)
graphFrame.pack(pady=10, padx=10, fill="both", expand=True)
graphFrame.grid_columnconfigure(0, weight=1)
graphFrame.grid_columnconfigure(1, weight=1)

graphCanvases = []


def pseudoternaryToArray(message):
    return [-1 if char == "-" else 1 if char == "+" else int(char) for char in message]


def createGraph(frame, data, row, column):
    fig = plt.Figure(figsize=(4, 3))
    ax = fig.add_subplot(111)
    ax.step(
        range(len(data)),
        pseudoternaryToArray(data),
        where="mid",
        marker="o",
        linestyle="-",
    )
    if column == 0:
        ax.set_title("Received Message")
    else:
        ax.set_title("Sended Message")

    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().grid(row=row, column=column, padx=10, pady=10)
    graphCanvases.append(canvas)


window.mainloop()
