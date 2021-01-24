<<<<<<< HEAD
import Tkinter as t
from Tkinter import PhotoImage
import tkMessageBox
import socket
from time import sleep
import threading

#game main window
window_utama = t.Tk()
window_utama.title("RPS Client")
#connect_reqed client name
pemain_nama = ""
rival_nama = ""
g_round = 0 #game round
g_timer = 3 #game timer
#player choice
pemain_choice = ""
rival_choice = ""
tot_rounds = 5 #for final round
pemain_score = 0
rival_score = 0
#network client
client = None
host_addr = "192.168.0.116"
host_port = 8080

#for player name and welcome message
welcome_frame= t.Frame(window_utama)
lbl_nama = t.Label(welcome_frame, text = "Name:")
lbl_nama.pack(side=t.LEFT)
ent_nama = t.Entry(welcome_frame)
ent_nama.pack(side=t.LEFT)
btn_connect = t.Button(welcome_frame, text="Connect", command=lambda : connect())
btn_connect.pack(side=t.LEFT)
welcome_frame.pack(side=t.TOP)

#in the top frame
message_frame = t.Frame(window_utama)
lbl_line = t.Label(message_frame, text="-----------------------------------------------------------").pack()
lbl_welcome = t.Label(message_frame, text="")
lbl_welcome.pack()
lbl_line_server = t.Label(message_frame, text="-----------------------------------------------------------")
lbl_line_server.pack_forget()
message_frame.pack(side=t.TOP)

#frame to display the player and opponent name
top_frame = t.Frame(window_utama)
left_frame= t.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_pemain_nama = t.Label(left_frame, text="pemainr name: " + pemain_nama, font = "Helvetica 13 bold")
lbl_rival_nama = t.Label(left_frame, text="rival: " + rival_nama)
lbl_pemain_nama.grid(row=0, column=0, padx=5, pady=8)
lbl_rival_nama.grid(row=1, column=0, padx=5, pady=8)
left_frame.pack(side=t.LEFT, padx=(10, 10))

#game round frame
right_frame = t.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_g_round = t.Label(right_frame, text="Game round (x) begins in", foreground="blue", font = "Helvetica 14 bold")
lbl_timer = t.Label(right_frame, text=" ", font = "Helvetica 24 bold", foreground="blue")
lbl_g_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
right_frame.pack(side=t.RIGHT, padx=(10, 10))

top_frame.pack_forget()
#game table frame
middle_frame = t.Frame(window_utama)

