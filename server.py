# Import required modules
import socket
import threading
from tkinter import messagebox as mb

active_clients = []  # List of all currently connected users

class Server:
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 1234 # Any port between 0 and 65535
        self.LISTENER_LIMIT = 5

    def close_existing_socket_instances(self, address, port):
        # Attempt to create a socket and bind to the specified address and port
        if len(active_clients)>4:
            try:
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_socket.bind((self.HOST, self.PORT))
                temp_socket.close()
            except Exception as e:
                # If binding fails, assume that there is an existing socket and close it
                mb.showinfo("Information", f"Closing existing socket on {self.HOST}:{self.PORT}")
                existing_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                existing_socket.connect((self.HOST, self.PORT))
                existing_socket.close()
        else:
            pass
    # Function to listen for upcoming messages from a client
    def listen_for_messages(self, client, username):
        try:
            while 1:
                message = client.recv(2048).decode('utf-8')
                if message != '':
                    final_msg = username + '~' + message
                    self.send_messages_to_all(final_msg)
                else:
                    mb.showinfo("Information", f"The message send from client {username} is empty")
        except Exception as e:
            mb.showerror("Error",e)
    # Function to send message to a single client
    def send_message_to_client(self, client, message):
        try:
            client.sendall(message.encode())
        except Exception as e:
            mb.showerror("Error",e)

    # Function to send any new message to all the clients that
    # are currently connected to this server
    def send_messages_to_all(self, message):
        try:
            for user in active_clients:
                self.send_message_to_client(user[1], message)
        except Exception as e:
            mb.showerror("Error",e)

    # Function to handle client
    def client_handler(self, client):
        try:
            # Server will listen for client message that will
            # Contain the username
            while 1:
                username = client.recv(2048).decode('utf-8')
                if username != '':
                    active_clients.append((username, client))
                    prompt_message = "SERVER~" + f"{username} joined the chat"
                    self.send_messages_to_all(prompt_message)
                    break
                else:
                    mb.showinfo("Information", "Client username is empty")
            threading.Thread(target=self.listen_for_messages, args=(client, username, )).start()
        except Exception as e:
            mb.showerror("Error",e)

    # Main function
    def main(self):
        try:
            # Creating the socket class object
            # AF_INET: we are going to use IPv4 addresses
            # SOCK_STREAM: we are using TCP packets for communication
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            # Creating a try catch block
            try:
                # Provide the server with an address in the form of
                # host IP and port
                server.bind((self.HOST, self.PORT))
                mb.showinfo("Information", f"Running the server on {self.HOST} {self.PORT}")
            except:
                mb.showinfo("Information", f"Unable to bind to host {self.HOST} and port {self.PORT}")
            # Set server limit
            server.listen(self.LISTENER_LIMIT)
            # This while loop will keep listening to client connections
            while 1:
                client, address = server.accept()
                mb.showinfo("Information", f"Successfully connected to client {address[0]} {address[1]}")
                threading.Thread(target=self.client_handler, args=(client, )).start()
        except Exception as e:
            mb.showerror("Error",e)

if __name__ == "__main__":
    serverInst = Server()
    serverInst.close_existing_socket_instances(serverInst.HOST,serverInst.PORT)
    serverInst.main()