import grpc

from proto_modules import chat_server_pb2 as __pb2
from proto_modules import chat_server_pb2_grpc as __pb2_grpc

# to activate : python chat_client.py --dev
from argparser import DEV

from typing import List, NewType, Tuple
from dataclasses import dataclass

# Typing
USER_NAME = NewType('UserName', str)
USER_ID = NewType('UserId', int)
MSG_CONTENT = NewType('msgContent', str)
MSG_COUNT = NewType('msgCount', int)

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


@dataclass
class ChatData:
    msgCOUNT: int
    user_name: str
    user_id: int
    msgCONTENT: str

    def all(self) -> tuple:
        return self.msgCOUNT, self.user_name, self.user_id, self.msgCONTENT


class MyChatClient:

    def __init__(self, name: str, stub, channel) -> None:
        self.__channel = channel
        self.__stub = stub(channel)
        self.name = name
        self.id: int = 0
        self.msgCount: int = 0

    def __makeUser(self, ) -> User:
        """
        This method build `User` proto buffer object
        defined at `protos/user.proto`

        only used for (gRPC stub's server-side; this script)
        """
        return User(
            name=self.name,
            id=self.id
        )

    def __makePing(self, ) -> Ping:
        """
        This method build `Ping` proto buffer object
        defined at `protos/chat_server.proto`

        only used for (gRPC stub's server-side; this script)
        """
        return Ping(
            user=self.__makeUser(),
            messageCount=self.msgCount
        )

    def __makeOk(self, msgCount) -> Ok:
        """
        This method build `Ok` proto buffer object
        defined at `protos/chat_server.proto`

        only used for (gRPC stub's server-side; this script)
        """
        return Ok(
            ok=True,
            messageCount=msgCount,
            id=self.id
        )

    def __makeChatMessages(self, msg: str) -> ChatMessages:
        """
        This method build `ChatMessages` proto buffer object
        defined at `protos/message.proto`

        only used for (gRPC stub's server-side; this script)

        In this example, this is used only when
        sending message from chat-app client side
        """
        chat = Chat(
            user=self.__makeUser(),
            message=msg,
            messageCount=self.msgCount
        )

        _chatMsg = ChatMessages()
        _chatMsg.chatMessages.append(chat)
        # _chatMsg.chatMessages.extend(chat)
        return _chatMsg

    def Login(self,) -> Tuple[MSG_COUNT, USER_ID]:
        """
        defines method from ChatServer service

        send service::Login() defined at `chat_server.proto`

        returns 
            MSG_COUNT : int
            USER_ID : int

        this method is called only once when 
        called from GUI app(gRPC stub's client-side)
        """
        response: Ok = self.__stub.Login(Hello(user=self.__makeUser()))

        # save id from server's response
        self.id = response.id

        ok = response.ok
        msgCnt = response.messageCount
        id = response.id

        # update initial msgCount received from server
        self.msgCount = msgCnt

        return (msgCnt, id)

    def PingRequest(self,) -> Tuple[MSG_COUNT]:
        """
        defines method from ChatServer service

        send service::PingRequest() defined at `chat_server.proto`

        returns 
            MSG_COUNT : int

        this method is called to get latest message count at server 
        called from GUI app(gRPC stub's client-side)
        """

        response: Pong = self.__stub.PingRequest(self.__makePing())

        _ok, _state = response.ok, response.state

        _id, _msgCount = _ok.id, _ok.messageCount

        assert _ok.id == self.id

        return (_ok.messageCount, )

    def GetMessage(self, fromMsgCount: int = 0) -> List[ChatData]:
        """
        defines method from ChatServer service

        send service::GetMessage() defined at `chat_server.proto`

        returns 
            Iterable[Chatdata] : Iterable

        this method is called to get new messages from server
        called from GUI app(gRPC stub's client-side)

        GUI decides wheather to get new messages from server
        after receiving latest message count by calling `PingRequest`
        """

        assert fromMsgCount != 0

        # it returns as generator wraped with _MultiThreadedRendezvous
        # so we could use as iterable, iterating with for-loop
        response = self.__stub.GetMessage(self.__makeOk(fromMsgCount))

        sendLoad = []

        for m in response:
            sendLoad.append(
                ChatData(m.messageCount, m.user.name, m.user.id, m.message))

        return sendLoad

    def SendMessage(self, msg: str) -> Tuple[MSG_COUNT]:
        """
        defines method from ChatServer service

        send service::SendMessage() defined at `chat_server.proto`

        returns 
            MSG_COUNT : int

        this method is called to send new message from 
        GUI app(gRPC stub's client-side)
        """

        if msg == '{quit}':
            self.__SHUTDOWN()
            return

        response: Ok = self.__stub.SendMessage(self.__makeChatMessages(msg))

        assert response.id == self.id

        _ok, _msgCount, _id = response.ok, response.messageCount, response.id

        return (_msgCount, )

    def __SHUTDOWN(self,):
        self.__channel.close()