lbl_line = t.Label(middle_frame, text="-----------------------------------------------------------").pack()
lbl_line = t.Label(middle_frame, text="**** GAME TABLE ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = t.Label(middle_frame, text="-----------------------------------------------------------").pack()

#frame for player and opponent choice and the game round
round_frame = t.Frame(middle_frame)
lbl_round = t.Label(round_frame, text="Round")
lbl_round.pack()
lbl_pemain_choice = t.Label(round_frame, text="Player Choice: " + "None", font = "Helvetica 13 bold")
lbl_pemain_choice.pack()
lbl_rival_choice = t.Label(round_frame, text="Opponent Choice: " + "None")
lbl_rival_choice.pack()
lbl_result = t.Label(round_frame, text=" ", foreground="blue", font = "Helvetica 14 bold")
lbl_result.pack()
round_frame.pack(side=t.TOP)

bottom_frame = t.Frame(middle_frame)
lbl_line = t.Label(bottom_frame, text="-----------------------------------------------------------").pack()
lbl_final = t.Label(bottom_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final.pack()
lbl_line = t.Label(bottom_frame, text="-----------------------------------------------------------").pack()
bottom_frame.pack(side=t.TOP)

middle_frame.pack_forget()
#read picture file
button_frame = t.Frame(window_utama)
rock_img = PhotoImage(file=r"rock.gif")
paper_img = PhotoImage(file = r"paper.gif")
scissors_img = PhotoImage(file = r"scissors.gif")

#place for rock paper scissor button at the bottom
rock_button = t.Button(button_frame, text="Rock", command=lambda : choice("rock"), state=t.DISABLED, image=rock_img)
paper_button = t.Button(button_frame, text="Paper", command=lambda : choice("paper"), state=t.DISABLED, image=paper_img)
scissors_button = t.Button(button_frame, text="Scissors", command=lambda : choice("scissors"), state=t.DISABLED, image=scissors_img)
rock_button.grid(row=0, column=0)
paper_button.grid(row=0, column=1)
scissors_button.grid(row=0, column=2)
button_frame.pack(side=t.BOTTOM)

#logic rules to find winner for each round
def score_count(pemain, rival):
    winner = ""
    rock = "rock"
    paper = "paper"
    scissors = "scissors"
    p0 = "pemain"
    p1 = "rival"

    if pemain == rival:
        winner = "draw"
    elif pemain == rock:
        if rival == paper:
            winner = p1
        else:
            winner = p0
    elif pemain == scissors:
        if rival == rock:
            winner = p1
        else:
            winner = p0
    elif pemain == paper:
        if rival == scissors:
            winner = p1
        else:
            winner = p0
    return winner

#to disable and enable picture buttons
def buttons(do):
    if do == "disable":
        rock_button.config(state=t.DISABLED)
        paper_button.config(state=t.DISABLED)
        scissors_button.config(state=t.DISABLED)
    else:
        rock_button.config(state=t.NORMAL)
        paper_button.config(state=t.NORMAL)
        scissors_button.config(state=t.NORMAL)

#get the name and display it on the name frame
def connect():
    global pemain_nama
    if len(ent_nama.get()) < 1:
        t.messagebox.showerror(title="ERROR!", message="PLAYER MUST ENTER FIRST NAME!")
    else:
        pemain_nama = ent_nama.get()
        lbl_pemain_nama["text"] = "Player Name: " + pemain_nama
        server_connect(pemain_nama)

#for game round counter
def countdown_timer(pemain_timer, nothing):
    global g_round
    if g_round <= tot_rounds:
        g_round = g_round + 1

    lbl_g_round["text"] = "Game Round" + str(g_round) + " begins in"

    while pemain_timer > 0:
        pemain_timer = pemain_timer - 1
        print("Game Timer is: " + str(pemain_timer))
        lbl_timer["text"] = pemain_timer
        sleep(1)

    buttons("enable")
    lbl_round["text"] = "Round - " + str(g_round)
    lbl_final["text"] = ""

#display player choice
def choice_pemain(arg):
    global pemain_choice, cl, g_round
    pemain_choice = arg
    lbl_pemain_choice["text"] = "Player Choice: " + pemain_choice
    #send the choice to the server for server to send it to the opponent
    if cl:
        cl.send("Game Round"+str(g_round)+pemain_choice)
        buttons("disable")

#to get the player name
def server_connect(nama):
    global cl, host_addr, host_port, pemain_nama
    try:
        cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cl.connect((host_addr, host_port))
        cl.send(nama) #send nama to server after connect_reqing

        #widgets are disabled
        btn_connect.config(state=t.DISABLED)
        ent_nama.config(state=t.DISABLED)
        lbl_nama.config(state=t.DISABLED)
        buttons("disable")

        #for multiple client to connect 
        threading._start_new_thread(serv_receive, (cl, "m"))
    except Exception as e:
        t.messagebox.showerror(title="ERROR!", message="UNABLE TO CONNECT TO HOST: " + host_addr + " ON PORT: " + str(host_port) + " SERVER IS UNAVAILABLE PLEASE TRY AGAIN")


def serv_receive(sock, m):
    global pemain_nama, rival_nama, g_round
    global pemain_choice, rival_choice, pemain_score, rival_score

    while True:
        msgfrom_server = sock.recv(4096)

        if not msgfrom_server: break
        #check - as the server sends welcome, it then waits for
        #another player
        #if the welcome message already been received twice it
		#will proceed the game
        if msgfrom_server.startswith("welcome"):
            if msgfrom_server == "welcome1":
                lbl_welcome["text"] = "Welcome " + pemain_nama + "! Please wait for Player 2."
            elif msgfrom_server == "welcome2":
                lbl_welcome["text"] = "Welcome " + pemain_nama + "! Game will begin soon."
            lbl_line_server.pack()
        #to display the opponent name which we receive from the server
        elif msgfrom_server.startswith("rival_nama$"):
            rival_nama = msgfrom_server.replace("rival_nama$", "")
            lbl_rival_nama["text"] = "rival: " + rival_nama
            top_frame.pack()
            middle_frame.pack()

            #if 2 players already connected proceed to the game
			#timer will begin
			#timer - to coordinate the apps
            threading._start_new_thread(countdown_timer, (g_timer, ""))
            lbl_welcome.config(state=t.DISABLED)
            lbl_line_server.config(state=t.DISABLED)
        #to display the opponent choice, get from server
        elif msgfrom_server.startswith("$rival_choice"):
            #get the opponent choice from server
            rival_choice = msgfrom_server.replace("$rival_choice", "")

            #to count the winner in the final
            pemenang_round = score_count(pemain_choice, rival_choice)
            round_result = " "
            if pemenang_round == "pemain":
                pemain_score = pemain_score + 1
                round_result = "WIN"
            elif pemenang_round == "rival":
                rival_score = rival_score + 1
                round_result = "LOSS"
            else:
                round_result = "DRAW"

            #GUI will be updated
            lbl_rival_choice["text"] = "Opponent Choice: " + rival_choice
            lbl_result["text"] = "Result: " + round_result

            #last round:Round 3
            if g_round == tot_rounds:
                #compute final result
                final = ""
                color = ""

                if pemain_score > rival_score:
                    final = "(YOU WON!)"
                    color = "green"
                elif pemain_score < rival_score:
                    final = "(YOU LOST!)"
                    color = "red"
                else:
                    final = "(IT IS A DRAW!)"
                    color = "yellow"

                lbl_final["text"] = "FINAL RESULT: " + str(pemain_score) + " - " + str(rival_score) + " " + final
                lbl_final.config(foreground=color)

                buttons("disable")
                g_round = 0

            #start the timer
            threading._start_new_thread(countdown_timer, (g_timer, ""))


    sock.close()


window_utama.mainloop()
=======
import Tkinter as t
from Tkinter import PhotoImage
#from Tkinter import messagebox
import tkMessageBox
import socket
from time import sleep
import threading

#game main window
window_utama = t.Tk()
window_utama.title("RPS Client")
#connect_reqed client name
pemain_nama = ""
rival_nama = ""
g_round = 0 #game round
g_timer = 5 #game timer
#player choice
pemain_choice = ""
rival_choice = ""
TOTAL_NO_OF_ROUNDS = 5 #for final round
pemain_score = 0
rival_score = 0
#network client
client = None
HOST_ADDR = "192.168.0.116"
HOST_PORT = 8080

#for player name and welcome message
welcome_frame= t.Frame(window_utama)
lbl_nama = t.Label(welcome_frame, text = "Name:")
lbl_nama.pack(side=t.LEFT)
ent_nama = t.Entry(welcome_frame)
ent_nama.pack(side=t.LEFT)
btn_connect = t.Button(welcome_frame, text="Connect", command=lambda : connect())
btn_connect.pack(side=t.LEFT)
welcome_frame.pack(side=t.TOP)

#in the top frame
message_frame = t.Frame(window_utama)
lbl_line = t.Label(message_frame, text="---------------------------------------------------------------------").pack()
lbl_welcome = t.Label(message_frame, text="")
lbl_welcome.pack()
lbl_line_server = t.Label(message_frame, text="---------------------------------------------------------------------")
lbl_line_server.pack_forget()
message_frame.pack(side=t.TOP)

#frame to display the player and opponent name
top_frame = t.Frame(window_utama)
left_frame= t.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_pemain_nama = t.Label(left_frame, text="Player Name: " + pemain_nama, font = "Verdana 14 bold")
lbl_rival_nama = t.Label(left_frame, text="Opponent: " + rival_nama)
lbl_pemain_nama.grid(row=0, column=0, padx=5, pady=5)
lbl_rival_nama.grid(row=1, column=0, padx=5, pady=5)
left_frame.pack(side=t.LEFT, padx=(10, 10))

#game round frame
right_frame = t.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)
lbl_g_round = t.Label(right_frame, text="Game Round  (x) begins in", foreground="blue", font = "Verdana 14 bold")
lbl_timer = t.Label(right_frame, text=" ", font = "Verdana 14 bold", foreground="blue")
lbl_g_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)
right_frame.pack(side=t.RIGHT, padx=(10, 10))

