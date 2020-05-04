import socket  # provide acccess to BSD Socket Interface
from threading import Thread

import tkinter as tk
from tkinter import ttk

#_____CLIENT FUNCTIONS_____
global client_name,first_time,message_records


client_name =  " "
first_time = True

message_records = []

def receive_msg():
	while True:
		try:
			msg = client_socket.recv(BUFFER_SIZE).decode("utf-8")
			global client_name

			if (msg == "+shwmsg"):
				top = tk.Tk()
				msg_history = tk.Listbox(top,bg="#D27933",height=15,width=50,font=("Courier",12,"bold"))
				for i,jmsg in enumerate(message_records):
					if(i>0):
						msg_history.insert(tk.END, jmsg)
				msg_history.pack()
				btnexit = tk.Button(top,text="Okey",command = top.destroy)
				top.mainloop()

			elif (msg.find("If you ever want to quit") != -1):
				msg_to_print = msg.split("+")[0]
				online_users = msg.split("+")[1]

				users_listbox.insert(tk.END,"Online Users:")
				for user in online_users.split(" "):
					users_listbox.insert(tk.END,user)

				msg_list.insert(tk.END, msg_to_print)
			elif ( msg.find("joined to the chat room") != -1):
				msg_to_print = msg.split("+")[0]
				online_users = msg.split("+")[1]
				users_listbox.delete(0,tk.END)	

				users_listbox.insert(tk.END,"Online Users:")
				for user in online_users.split(" "):
					users_listbox.insert(tk.END,user)

				msg_list.insert(tk.END, msg_to_print)


			elif(msg.find("shwuserbymsg+") != -1):
				msgs = msg.split("+")[1].split(",")
				selected_client = msg.split("+")[2]

				top = tk.Tk()
				lbox = tk.Listbox(top,bg = "white",height=15,width=50) 
				for i in msgs:
					i = selected_client+": "+i
					lbox.insert(tk.END,i)

				button = tk.Button(top,text="Okey",command = top.destroy)
				lbox.pack()
				button.pack()
				top.mainloop()
			elif(msg.find("groupmessage+") !=-1):
				group_messages.place(relx=0,rely=0,relheight=1,relwidth=0.70)
				real_msg = msg.split("+")[1]
				groupname = msg.split("+")[2]
				clientname = msg.split("+")[3]
				group_messages.insert(tk.END,clientname+" ("+groupname + "): " + real_msg)

			else:
				message_records.append(msg)
				# save to the messages.txt file
				if msg != "Please type your name and enter:":
					with open("messages.txt","a") as output:
						output.write(msg + '\n')


				if(msg != "+shwmsg"):
					msg_list.insert(tk.END, msg)

		except OSError:
			pass # Probabaly client has left the chat

def search_message():
	

	def callback():
		global message_records
		lbox.delete(0,tk.END)
		keyword = entry.get()

		for i,msg in enumerate(message_records):
			if i == 0:
				continue
			if msg.split(":")[1].find(keyword) != -1 : 
				lbox.insert(tk.END,msg)



	def exit():
		lbox.delete(0,tk.END)
		top.destroy()

	top = tk.Tk()
	lbox = tk.Listbox(top,height=15,width=50,bg="white")
	entry = tk.Entry(top,bg="red")
	search_btn = tk.Button(top,text="Search",command=callback)
	button = tk.Button(top,text="Exit",command=exit)
	lbox.pack()
	entry.pack()
	search_btn.pack()
	button.pack()
	top.mainloop()


	
def send_msg(event = None):
	global first_time,client_name
	if first_time == True:
		msg = my_msg.get()
		client_name = msg
		root.title(client_name)
		first_time = False

	msg = my_msg.get()

	if(msg != "" or msg != " "): # if message isn't empty
		my_msg.set("")  # Clears input field.

		if msg.find("$")!=-1:
			msg = msg + "+"+ client_name
			client_socket.send(msg.encode("utf-8")) #send message

		elif msg == "{quit}":  # close client 
			client_socket.close()
			root.quit()
		else:
			
			client_socket.send(msg.encode("utf-8")) #send message

