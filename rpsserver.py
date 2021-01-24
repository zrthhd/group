import Tkinter as t
import socket
import threading
from time import sleep

window_utama = t.Tk()
window_utama.title("RPS Server")

#first frame - for button
#only one button is enabled at time to avoid multiple selection
#for client to stop connection, they only have to click the exit
#they dont have to interfere with the server button
firstFrame = t.Frame(window_utama)
startBtn = t.Button(firstFrame, text="Start", command=lambda : start())
startBtn.pack(side=t.LEFT)
stopBtn = t.Button(firstFrame, text="Stop", command=lambda : stop(), state=t.DISABLED)
stopBtn.pack(side=t.LEFT)
firstFrame.pack(side=t.TOP, pady=(5, 0))

#second frame to display address and port used
#this is manually set
secondFrame = t.Frame(window_utama)
hostLabel = t.Label(secondFrame, text = "")
hostLabel.pack(side=t.LEFT)
portLabel = t.Label(secondFrame, text = "")
portLabel.pack(side=t.LEFT)
secondFrame.pack(side=t.TOP, pady=(5, 0))

#client frame to display the list of active cs
lstclFrame = t.Frame(window_utama)
lineLabel = t.Label(lstclFrame, text="Player List").pack()
scrollBar = t.Scrollbar(lstclFrame)
scrollBar.pack(side=t.RIGHT, fill=t.Y)
tDisplay = t.Text(lstclFrame, height=10, width=30)
tDisplay.pack(side=t.LEFT, fill=t.Y, padx=(5, 0))
scrollBar.config(command=tDisplay.yview)
tDisplay.config(yscrollcommand=scrollBar.set, background="#F4F6F7", highlightbackground="grey", state="disabled")
lstclFrame.pack(side=t.BOTTOM, pady=(5, 10))

server = None
HOST_ADDR = "192.168.0.116" #ip address of the server
HOST_PORT = 8080 #port used
cl_nama = " "
cs = []
cs_nama = []
p_data = [] #data about the player

#function for the server start button and to initiate connection
def start():
    #global is used to create variables from a non-global scope
    #in this case inside a function
    global serv, HOST_ADDR, HOST_PORT
    startBtn.config(state=t.DISABLED) #button is disabled upon select
    stopBtn.config(state=t.NORMAL)

    serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    print socket.AF_INET
    print socket.SOCK_STREAM

    serv.bind((HOST_ADDR, HOST_PORT))
    serv.listen(5)  #server listens for client

    #multiple cls allowed to be connected
    threading._start_new_thread(cs_accept, (serv, " "))
    
    #to display the address and port used on the server frame
    hostLabel["text"] = "Address: " + HOST_ADDR
    portLabel["text"] = "Port: " + str(HOST_PORT)

#function for the server stop button
def stop():
    global serv
    startBtn.config(state=t.NORMAL)
    stopBtn.config(state=t.DISABLED) #button will be disabled when clicked

#to accept multiple clients and stores the clients
def cs_accept(the_server, y):
    while True:
        if len(cs) < 2:
            cl, addr = the_server.accept()
            cs.append(cl)

            # use a thread so as not to clog the gui thread
            threading._start_new_thread(message_from_client, (cl, addr))

#continous loop to receive message from connected clients
def message_from_client(cl_connect, cl_ip_addr):
    global serv, cl_nama, cs, p_data, p0, p1
    #message from client
    cl_message = " "

    #player nama is received from client
    cl_nama = cl_connect.recv(4096)
    #welcome message is sent to client
    if len(cs) < 2:
        cl_connect.send("welcome1")
    else:
        cl_connect.send("welcome2")

    cs_nama.append(cl_nama)
    nama_display_update(cs_nama)  #update display client name

    if len(cs) > 1:
        sleep(1)

        #rival nama is sent
        cs[0].send("rival_nama$" + cs_nama[1])
        cs[1].send("rival_nama$" + cs_nama[0])
        #to coordinate

    while True:
        data = cl_connect.recv(4096)
        if not data: break

        #to retrieve the choice that player selects from the data received
        player_choice = data[11:len(data)]

        message = {
            "choice": player_choice,
            "socket": cl_connect
        }
        #check if there are already 2 connected clients
        if len(p_data) < 2:
            p_data.append(message)

        if len(p_data) == 2:
            #to send player choice to opponent
            p_data[0].get("socket").send("$rival_choice" + p_data[1].get("choice"))
            p_data[1].get("socket").send("$rival_choice" + p_data[0].get("choice"))

            p_data = []


    indeks = retrieve_indeks_cl(cs, cl_connect)
    del cs_nama[indeks]
    del cs[indeks]
    cl_connect.close()
    #to update the client name and display it on clients list
    nama_display_update(cs_nama)  #update client nama display

#the index of the current clients is returned to the clients list
def retrieve_indeks_cl(cl_list, cl_current):
    indeks = 0
    for conn in cl_list:
        if conn == cl_current:
            break
        indeks = indeks + 1
    return indeks

#when a new client connects or disconnects the clients list is updated
def nama_display_update(nama_list):
    tDisplay.config(state=t.NORMAL)
    tDisplay.delete('1.0', t.END)

    for k in nama_list:
        tDisplay.insert(t.END, k+"\n".encode('ascii'))
        tDisplay.config(state=t.DISABLED)
window_utama.mainloop()
