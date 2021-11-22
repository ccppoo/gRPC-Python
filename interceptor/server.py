import grpc
from concurrent import futures
from proto_modules.utils_pb2 import Ping, Pong
from proto_modules.interceptSample_pb2 import Load, Num
from proto_modules.interceptSample_pb2_grpc import add_SecureMessageServicer_to_server, SecureMessageServicer

from typing import Iterable

from interceptors.server.decodeInterceptor import DecodeInterceptor


class MsgServer(SecureMessageServicer):
    def __init__(self) -> None:
        super().__init__()

    def PingRequest(self, request: Ping, context) -> Pong:
        print("ping request got!!")
        return Pong(value="hello")

    def sendMessage(self, request: Load, context) -> Load:
        return Load(value="I am server")

    def addTheseNumbers(self, request: Iterable[Num], context) -> Num:

        return


def serve():

    decodeInterceptor = DecodeInterceptor()

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=(decodeInterceptor, ))

    add_SecureMessageServicer_to_server(MsgServer(), server)

    server.add_insecure_port('[::]:50051')

    server.start()

    server.wait_for_termination()
    server.stop(.5)


if __name__ == '__main__':
    serve()
