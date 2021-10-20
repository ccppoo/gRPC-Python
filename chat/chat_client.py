import grpc

from proto_modules import chat_server_pb2 as __pb2
from proto_modules import chat_server_pb2_grpc as __pb2_grpc

import asyncio

# to activate : python chat_client.py --dev
from argparser import DEV

from typing import NewType

# Typing
USER_NAME = NewType('UserName', str)
USER_ID = NewType('UserId', int)
msgCONTENT = NewType('msgContent', str)
msgCOUNT = NewType('msgCount', int)

# globals
myChatClient = None

CLI = __name__ == '__main__'
GUI = not CLI and __name__ == 'chat_client'

## Protocol Buffer Data : defined at /protos/*.proto ##

# chat_server.proto
Hello = __pb2.Hello
Ok = __pb2.Ok
Ping = __pb2.Ping
Pong = __pb2.Pong

# message.proto
ChatMessages = __pb2.message__pb2.ChatMessages
Chat = __pb2.message__pb2.Chat

# user.proto
User = __pb2.user__pb2.User


class MyChatClient:

    def __init__(self, name: str, stub, channel) -> None:
        self.__channel = channel
        self.__stub = stub(channel)
        self.name = name
        self.id: int = 0
        self.msgCount: int = 0

    # # message(Protocol buffer data) maker

    def __makeUser(self, ) -> User:
        return User(
            name=self.name,
            id=self.id
        )

    def __makePing(self, ) -> Ping:
        return Ping(
            user=self.__makeUser(),
            messageCount=self.msgCount
        )

    def __makeOk(self, msgCount) -> Ok:
        return Ok(
            ok=True,
            messageCount=msgCount,
            id=self.id
        )

    # make one message per chat
    def __makeChatMessages(self, msg: str) -> ChatMessages:
        chat = Chat(
            user=self.__makeUser(),
            message=msg,
            messageCount=self.msgCount
        )

        _chatMsg = ChatMessages()
        _chatMsg.chatMessages.append(chat)
        # _chatMsg.chatMessages.extend(chat)
        return _chatMsg

    # # override methods from ChatServer service

    # send : OK // get : Hello
    def Login(self,) -> tuple([msgCOUNT, USER_ID]):
        response: Ok = self.__stub.Login(Hello(user=self.__makeUser()))

        # save id from server's response
        self.id = response.id

        ok = response.ok
        msgCnt = response.messageCount
        id = response.id

        if DEV:
            print()
            print(":::   Login   :::")
            print("ok : {}".format(ok))
            print("messageCount : {}".format(msgCnt))
            print("id : {}".format(id))
            print("::: end Login :::")

        # update initial msgCount received from server
        self.msgCount = msgCnt

        return (msgCnt, id)

    # send : Pong // get : Ping
    def PingRequest(self,) -> tuple([msgCOUNT]):
        response: Pong = self.__stub.PingRequest(self.__makePing())

        _ok, _state = response.ok, response.state

        _id, _msgCount = _ok.id, _ok.messageCount

        assert _ok.id == self.id

        if DEV:
            print()
            print(":::   PingRequest   :::")
            print("OK.ok : {}".format(_ok.ok))
            print("OK.messageCount : {}".format(_msgCount))
            print("OK.id : {}".format(_id))
            print("state : {}".format(_state))
            print("::: end PingRequest :::")

        if CLI and _msgCount > self.msgCount:
            self.msgCount, oldMsgCount = _msgCount, self.msgCount
            self.GetMessage(oldMsgCount)

        # In case of GUI mode, GUI decides when to call GetMessage
        if GUI:
            return (_ok.messageCount, )

    # send : Ok // get : ChatMessages

    def GetMessage(self, fromMsgCount: int = 0) -> \
            list((msgCOUNT, USER_NAME, USER_ID, msgCONTENT)):

        if DEV:
            fromMsgCount = 0
            # fromMsgCount = self.msgCount
        if CLI:
            # in CLI mode, this method should not called directly
            # this should be called by following order :
            #                           PingRequest -> GetMessage
            fromMsgCount = self.msgCount
        if CLI or GUI:
            assert fromMsgCount != 0

        response: ChatMessages = self.__stub.GetMessage(
            self.__makeOk(fromMsgCount)
        )

        # ! chatMessages is consumable like generator
        chats = response.chatMessages

        if GUI:
            return [
                (m.messageCount, m.user.name, m.user.id, m.message)
                for m in chats
            ]

        if DEV:
            print()
            print("len(chats) : {}".format(len(chats)))
            print(":::   GetMessage   :::")

        if DEV or CLI:
            for msg in chats:
                msgcnt = msg.messageCount
                sender = msg.user.name
                sender_id = msg.user.id
                content = msg.message
                print("[{:3}] {:10}({}): {}".format(
                    msgcnt, sender, sender_id, content))

        if DEV:
            print("::: end GetMessage :::")

    # send : ChatMessages // get : Ok
    def SendMessage(self, msg: str) -> tuple([msgCOUNT]):

        if msg == '{quit}' or (CLI or DEV and msg == 'exit'):
            self.__SHUTDOWN()
            return

        if CLI:
            print("[{:3}] {:10}({}): {}".format(
                self.msgCount, self.name, self.id, msg))

        response: Ok = self.__stub.SendMessage(self.__makeChatMessages(msg))

        assert response.id == self.id

        _ok, _msgCount, _id = response.ok, response.messageCount, response.id

        if DEV:
            print()
            print(":::   SendMessage   :::")
            print("OK.ok : {}".format(_ok))
            print("messageCount : {}".format(_msgCount))
            print("id : {}".format(_id))
            print("::: end SendMessage :::")
            return

        if CLI and _msgCount > self.msgCount:
            self.GetMessage(self.msgCount)
            self.msgCount = _msgCount

        if GUI:
            return (_msgCount, )

        return _msgCount

    def __SHUTDOWN(self,):
        self.__channel.close()


def run():
    stub = __pb2_grpc.ChatServerStub
    channel = grpc.insecure_channel('localhost:50051')

    if DEV:
        myChatClient = MyChatClient('DEV USER', stub, channel)

        myChatClient.Login()

        myChatClient.PingRequest()

        myChatClient.GetMessage()

        myChatClient.SendMessage(
            "Hello This is Client {}".format(myChatClient.msgCount))

    name = input("User name : ")
    myChatClient = MyChatClient(name, stub, channel)


if __name__ == '__main__':
    run()
