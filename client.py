import socket
import threading
# host 
HOST_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050 
FORMAT = 'UTF-8'
# name for the chat group
Name = input("Enter you Name:")
# set the client socket and connect it
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

client.connect((HOST_IP,PORT))

stop_thread = False

def recieve():
    while True:
        global stop_thread
        if stop_thread:
            break    
        try:
            message = client.recv(1024).decode(FORMAT)
            # if the recived msg is name we send the name of the user
            if message == 'Name':
                # send the name
                client.send(Name.encode(FORMAT))
            # if the message is 'disconnect' we stop        
            elif message == 'DISCONNECT':
                stop_thread =True
                break

            # else we print the message
            else:
                print(message)
        except:
            print('Error while Connecting')
            client.close()
            break
        
def write():
    while True:
        if stop_thread:
            break
        # send the msg consisting of (name , msg)
        message = f'{Name}: {input("")}'
        
        client.send(message.encode(FORMAT))

recieve_thread = threading.Thread(target=recieve)
recieve_thread.start()
write_thread = threading.Thread(target=write)
write_thread.start()