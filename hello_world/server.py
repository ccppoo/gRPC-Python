# Copyright 2015 gRPC authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# NOTE : removed comments that existed, added new comment in Korean
#        changed file name greeter_server.py -> server.py
"""The Python implementation of the GRPC helloworld.Greeter server."""

from concurrent import futures

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


class Greeter(helloworld_pb2_grpc.GreeterServicer):
    # helloworld_pb2_grpc.py :: GreeterServicer 에서 상속을 받는다.
    # helloworld_pb2_grpc.py :: GreeterServicer는 abstract class 와 같으며,
    # helloworld.proto에 정의된 service에 있는 rpc 인터페이스를 재정의 해야한다.
    def SayHello(self, request, context):
        return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))

    # 위에 생성한 Greeter()는 gRPC의 C++ 엔진이 돌아갈 수 있도록 하는 장치와 같다.
    # (C++ 로 만들어진 C++를 조작하기 위한 python으로 만들어진 인터페이스와 같은 개념)
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)

    # gRPC는 http L7 상에서 작동하므로 포트를 오픈한다.
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
