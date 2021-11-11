import time
from proto_modules import chat_server_pb2_grpc as __pb2_grpc
from proto_modules import chat_server_pb2 as __pb2
import grpc
from concurrent import futures

# to activate : python chat_server.py --dev
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--dev", help="enables dev mode", action="store_true")
args = parser.parse_args()
if args.dev:
    DEV = True
else:
    DEV = False

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

mem = time.time()


class ChatServerPython(__pb2_grpc.ChatServerServicer):
    # ##### METHOD NAMING RULES #####
    #
    # get~, add~ : method for program logic, nothing to do with gRPC
    # make~ : mathod for making proto message buffer
    # others : overriding method defined from chat_server.proto :: service ChatServer

    """
    Methods are overrided from ChatServerServicer class
    Methods are declared in proto_modules/chat_server.proto 'service ChatServer'
    """

    def __init__(self) -> None:
        super().__init__()
        self.chat_que = []
        self.users = dict()
        self.userCnt = 0

        self.chat_que.append({
            'user': "SERVER",
            'msg': "SERVER INIT"
        })

    def getMsgCount(self, ) -> int:
        return len(self.chat_que)

    def addNewUser(self, name) -> int:
        self.userCnt += 1
        self.users[name] = self.userCnt

        return self.userCnt

    def getUserByID(self, userID: int) -> str:
        for name, id in self.users.items():
            if(id == userID):
                return name
        else:
            return ''

    # # message(Protocol buffer data) maker
    def makeUser(self, _name: str, _id: int = 0) -> User:

        if (_id != 0):
            return User(
                name=_name,
                id=_id
            )

        return User(
            name=_name,
            id=self.users.get(_name)
        )

    def makePong(self, UserMsgCount: int, id: int) -> Pong:

        st = State.IDLE if UserMsgCount == self.getMsgCount() else State.BUSY

        return Pong(
            ok=self.makeOk(True,  id),
            state=st
        )

    def makeOk(self, valid: bool, id: int = 0) -> Ok:
        # while sending Ok proto buff from Server,
        # there are no reason to get msgCount from callee
        # always need to send latest value to client

        return Ok(
            ok=valid,
            messageCount=self.getMsgCount(),
            id=id
        )

    def makeChatMessages(self, UserMsgCount: int):
        chat_list = []

        for i, ch in enumerate(self.chat_que[UserMsgCount:]):

            chat_list.append(Chat(
                user=self.makeUser(ch['user']),
                message=ch['msg'],
                messageCount=UserMsgCount + i
            ))

        _chatMsg = ChatMessages()
        _chatMsg.chatMessages.extend(chat_list)

        return _chatMsg

    # # define methods from ChatServer service
    def Login(self, request: Hello, context) -> Ok:

        name: str = request.user.name
        id: int = request.user.id

        if DEV:
            print()
            print(":::   Login   :::")
            print("From: {}({})".format(name, id))
            print("::: end Login :::")

        # invalid operation 1 -> Login should only called for once
        if(id != 0):
            return self.makeOk(False, id)

        # invalid operation 2 -> User nick name used before
        #                 or client restarted with same nickname used before
        if(name in self.users):
            return self.makeOk(False, self.users[name])

        return self.makeOk(
            True,
            self.addNewUser(name)
        )

    def PingRequest(self, request: Ping, context) -> Pong:

        name: str = request.user.name
        id: int = request.user.id
        msgCnt: int = request.messageCount

        global mem

        if(3 < time.time() - mem):
            print(f"CURRENT MSG_COUNT : {self.getMsgCount()}")
            mem = time.time()

        if DEV:
            print()
            print(":::   PingRequest   :::")
            print("From: {}({})".format(name, id))
            print("user messageCount: {} / delay: {}".
                  format(msgCnt, self.getMsgCount()-msgCnt))
            print("::: end PingRequest :::")

        return self.makePong(msgCnt, id)

    def GetMessage(self, request: Ok, context) -> ChatMessages:

        ok: bool = request.ok
        id: int = request.id
        msgCnt: int = request.messageCount

        if DEV:
            print()
            print(":::   GetMessage   :::")
            print("ok: {}".format(ok))
            print("From: {}({})".format(self.getUserByID(id), id))
            print("user messageCount: {} / delay: {}".
                  format(msgCnt, self.getMsgCount()-msgCnt))
            print("::: end GetMessage :::")

        return self.makeChatMessages(msgCnt)

    def SendMessage(self, request: ChatMessages, context) -> Ok:

        _msg: Chat = request.chatMessages[0]

        name: str = _msg.user.name
        id: int = _msg.user.id
        msgCnt: int = _msg.messageCount
        msg: str = _msg.message

        if DEV:
            print()
            print(":::   SendMessage   :::")
            print("From: {}({})".format(name, id))
            print("user messageCount: {} / delay: {}".
                  format(msgCnt, self.getMsgCount()-msgCnt))
            print("content: {}".format(msg))
            print("::: end SendMessage :::")

        self.chat_que.append({
            'user': name,
            'msg': msg
        })

        return self.makeOk(True, id)


def serve():
    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10)
    )

    __pb2_grpc.add_ChatServerServicer_to_server(
        ChatServerPython(), server
    )

    # gRPC는 http L7 상에서 작동하므로 포트를 오픈한다.
    server.add_insecure_port('[::]:50051')
    server.start()

    # test
    server.wait_for_termination()

    server.stop(.5)


if __name__ == '__main__':
    serve()
