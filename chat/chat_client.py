import grpc

from proto_modules import chat_server_pb2 as __pb2
from proto_modules import chat_server_pb2_grpc as __pb2_grpc

import asyncio

# to activate : python chat_client.py --dev
from argparser import DEV

myChatClient = None


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
        self.stub = stub(channel)
        self.name = name
        self.id: int = 0
        self.msgCount: int = 0

    # # message(Protocol buffer data) maker

    def makeUser(self, ):
        return User(
            name=self.name,
            id=self.id
        )

    def makePing(self, ):
        return Ping(
            user=self.makeUser(),
            messageCount=self.msgCount
        )

    def makeOk(self, msgCount):

        self.msgCount
        return Ok(
            ok=True,
            messageCount=msgCount,
            id=self.id
        )

    # make one message per chat
    def makeChatMessages(self, msg: str):
        chat = Chat(
            user=self.makeUser(),
            message=msg,
            messageCount=self.msgCount
        )

        _chatMsg = ChatMessages()
        _chatMsg.chatMessages.append(chat)
        # _chatMsg.chatMessages.extend(chat)
        return _chatMsg

    # # override methods from ChatServer service

    def Login(self,) -> Ok:
        response: Ok = self.stub.Login(Hello(user=self.makeUser()))

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

    def PingRequest(self,) -> Pong:
        response: Pong = self.stub.PingRequest(self.makePing())

        _ok, state = response.ok, response.state

        if DEV:
            print()
            print(":::   PingRequest   :::")
            print("OK.ok : {}".format(_ok.ok))
            print("OK.messageCount : {}".format(_ok.messageCount))
            print("OK.id : {}".format(_ok.id))
            print("state : {}".format(state))
            print("::: end PingRequest :::")

        assert _ok.id == self.id

        if not DEV and _ok.messageCount > self.msgCount:
            self.GetMessage(self.msgCount)
            self.msgCount = _ok.messageCount

    def GetMessage(self, fromMsgCount: int = 0) -> ChatMessages:

        fromMsgCount = self.msgCount

        if DEV:
            fromMsgCount = 0
            # fromMsgCount = self.msgCount
        else:
            # in non-dev mode, it should not called directly
            assert fromMsgCount != 0
        response: ChatMessages = self.stub.GetMessage(
            self.makeOk(0))

        chats = response.chatMessages
        print("len(chats) : {}".format(len(chats)))

        if DEV:
            print()
            print(":::   GetMessage   :::")

        for msg in chats:
            msgcnt = msg.messageCount
            sender = msg.user.name
            sender_id = msg.user.id
            content = msg.message
            print("[{:3}] {:10}({}): {}".format(
                msgcnt, sender, sender_id, content))
        if DEV:
            print("::: end GetMessage :::")

        # update msgCount
        # print(len(chats))
        # self.msgCount = chats[-1].messageCount

    def SendMessage(self, msg: str) -> Ok:
        print("[{:3}] {:10}({}): {}".format(
            self.msgCount, self.name, self.id, msg))

        response: Ok = self.stub.SendMessage(self.makeChatMessages(msg))

        if DEV:
            print()
            print(":::   SendMessage   :::")
            print("OK.ok : {}".format(response.ok))
            print("messageCount : {}".format(response.messageCount))
            print("id : {}".format(response.id))
            print("::: end SendMessage :::")

        assert response.id == self.id

        if not DEV and response.messageCount > self.msgCount:
            self.GetMessage(self.msgCount)
            self.msgCount = response.messageCount


def run():
    stub = __pb2_grpc.ChatServerStub
    channel = grpc.insecure_channel('localhost:50051')

    if DEV:
        myChatClient = MyChatClient('DEV USER', stub, channel)
    else:
        name = input("User name : ")
        myChatClient = MyChatClient(name, stub, channel)

    # async def runClient():

    #     myChatClient.Login()

    #     while True:
    #         # send Ping every 0.5 second
    #         await asyncio.sleep(.1)
    #         myChatClient.PingRequest()
    #         value = await ainput("msg >> ")
    #         if value == 'stop':
    #             loop.stop()

    if DEV:
        myChatClient.Login()

        myChatClient.PingRequest()

        myChatClient.GetMessage()

        myChatClient.SendMessage(
            "Hello This is Client {}".format(myChatClient.msgCount))
    # else:
    #     loop = asyncio.get_event_loop()

    #     loop.run_until_complete(runClient())

    #     loop.run_forever()


if __name__ == '__main__':
    run()
