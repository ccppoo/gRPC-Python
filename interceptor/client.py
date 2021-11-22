import grpc
from proto_modules.utils_pb2 import Ping, Pong
from proto_modules.interceptSample_pb2 import Load
from proto_modules.interceptSample_pb2_grpc import SecureMessageStub

from interceptors.client.encodeInterceptor import EncodeInterceptor
from interceptors.client.messageFormatInterceptor import MessageFormatInterceptor


class InterceptClient:

    def __init__(self, stub) -> None:
        self.__stub = stub

    def __buildPing(self, message: str = "ping") -> Ping:

        return Ping(value=message)

    def __buildLoad(self, message: str) -> Load:

        return Load(value=message)

    def sendPing(self, ) -> str:
        ping = self.__buildPing("Ping")

        response: Pong = self.__stub.PingRequest(ping)
        return response.value

    def sendMessage(self, ) -> str:

        load = self.__buildLoad("hello")

        response: Load = self.__stub.sendMessage(load)

        return response.value


def run():
    channel = grpc.insecure_channel('localhost:50051')

    formatInterceptor = MessageFormatInterceptor()
    encodeInterceptor = EncodeInterceptor()

    _interceptChannel = grpc.intercept_channel(
        channel, formatInterceptor, encodeInterceptor)

    stub = SecureMessageStub(_interceptChannel)

    interceptClient = InterceptClient(stub)

    response = interceptClient.sendPing()
    print(response)

    response: str = interceptClient.sendMessage()
    print(response)


if __name__ == '__main__':
    run()
