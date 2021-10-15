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
#        changed file name greeter_client.py -> client.py
"""The Python implementation of the GRPC helloworld.Greeter client."""

from __future__ import print_function

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


# using class
class MyClient:

    def __init__(self, stub, channel):
        self.stub = stub(channel)

    def SayHello(self, name_: str):
        response = self.stub.SayHello(helloworld_pb2.HelloRequest(name=name_))
        print("Greeter client received: " + response.message)


# original example
def run():

    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        response = stub.SayHello(helloworld_pb2.HelloRequest(name='ccppoo'))

    # response는 helloworld.proto에서 정의한 message HelloReply buffer data이며,
    # 필드에는 미리 정의한 string message가 있기 때문에 아래와 같이 참조가 가능하다.
    print("Greeter client received: " + response.message)

    # help(response) 를 하면...
    # HelloReply
    # google.protobuf.pyext._message.CMessage
    # google.protobuf.message.Message
    # builtins.object
    # 순으로 MRO가 되어 있는 것을 볼 수 있다.


if __name__ == '__main__':

    # run()

    import asyncio

    channel = grpc.insecure_channel('localhost:50051')
    stub = helloworld_pb2_grpc.GreeterStub
    mc = MyClient(stub, channel)

    name = ['ccppoo', 'posix', 'linux', 'Kotlin', 'Java', 'cpp']

    async def sendRandomName(handler):
        for n in name:
            mc.SayHello(name_=n)
            await asyncio.sleep(1.0)
        handler.stop()

    loop = asyncio.get_event_loop()

    try:
        asyncio.ensure_future(sendRandomName(loop))
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        print("Closing Loop")
        loop.close()
