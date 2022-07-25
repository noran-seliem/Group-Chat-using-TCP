#import the needed modules
import threading
import socket
# set the host ip and port of the server and the format
HOST_IP = socket.gethostbyname(socket.gethostname())
# port is prefered as high number  and not something that is usually used by the system like 80 or 8080
PORT = 5050 
FORMAT = 'UTF-8'
# make the server socket and bind it
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST_IP, PORT))

server.listen(3)
# here we track the connected clients and their names 
clients = []
Names = []

# this function is used to send the recived msg from one client to all other clients 
def broadcast(message,client2):
    for client in clients:
        if client is not client2:
            client.send(message)
              

# function for recive the msg and handle it
def handle(client):
    while True:
        try:
            # recive the msg
            msg = message = client.recv(1024)  
            # if the msg is 'exit' we disconnect the client
            if 'exit' in msg.decode(FORMAT):
                if client in clients:
                    index = clients.index(client)
                    # send 'DISCONNECT' and then remove the client from the lest and close his connection
                    client.send('DISCONNECT'.encode(FORMAT))
                    clients.remove(client)
                    client.close()
                    Name = Names[index]
                    print(f'{Name} Left the chat!')
                    broadcast(f'{Name} left the Chat!'.encode(FORMAT),client)
                    Names.remove(Name)
                    break
                 
            else:
                broadcast(message,client)  
        # if there is a problem with the connection
        except:
            if client in clients:
                index = clients.index(client)
                clients.remove(client)
                client.close()
                Name = Names[index]
                broadcast(f'{Name} left the Chat!'.encode(FORMAT),client)
                Names.remove(Name)
                break
# main function to recive client connection and add them in the lists
def recieve():
    while True:
        # accept a client connection
        client, address = server.accept()
        print(f"Connected with {str(address)}")
        # ask the client of his name
        client.send('Name'.encode(FORMAT))
        Name = client.recv(1024).decode(FORMAT)
        # add the client to the list
        Names.append(Name)
        clients.append(client)

        print(f'Name of the client is {Name}')
        broadcast(f'{Name} joined the Chat'.encode(FORMAT),client)
        client.send('Connected to the Server!'.encode(FORMAT))

        
        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


print('Server is Listening ...')
recieve()

