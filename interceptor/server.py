import grpc
from concurrent import futures
from proto_modules.utils_pb2 import Ping, Pong
from proto_modules.interceptSample_pb2 import Load, Num
from proto_modules.interceptSample_pb2_grpc import add_SecureMessageServicer_to_server, SecureMessageServicer
from grpc._server import _Context as Context

from typing import Iterable

from interceptors.server.headerInterceptor import HeaderInterceptor


class MsgServer(SecureMessageServicer):
    def __init__(self) -> None:
        super().__init__()

    def PingRequest(self, request: Ping, context: Context) -> Pong:

        return Pong(value="hello")

    def sendMessage(self, request: Load, context: Context) -> Load:

        return Load(value=f"you send : {request.value}")

    def addTheseNumbers(self, request_stream: Iterable[Num], context: Context) -> Num:

        val = 0

        for request in request_stream:
            val += request.value

        return Num(value=val)


def serve():

    headerInterceptor = HeaderInterceptor()

    server = grpc.server(
        futures.ThreadPoolExecutor(max_workers=10),
        interceptors=(headerInterceptor, ))

    '''
    # handlers 인자
        server( ... ,handlers = <여기>)
        Generic Handler 추가할 때 추가하는 거:
            https://grpc.github.io/grpc/python/grpc.html#grpc.method_handlers_generic_handler
        
        # options 인자
        C Define 매크로 옆에 설명대로 하면된다.
        https://github.com/grpc/grpc/blob/cd9730d2d28626c57431253208f23507d466c825/include/grpc/impl/codegen/grpc_types.h#L140-L448
        https://grpc.github.io/grpc/python/glossary.html#term-channel_arguments
        
        예) tcp 포트 재사용 X 인 경우 : (('grpc.so_reuseport', 0),)
        
        여러 옵션을 사용하는 경우, 튜플의 튜플로 만들면 됨
    
    # maximum concurrent rpcs 인자
        최대로 동시 처리 가능한 rpc개수,
        인자로 넣은 정수 이상일 경우 RESOURCE_EXHAUSTED 상태 반환
        

    # compression 인자
        https://grpc.github.io/grpc/python/grpc.html#grpc.Compression
        grpc.Compression.NoCompression, Gzip, Deflate
        셋 중 하나 사용하면 된다.
        
    # xds 인자 (xDS, envoy 기능 이용하는 것)
           xds=False    
    '''

    add_SecureMessageServicer_to_server(MsgServer(), server)

    # server.add_generic_rpc_handlers 이게 뭘까?

    server.add_insecure_port('[::]:50051')

    server.start()

    server.wait_for_termination()
    server.stop(.5)


if __name__ == '__main__':
    serve()
