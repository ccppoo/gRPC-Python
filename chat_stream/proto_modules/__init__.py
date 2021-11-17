# proto modules 내 작성된 모듈(user_pb2.py, message_pb2.py, ...)이 생성될 때
# 상대 경로로 import가 되어있으므로 다른 py 스크립트에서 정상적으로 import 하기 위해서 경로를 추가한다.

#  chat_server_pb2_grpc.py 에 import chat_server_pb2 as chat__server__pb2 부분을
# from . import chat_server_pb2 as chat__server__pb2 처럼 "from ."을 추가해 상대 경로를 지정할 수 있지만,
# gRPC 파이썬 스크립트를 생성할 때마다 작성하기 귀찮으므로 아래와 같이 경로를 추가한다.
import sys
sys.path.append('proto_modules')
