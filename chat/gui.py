import argparser
import threading
import tkinter as tk
import chat_client as gRPC_client
import grpc
from proto_modules import chat_server_pb2_grpc as __pb2_grpc


# from argparser
NAME = argparser.NAME or 'DEFAULT NAME'
DEV = argparser.DEV

# gui.py doesn't work with chat_client.py when DEV mode
assert DEV == False


class ChatGUI(tk.Tk):
    def __init__(self, _grpcClient) -> None:
        super().__init__()
        self.name = NAME
        self.grpcClient = _grpcClient
        self.setVars()
        self.guiSettings()
        self.setProtocol()

    def setVars(self):
        self.msgCount = 5

    def guiSettings(self):

        self.title("gRPC Chat Room")

        self.msgShow_frame = tk.Frame(self)
        self.msgShow_frame.pack()

        self.msg_frame = tk.Frame(self.msgShow_frame)
        self.scrollbar = tk.Scrollbar(self.msg_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.msg_list = tk.Listbox(
            self.msg_frame, height=17,
            width=100, yscrollcommand=self.scrollbar.set
        )
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()

        # msg_frame.grid(row=0, column=0, columnspan=2)
        self.msg_frame.pack()

        ###################

        input_field = tk.Frame(self)
        # input_field.grid(row=1, column=0)
        input_field.pack()

        user_name = tk.Label(input_field, text=NAME, width=10, height=2)
        user_name.grid(row=0, column=0)

        self.my_msg = tk.StringVar()
        self.my_msg.set("")

        entry_field = tk.Entry(input_field, width=50, textvariable=self.my_msg)
        entry_field.bind("<Return>", self.send)
        entry_field.grid(row=0, column=1)
        # entry_field.pack()

        send_button = tk.Button(
            input_field, text="Send", width=20, command=self.send)
        send_button.grid(row=0, column=2, sticky=tk.E)
        # send_button.pack()

    def setWindowSize(self):
        self.geometry("600x400")

    def setProtocol(self):
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # threading
    def send(self, event=None):
        self.msgCount += 1
        msg = self.my_msg.get()
        self.my_msg.set("")

        self.msg_list.insert(self.msgCount, msg)

        if msg == "{quit}":
            self.quit()

    def on_closing(self, event=None):
        self.my_msg.set("{quit}")
        self.send()

    # threading
    # receive, send ping, send message
    def stubHandler(self, ):
        pass

    def run(self, ):
        self.mainloop()


if __name__ == '__main__':

    stub = __pb2_grpc.ChatServerStub
    channel = grpc.insecure_channel('localhost:50051')

    grpcClient = gRPC_client.MyChatClient(NAME, stub, channel)

    ChatGUI(grpcClient)
