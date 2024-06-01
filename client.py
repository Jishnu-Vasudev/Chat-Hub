# import required modules
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox as mb

class Client:
    HOST = '127.0.0.1'
    PORT = 1234

    DARK_GREY = '#121212'
    MEDIUM_GREY = '#1F1B24'
    OCEAN_BLUE = '#464EB8'
    BLACK = "black"
    WHITE = "white"
    FONT = ("Helvetica", 17)
    BUTTON_FONT = ("Helvetica", 15)
    SMALL_FONT = ("Helvetica", 13)

    # Creating a socket object
    # AF_INET: we are going to use IPv4 addresses
    # SOCK_STREAM: we are using TCP packets for communication
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def add_message(self, message):
        message_box.config(state=tk.NORMAL)
        message_box.insert(tk.END, message + '\n')
        message_box.config(state=tk.DISABLED)

    def Connect_Server(self):
        # try except block
        try:
            # Connect to the server
            self.client.connect((self.HOST, self.PORT))
            mb.showinfo("Information","Successfully connected to server")
            self.add_message("[SERVER] Successfully connected to the server")
        except:
            mb.showerror("Unable to connect to server", f"Unable to connect to server {self.HOST} {self.PORT}")

        username = username_textbox.get()
        if username != '':
            self.client.sendall(username.encode())
        else:
            mb.showerror("Invalid username", "Username cannot be empty")

        threading.Thread(target=self.listen_for_messages_from_server, args=(self.client, )).start()

        username_textbox.config(state=tk.DISABLED)
        username_button.config(state=tk.DISABLED)

    def send_message(self, event=None):
        message = message_textbox.get()
        if message != '':
            self.client.sendall(message.encode())
            message_textbox.delete(0, len(message))
        else:
            mb.showerror("Empty message", "Message cannot be empty")

    def GUI(self):
        root = tk.Tk()
        root.geometry("600x600")
        root.title("Messenger Client")
        root.resizable(False, False)

        root.grid_rowconfigure(0, weight=1)
        root.grid_rowconfigure(1, weight=4)
        root.grid_rowconfigure(2, weight=1)

        top_frame = tk.Frame(root, width=600, height=100, bg=self.DARK_GREY)
        top_frame.grid(row=0, column=0, sticky=tk.NSEW)

        middle_frame = tk.Frame(root, width=600, height=400, bg=self.MEDIUM_GREY)
        middle_frame.grid(row=1, column=0, sticky=tk.NSEW)

        bottom_frame = tk.Frame(root, width=600, height=100, bg=self.DARK_GREY)
        bottom_frame.grid(row=2, column=0, sticky=tk.NSEW)

        username_label = tk.Label(top_frame, text="Enter username:", font=self.FONT, bg=self.DARK_GREY, fg=self.WHITE)
        username_label.pack(side=tk.LEFT, padx=10)

        global username_textbox
        username_textbox = tk.Entry(top_frame, font=self.FONT, bg=self.MEDIUM_GREY, fg=self.WHITE, width=23)
        username_textbox.pack(side=tk.LEFT)

        global username_button
        username_button = tk.Button(top_frame, text="Join", font=self.BUTTON_FONT, bg=self.OCEAN_BLUE, fg=self.WHITE, command=lambda: self.Connect_Server())
        username_button.pack(side=tk.LEFT, padx=15)

        global message_textbox
        message_textbox = tk.Entry(bottom_frame, font=self.FONT, bg=self.BLACK, fg=self.WHITE, width=38)
        message_textbox.pack(side=tk.LEFT, padx=10)

        message_button = tk.Button(bottom_frame, text="Send", font=self.BUTTON_FONT, bg=self.OCEAN_BLUE, fg=self.WHITE, command=self.send_message)
        message_button.pack(side=tk.LEFT, padx=10)

        root.bind('<Return>',self.send_message)

        global message_box
        message_box = scrolledtext.ScrolledText(middle_frame, font=self.SMALL_FONT, bg=self.MEDIUM_GREY, fg=self.WHITE, width=67, height=26.5)
        message_box.config(state=tk.DISABLED)
        message_box.pack(side=tk.TOP)

        root.mainloop()

    def listen_for_messages_from_server(self, client):
        while 1:
            message = client.recv(2048).decode('utf-8')
            if message != '':
                username = message.split("~")[0]
                content = message.split('~')[1]
                self.add_message(f"[{username}] {content}")
            else:
                mb.showerror("Error", "Message recevied from client is empty")

    # main function
    def main(self):
        self.GUI()

if __name__ == "__main__":
    client = Client()
    client.main()