from typing import NewType
import time
from proto_modules import chat_server_pb2_grpc as __pb2_grpc
from proto_modules import chat_server_pb2 as __pb2
import grpc
from concurrent import futures
from typing import Iterable

from collections.abc import Iterable


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

# Stream Chat
StreamOf = NewType('StreamOf', tuple)


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
        """
        This method build `User` proto buffer object
        defined at `protos/user.proto`

        return
            User
        """

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
        """
        This method build `Pong` proto buffer object
        defined at `protos/chat_server.proto`

        return
            Pong
        """

        st = State.IDLE if UserMsgCount == self.getMsgCount() else State.BUSY

        return Pong(
            ok=self.makeOk(True,  id),
            state=st
        )

    def makeOk(self, valid: bool, id: int = 0) -> Ok:
        """
        This method build `Ok` proto buffer object
        defined at `protos/chat_server.proto`

        return
            Ok
        """

        return Ok(
            ok=valid,
            messageCount=self.getMsgCount(),
            id=id
        )

    def makeChatStream(self, UserMsgCount: int) -> Iterable[Chat]:
        """
        Returns iterable object(working as stream)
        gRPC library side fulfills when returning protobuf as Iterable

        return
            Iterable[Chat]
        """

        for i, ch in enumerate(self.chat_que[UserMsgCount:]):

            chat2client = Chat(
                user=self.makeUser(ch['user']),
                message=ch['msg'],
                messageCount=UserMsgCount + i
            )

            yield chat2client

    # # define methods from ChatServer service
    def Login(self, request: Hello, context) -> Ok:
        """
        Override method from ChatServer service

        send service::Login() defined at `chat_server.proto`

        returns 
            Ok
        """

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
        """
        Override method from ChatServer service

        send service::PingRequest() defined at `chat_server.proto`

        returns 
            Pong
        """

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

    def GetMessage(self, request: Ok, context) -> Iterable[Chat]:
        """
        Override method from ChatServer service

        send service::GetMessage() defined at `chat_server.proto`

        returns
            Iterable[Chat]
        """

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

        # in case of stream, it should return as generator
        # gRPC will take care of rest of it
        return self.makeChatStream(msgCnt)

    def SendMessage(self, request: ChatMessages, context) -> Ok:
        """
        Override method from ChatServer service

        send service::SendMessage() defined at `chat_server.proto`

        returns
            Ok
        """

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

    server.wait_for_termination()

    server.stop(.5)


if __name__ == '__main__':
    serve()
