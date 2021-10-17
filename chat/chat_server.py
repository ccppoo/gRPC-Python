from proto_modules import chat_server_pb2_grpc as __pb2_grpc
from proto_modules import chat_server_pb2 as __pb2
import grpc
from concurrent import futures

## Protocol Buffer Data : defined at /protos/*.proto ##

# chat_server.proto
Hello = __pb2.Hello
Ok = __pb2.Ok
Ping = __pb2.Ping
Pong = __pb2.Pong
State = __pb2.State

# message.proto
ChatMessages = __pb2.message__pb2.ChatMessages
Chat = __pb2.message__pb2.Chat

# user.proto
User = __pb2.user__pb2.User


class ChatServerPython(__pb2_grpc.ChatServerServicer):

    def __init__(self) -> None:
        super().__init__()
        self.chat_que = []
        self.users = set()

    def getMsgCount(self, ) -> int:
        return len(self.chat_que)

    # # message(Protocol buffer data) maker
    def makeUser(self, _name: str, _id: int = 0):
        return User(
            name=_name,
            id=_id
        )

    def makePong(self, ):
        print()
        print('::: Make Pong :::')
        return Pong(
            ok=self.makeOk(True, 42, 000),
            state=State.IDLE
        )

    def makeOk(self, valid: bool, msgCounf: int, id: int = 0):

        print()
        print('::: Make Ok :::')
        return Ok(
            ok=True,
            messageCount=self.getMsgCount(),
            id=id
        )

    def makeChatMessages(self, ):
        pass

    # # define methods from ChatServer service
    def Login(self, request: Hello, context) -> Ok:
        print()
        print("::: Login :::")

        print("request :: Hello :: User")
        print("User user.name : {}".format(request.user.name))
        print("User user.id : {}".format(request.user.id))

        _name, _id = request.user.name, request.user.id

        # invalid operation -> Login should only called for once
        if(_id != 0):
            return self.makeOk(False, _id)

        return self.makeOk(
            True,
            self.getMsgCount(),
            123
        )

    def PingRequest(self, request: Ping, context) -> Pong:
        print()
        print("::: PingRequest :::")

        print("request :: Ping :: User")
        print("User user.name : {}".format(request.user.name))
        print("User user.id : {}".format(request.user.id))

        print("request :: Ping :: messageCount")
        print("messageCount : {}".format(request.messageCount))

        return self.makePong()

    def GetMessage(self, request: Ok, context) -> ChatMessages:
        print()
        print("::: GetMessage :::")

        print("request :: ok")
        print("Ok ok : {}".format(request.ok))

        print("request :: messageCount")
        print("messageCount : {}".format(request.messageCount))

        print("request :: id")
        print("id : {}".format(request.id))

        li = []
        for i in range(5, 10):
            li.append(Chat(
                user=self.makeUser('naa_{}'.format(i), 123),
                message='hehe__{}'.format(i),
                messageCount=i
            ))

        chat_grpc = ChatMessages()
        chat_grpc.chatMessages.extend(li)
        # [chat_grpc.chatMessages.append(x) for x in li]

        return chat_grpc

    def SendMessage(self, request: ChatMessages, context) -> Ok:
        print()
        print("::: SendMessage :::")

        print("response :: ChatMessages :: Chat[]")
        msg = request.chatMessages[0]
        print("user_name : {}".format(msg.user.name))
        print("user_id : {}".format(msg.user.id))
        print("msgCount : {}".format(msg.messageCount))
        print("message : {}".format(msg.message))

        return self.makeOk(True, self.getMsgCount(), 999)


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    __pb2_grpc\
        .add_ChatServerServicer_to_server(
            ChatServerPython(), server
        )

    # gRPC는 http L7 상에서 작동하므로 포트를 오픈한다.
    server.add_insecure_port('[::]:50051')
    server.start()

    # test

    print('hello')
    server.wait_for_termination()

    server.stop(.5)


if __name__ == '__main__':
    serve()
