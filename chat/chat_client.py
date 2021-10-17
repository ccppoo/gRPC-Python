import grpc

from proto_modules import chat_server_pb2 as __pb2
from proto_modules import chat_server_pb2_grpc as __pb2_grpc

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

    def makeOk(self, ):
        return Ok(
            ok=True,
            messageCount=self.msgCount,
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

    def Login(self) -> Ok:
        response: Ok = self.stub.Login(Hello(user=self.makeUser()))

        # set id from server's response
        self.id = response.id

        print()
        print("::: Login :::")

        a, b, c = response.ok, response.messageCount, response.id

        print("response :: Ok :: ok")
        print("OK.ok : {}".format(a))

        print("response :: messageCount")
        print("messageCount : {}".format(b))

        print("response :: id")
        print("id : {}".format(c))

    def PingRequest(self,) -> Pong:
        response: Pong = self.stub.PingRequest(self.makePing())

        a, b = response.ok, response.state

        print()
        print("::: PingRequest :::")

        print("response :: Pong :: ok")
        print("OK.ok : {}".format(a.ok))
        print("OK.messageCount : {}".format(a.messageCount))
        print("OK.id : {}".format(a.id))

        print("response :: Pong :: state")
        print("state : {}".format(b))

    def GetMessage(self, ) -> ChatMessages:
        response: ChatMessages = self.stub.GetMessage(self.makeOk())

        a = response.chatMessages

        print()
        print("::: GetMessage :::")

        print("response :: ChatMessages :: Chat[]")

        for msg in response.chatMessages:
            print()
            print("user_name : {}".format(msg.user.name))
            print("user_id : {}".format(msg.user.id))
            print("msgCount : {}".format(msg.messageCount))
            print("message : {}".format(msg.message))

    def SendMessage(self, msg: str) -> Ok:
        response: Ok = self.stub.SendMessage(self.makeChatMessages(msg))

        print()
        print("::: SendMessage :::")

        print("response :: Ok :: ok")
        print("OK.ok : {}".format(response.ok))

        print("response :: messageCount")
        print("messageCount : {}".format(response.messageCount))

        print("response :: id")
        print("id : {}".format(response.id))


def run():
    stub = __pb2_grpc.ChatServerStub
    channel = grpc.insecure_channel('localhost:50051')
    myChatClient = MyChatClient('ccppoo', stub, channel)

    myChatClient.Login()

    myChatClient.PingRequest()

    myChatClient.GetMessage()

    myChatClient.SendMessage("Hello This is Client")


if __name__ == '__main__':
    run()