top_frame.pack_forget()
#game table frame
middle_frame = t.Frame(window_utama)

lbl_line = t.Label(middle_frame, text="---------------------------------------------------------------------").pack()
lbl_line = t.Label(middle_frame, text=" GAME TABLE ", font = "Verdana 14 bold", foreground="blue").pack()
lbl_line = t.Label(middle_frame, text="---------------------------------------------------------------------").pack()

#frame for player and opponent choice and the game round
round_frame = t.Frame(middle_frame)
lbl_round = t.Label(round_frame, text="Round")
lbl_round.pack()
lbl_pemain_choice = t.Label(round_frame, text="Player Choice: " + "None", font = "Verdana 13 bold")
lbl_pemain_choice.pack()
lbl_rival_choice = t.Label(round_frame, text="Opponent Choice: " + "None")
lbl_rival_choice.pack()
lbl_result = t.Label(round_frame, text=" ", foreground="blue", font = "Verdana 14 bold")
lbl_result.pack()
round_frame.pack(side=t.TOP)

bottom_frame = t.Frame(middle_frame)
lbl_line = t.Label(bottom_frame, text="---------------------------------------------------------------------").pack()
lbl_final = t.Label(bottom_frame, text=" ", font = "Verdana 13 bold", foreground="blue")
lbl_final.pack()
lbl_line = t.Label(bottom_frame, text="---------------------------------------------------------------------").pack()
bottom_frame.pack(side=t.TOP)

