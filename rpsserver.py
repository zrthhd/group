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

