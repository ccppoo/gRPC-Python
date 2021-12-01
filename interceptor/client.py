import grpc
from proto_modules.interceptSample_pb2 import Num
from proto_modules.utils_pb2 import Ping, Pong
from proto_modules.interceptSample_pb2 import Load
from proto_modules.interceptSample_pb2_grpc import SecureMessageStub

from interceptors.client.headerInterceptor import HeaderInterceptor
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

    def sendNumbers(self, ) -> int:

        # could send as generator
        response: Num = self.__stub.addTheseNumbers(
            (Num(value=n) for n in range(1, 11)))

        # or send after making iterable
        # response: Num = self.__stub.addTheseNumbers(
        #     iter([Num(value=n) for n in range(1, 11)]))

        return response.value


def run():
    channel = grpc.insecure_channel('localhost:50051')

    formatInterceptor = MessageFormatInterceptor()
    headerInterceptor = HeaderInterceptor()

    _interceptChannel = grpc.intercept_channel(
        channel, formatInterceptor, headerInterceptor)

    stub = SecureMessageStub(_interceptChannel)

    interceptClient = InterceptClient(stub)

    response = interceptClient.sendPing()
    print(f'response from sendPing : {response}')

    response: str = interceptClient.sendMessage()
    print(f'response from sendMessage : {response}')

    response = interceptClient.sendNumbers()
    print(f'response from sendNumbers : {response}')


if __name__ == '__main__':
    run()