middle_frame.pack_forget()
#read picture file
button_frame = t.Frame(window_utama)
rock_img = PhotoImage(file=r"rock.gif")
paper_img = PhotoImage(file = r"paper.gif")
scissors_img = PhotoImage(file = r"scissors.gif")

#place for rock paper scissor button at the bottom
rock_button = t.Button(button_frame, text="Rock", command=lambda : choice("Rock"), state=t.DISABLED, image=rock_img)
paper_button = t.Button(button_frame, text="Paper", command=lambda : choice("Paper"), state=t.DISABLED, image=paper_img)
scissors_button = t.Button(button_frame, text="Scissors", command=lambda : choice("Scissors"), state=t.DISABLED, image=scissors_img)
rock_button.grid(row=0, column=0)
paper_button.grid(row=0, column=1)
scissors_button.grid(row=0, column=2)
button_frame.pack(side=t.BOTTOM)

#logic rules to find winner for each round
def score_count(pemain, rival):
    winner = ""
    rock = "Rock"
    paper = "Paper"
    scissors = "Scissors"
    p0 = "pemain"
    p1 = "rival"

    if pemain == rival:
        winner = "draw"
    elif pemain == rock:
        if rival == paper:
            winner = p1
        else:
            winner = p0
    elif pemain == scissors:
        if rival == rock:
            winner = p1
        else:
            winner = p0
    elif pemain == paper:
        if rival == scissors:
            winner = p1
        else:
            winner = p0
    return winner

#to disable and enable picture buttons
def buttons_start(do):
    if do == "disable":
        rock_button.config(state=t.DISABLED)
        paper_button.config(state=t.DISABLED)
        scissors_button.config(state=t.DISABLED)
    else:
        rock_button.config(state=t.NORMAL)
        paper_button.config(state=t.NORMAL)
        scissors_button.config(state=t.NORMAL)

#get the name and display it on the name frame
def connect():
    global pemain_nama
    if len(ent_nama.get()) < 1:
        t.messagebox.showerror(title="ERROR!", message="PLAYER MUST ENTER FIRST NAME!")
    else:
        pemain_nama = ent_nama.get()
        lbl_pemain_nama["text"] = "Player Name: " + pemain_nama
        server_connect(pemain_nama)

#for game round counter
def countdown_timer(pemain_timer, nothing):
    global g_round
    if g_round <= TOTAL_NO_OF_ROUNDS:
        g_round = g_round + 1

    lbl_g_round["text"] = "Game Round" + " " + str(g_round) + " begins in"

    while pemain_timer > 0:
        pemain_timer = pemain_timer - 1
        print("Game Timer is: " + str(pemain_timer))
        lbl_timer["text"] = pemain_timer
        sleep(1)

    buttons_start("enable")
    lbl_round["text"] = "Round - " + str(g_round)
    lbl_final["text"] = ""

