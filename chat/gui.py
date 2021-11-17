import argparser
import threading
import tkinter as tk
import chat_client as gRPC_client
from chat_client import ChatData
import grpc
from proto_modules import chat_server_pb2_grpc as __pb2_grpc
from typing import List


# from argparser
NAME = argparser.NAME or 'DEFAULT NAME'
DEV = argparser.DEV

# gui.py doesn't work with chat_client.py when DEV mode
assert DEV == False

# send ping every _ seconds
PING_time = 0.1

CHATFORMAT = "[{:<3}]{:<20}({}) : {}"


class ChatGUI(tk.Tk):
    def __init__(self, _grpcClient) -> None:
        super().__init__()
        self.name = NAME
        self.id = 0
        self.grpcClient = _grpcClient
        self.setVars()
        self.guiSettings()
        self.setProtocol()

    def setVars(self):
        self.msgCount = 0
        self.msgCount_received = 0
        self.stubThread = None

    def guiSettings(self):

        self.title("gRPC Chat Room")

        self.msgShow_frame = tk.Frame(self)
        self.msgShow_frame.pack()

        self.msg_frame = tk.Frame(self.msgShow_frame)
        self.scrollbar = tk.Scrollbar(self.msg_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list = tk.Listbox(
            self.msg_frame, height=17,
            width=100,
        )
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.msg_list.pack()
        self.msg_list.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.configure(command=self.msg_list.yview)

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
        msg = self.my_msg.get()
        self.my_msg.set("")

        # when msgCount returned by SendMessage is larger then self.msgCount
        # it should call getMessage for update, but since self.stubHandler
        # calls PingRequest every PING_time, self.send doesn't do anything
        # but just sending a message
        self.msgCount_received = self.grpcClient.SendMessage(f'{msg}')

        if self.msgCount_received:
            self.msgCount_received = self.msgCount_received[0]
        else:
            self.quit()

        chatshown = CHATFORMAT.format(self.msgCount, self.name, self.id, msg)

        self.msgCount += 1
        self.msg_list.insert(self.msgCount, chatshown)
        self.msg_list.yview_moveto(1)

        # if msg == "{quit}":
        #     self.quit()

    def on_closing(self, event=None):
        self.my_msg.set("{quit}")
        self.send()

    # threading
    # receive, send ping, send message
    def stubHandler(self, ):
        msgCount, id = self.grpcClient.Login()

        self.id = id
        self.msgCount = msgCount
        self.msgCount_received = msgCount

        mcount = msgCount

        import time
        mem = time.time()

        while True:
            time.sleep(.1)
            if(PING_time < time.time() - mem):
                mcount = self.grpcClient.PingRequest()[0]
                mem = time.time()

            if(self.msgCount_received > self.msgCount or mcount > self.msgCount):
                msgs: List[ChatData] = self.grpcClient.GetMessage(
                    self.msgCount)

                for msg in msgs:
                    self.msg_list.insert(
                        msg.msgCOUNT,
                        CHATFORMAT.format(
                            msg.msgCOUNT, msg.user_name, msg.user_id, msg.msgCONTENT)
                    )
                    self.msg_list.yview_moveto(1)
                self.msgCount = self.msgCount + len(msgs)

    def run(self, ):
        self.stubThread = threading.Thread(target=self.stubHandler, )
        self.stubThread.daemon = True
        self.stubThread.start()

        self.mainloop()


if __name__ == '__main__':

    stub = __pb2_grpc.ChatServerStub
    channel = grpc.insecure_channel('localhost:50051')

    grpcClient = gRPC_client.MyChatClient(NAME, stub, channel)

    ChatGUI(grpcClient).run()