def show_msg_records():
	global client_name
	cmsg = "shwmsg+" + client_name
	client_socket.send(cmsg.encode("utf-8")) # show messages records




def show_user_msg():
	global client_name
	def callback():
		selected_client = combobox.get()

		top.destroy()
		cmsg = "shwuserbymsg+" + client_name + "+" + selected_client
		client_socket.send(cmsg.encode("utf-8")) # show messages records


	top = tk.Tk()
	label = tk.Label(top,text = "Please select username:")
	val = list(users_listbox.get(0,tk.END))
	val.remove("Online Users:")
	combobox = ttk.Combobox(top,values = val)

	btn = tk.Button(top,text = "okey",command= callback)
	label.grid(row = 0,column = 0)
	combobox.grid(row = 0,column = 1)
	btn.grid(row = 1,column = 0)
	top.mainloop()



def on_closing(event=None): # close connection before close the kinter app
	my_msg.set("{quit}")
	#send_msg()

# TKINTER WINDOW
WIDTH = 1200
HEIGHT = 400

root = tk.Tk()
root.title("Chat Room")

canvas = tk.Canvas(root,width = WIDTH,height = HEIGHT)
canvas.pack()

user_frame = tk.Frame(canvas,bg="#5EB619")
user_frame.place(relx=0,rely=0,relwidth=0.60,relheight=1)

result_frame = tk.Frame(canvas,bd=5,bg="white")
result_frame.place(relx=0.60,y=0,relwidth = 0.40,relheight = 1)



group_messages = tk.Listbox(result_frame,bg="#D6A640",font=("Courier",10,"bold"))
group_messages.place(relx=0,rely=0,relheight=1,relwidth=0.70)
group_messages.place_forget()

users_listbox = tk.Listbox(result_frame,bg="#E6D207",font=("Courier",12,"bold"))
users_listbox.place(relx=0.70,rely=0,relheight=1,relwidth=0.30)


msg_frame = tk.Frame(user_frame,bd=5,bg="#5EB619")
msg_frame.place(relx=0,rely=0,relheight = 0.80,relwidth=1)

button_frame = tk.Frame(user_frame,bd=5,bg="#5EB619")
button_frame.place(relx=0,rely=  0.80,relheight = 0.20,relwidth=1)

my_msg = tk.StringVar()

my_msg.set("Type here...")

scrollbar = tk.Scrollbar(msg_frame)

msg_list = tk.Listbox(msg_frame,height=15,width=80,yscrollcommand=scrollbar.set,font=("Courier",12,"bold"))
# packing

scrollbar.pack(side=tk.RIGHT,fill=tk.Y)
msg_list.pack(side=tk.LEFT,fill=tk.BOTH)

# typing field

entry_field = tk.Entry(button_frame,textvariable=my_msg,font=("Courier",12,"bold"),bg="#18E1BA" )
entry_field.bind("<Return>", send_msg)
entry_field.place(relx=0,rely=0,relheight=0.5,relwidth=1)

send_button = tk.Button(button_frame,text="Send",command = send_msg)
send_button.place(relx=0,rely=0.5,relheight=0.5,relwidth=0.40)

show_msg_by_user = tk.Button(button_frame,text="Show Messages by Users",command = show_user_msg)
show_msg_by_user.place(relx=0.40,rely=0.5,relheight=0.5,relwidth=0.20)

show_past_msg = tk.Button(button_frame,text="Show Messages Records",command = show_msg_records)
show_past_msg.place(relx=0.60,rely=0.5,relheight=0.5,relwidth=0.20)

find_keyword_btn = tk.Button(button_frame,text="Search message",command = search_message)
find_keyword_btn.place(relx=0.80,rely=0.5,relheight=0.5,relwidth=0.20)





root.protocol("WM_DELETE_WINDOW",on_closing) # call on_closing function when tkinter window is closed


BUFFER_SIZE = 1024
TCP_IP = "127.0.0.1"
TCP_PORT = 5005  # port number
SERVER_ADD = (TCP_IP,TCP_PORT)

client_socket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM, proto = 0)

client_socket.connect(SERVER_ADD)
 

receive_thread = Thread(target = receive_msg)
receive_thread.start()

root.mainloop()