#display player choice
def choice(arg):
    global pemain_choice, cl, g_round
    pemain_choice = arg
    lbl_pemain_choice["text"] = "Player Choice: " + pemain_choice
    #send the choice to the server for server to send it to the opponent
    if cl:
        cl.send("Game Round"+ str(g_round) + pemain_choice)
        buttons_start("disable")

#to get the player name
def server_connect(nama):
    global cl, HOST_ADDR, HOST_PORT, pemain_nama
    try:
        cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        cl.connect((HOST_ADDR, HOST_PORT))
        cl.send(nama) #send nama to server after connect_reqing

        #widgets are disabled
        btn_connect.config(state=t.DISABLED)
        ent_nama.config(state=t.DISABLED)
        lbl_nama.config(state=t.DISABLED)
        buttons_start("disable")

        #for multiple client to connect 
        threading._start_new_thread(serv_receive, (cl, "m"))
    except Exception as e:
        t.messagebox.showerror(title="ERROR!", message="UNABLE TO CONNECT TO HOST: " + HOST_ADDR + " ON PORT: " + str(HOST_PORT) + " SERVER IS UNAVAILABLE PLEASE TRY AGAIN")


def serv_receive(sock, m):
    global pemain_nama, rival_nama, g_round
    global pemain_choice, rival_choice, pemain_score, rival_score

    while True:
        msgfrom_server = sock.recv(4096)

        if not msgfrom_server: break
        #check - as the server sends welcome, it then waits for
        #another player
        #if the welcome message already been received twice it
		#will proceed the game
        if msgfrom_server.startswith("welcome"):
            if msgfrom_server == "welcome1":
                lbl_welcome["text"] = "Welcome " + pemain_nama + "! Please wait for Player 2."
            elif msgfrom_server == "welcome2":
                lbl_welcome["text"] = "Welcome " + pemain_nama + "! Game will begin soon."
            lbl_line_server.pack()
        #to display the opponent name which we receive from the server
        elif msgfrom_server.startswith("rival_nama$"):
            rival_nama = msgfrom_server.replace("rival_nama$", "")
            lbl_rival_nama["text"] = "Opponent: " + rival_nama
            top_frame.pack()
            middle_frame.pack()

            #if 2 players already connected proceed to the game
			#timer will begin
			#timer - to coordinate the apps
            threading._start_new_thread(countdown_timer, (g_timer, ""))
            lbl_welcome.config(state=t.DISABLED)
            lbl_line_server.config(state=t.DISABLED)
            
        #to display the opponent choice, get from server
        elif msgfrom_server.startswith("$rival_choice"):
            #get the opponent choice from server
            rival_choice = msgfrom_server.replace("$rival_choice", "")

            #to count the winner in the final
            pemenang_round = score_count(pemain_choice, rival_choice)
            round_result = " "
            if pemenang_round == "pemain":
                pemain_score = pemain_score + 1
                round_result = "WIN"
            elif pemenang_round == "rival":
                rival_score = rival_score + 1
                round_result = "LOSS"
            else:
                round_result = "DRAW"

            #GUI will be updated
            lbl_rival_choice["text"] = "Opponent Choice: " + rival_choice
            lbl_result["text"] = "Result: " + round_result

            #last round:Round 3
            if g_round == TOTAL_NO_OF_ROUNDS:
                #compute final result
                final = ""
                color = ""

                if pemain_score > rival_score:
                    final = "(YOU WON!)"
                    color = "green"
                elif pemain_score < rival_score:
                    final = "(YOU LOST!)"
                    color = "red"
                else:
                    final = "(IT IS A DRAW!)"
                    color = "orange"

                lbl_final["text"] = "FINAL RESULT: " + str(pemain_score) + " - " + str(rival_score) + " " + final
                lbl_final.config(foreground=color)

                buttons_start("disable")
                g_round = 0

            #start the timer
            threading._start_new_thread(countdown_timer, (g_timer, ""))


    sock.close()


window_utama.mainloop()
>>>>>>> 748ace0c5b0c1a400a43f03bf66451a44893b560
