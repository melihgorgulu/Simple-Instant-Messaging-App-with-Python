# IMPORTING LİBRARİES
import socket
from threading import Thread

# ________SERVER FUNCTİONS________

# BROADCAST MESSAGE

def broadcast(msg,prefix=""): # msg:message to broadcast, prefix: sender ideftification  
	# broadcast message to the all clients
	for client_socket in clients:
		client_socket.send(prefix.encode("utf-8")+ msg)

def send_msgto_one_client(msg,client_name):
	for client_socket,name in clients.items():
		if(name==client_name):
			client_socket.send(msg.encode("utf-8"))

def send_msgto_multiple_client(msg,members):

	if isinstance(members,list) != True:
		members = members.split(",") # create a list

	for name_client in members:
		for client_socket,name in clients.items():
			if(name==name_client):
				client_socket.send(msg.encode("utf-8"))




# ACCEPT CONNECTIONS

def accept_connections():  # accept incoming client/s connection request
	while True:  # wait connection
		client_conn,client_address = server.accept()  # returns connection socket and socket address
		print("{0}:{1} has connected.".format(client_address[0],client_address[1]))

		client_conn.send("Please type your name and enter:".encode("utf-8"))  # send it to the connected client
		adresses[client_conn] = client_address # add connected client adress to the adresses dict
		Thread(target = handle_client,args = (client_conn,)).start()  # starting thread ps: init thread for every connection


# HANDLE CLİENT

def handle_client(client):

	name = client.recv(BUFFER_SIZE).decode("utf-8") # get client name
	clients[client] = name # add client name to the clients dict.

	hello_msg = "Hi {0}. If you ever want to quit, type kapanbaba".format(name) + "+"
	tmp = " "
	tmp = tmp.join(list(clients.values()))

	hello_msg = hello_msg + tmp

	client.send(hello_msg.encode("utf-8")) #send hello message to the user

	join_msg = "{0} joined to the chat room".format(name) + "+"
	tmp = " "
	tmp = tmp.join(list(clients.values()))
	join_msg = join_msg + tmp
	broadcast(join_msg.encode("utf-8"))  # broad cast the message to the all users.
	
	global opened_group_name,opened_group_members
	while True:
		client_msg = client.recv(BUFFER_SIZE) #receive client's message
		decoded_msg = client_msg.decode("utf-8")
		 

		if(decoded_msg == "kapanbaba"):
			client.send(bytes("{quit}", "utf-8"))
			client.close()  #close connection

			del clients[client] # delete client from dict
			broadcast(bytes("{0} has left the chat".format(name),"utf-8"))
			break
			
		elif(decoded_msg.find("shwmsg+")!=-1):

			client_name = decoded_msg.split("+")[1]
			send_msgto_one_client("+shwmsg",client_name)

		elif(decoded_msg.find("shwuserbymsg+")!=-1):
			dest_client = decoded_msg.split("+")[1]
			selected_client_for_msg = decoded_msg.split("+")[2]

			if (selected_client_for_msg in messages.keys()):
				send_msgto_one_client("shwuserbymsg+" + messages[selected_client_for_msg]+"+"+selected_client_for_msg,dest_client)

		elif(decoded_msg.find("opengroup+") != -1):  # client want to open group
			dest_client = decoded_msg.split("+")[1] # return all client names to dest client
			msg = "opengroup+"
			for i in clients.values():
				msg = msg+i+","

			send_msgto_one_client(msg,dest_client)



		elif(decoded_msg.find("groupopened+") !=-1):

			group_name = decoded_msg.split("+")[1] # specift group name to the clients
			opened_group_name = group_name

			opened_group_members = decoded_msg.split("+")[2] # clients to sent message
			opened_group_members = opened_group_members.split(",")
			

		elif (decoded_msg.find("$")!=-1 and decoded_msg.split("+")[1] in opened_group_members):

			decoded_msg = decoded_msg.split("+")[0]
			decoded_msg = decoded_msg.replace("$","") # remove code $

			msg = "groupmessage+" + decoded_msg + "+" + opened_group_name + "+" + name
			send_msgto_multiple_client(msg,opened_group_members)

		elif(decoded_msg.find("$")!=-1 and decoded_msg.find("+")!=-1):
			decoded_msg = decoded_msg.split("$")[1].split("+")[0]
			encoded_msg = decoded_msg.encode("utf-8")
			broadcast(encoded_msg,name+": ")




		else:  # send message
			if name in messages.keys(): 
				messages[name] = messages[name] + "," + decoded_msg 
			else:
				messages[name] = decoded_msg

			broadcast(client_msg,name+": ")


clients = {} # dict for clients that connected to the server
adresses= {} # dict Connected client's adresses

messages = {}  # for store messages 


global opened_group_members,opened_group_name
opened_group_members = []
opened_group_name = " "


TCP_IP = "127.0.0.1"
TCP_PORT = 5005  #server port number
BUFFER_SIZE = 1024 # server input buffer size

server = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM, proto = 0) # create socket for server
server.bind((TCP_IP,TCP_PORT))  # bind socket adress to server



if __name__ == "__main__":
	server.listen(5) # max 5 connection
	print("Waiting for connection...")
	thread = Thread(target=accept_connections)
	thread.start()
	thread.join()
	server.close()

