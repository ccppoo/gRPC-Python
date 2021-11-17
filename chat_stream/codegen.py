from grpc_tools import protoc

# python -m grpc_tools.protoc -I./protos --proto_path=. --python_out=.  --grpc_python_out=. ./protos/*.proto

print("====================")
print("compile user.proto")

result = protoc.main((
    '',
    '-I./protos',
    '--python_out=./proto_modules',
    './protos/user.proto'
))

print()
print("compile message.proto")

protoc.main((
    '',
    '-I./protos',
    '--python_out=./proto_modules',
    './protos/message.proto'
))

print()
print("compile message.proto")

protoc.main((
    '',
    '-I./protos',
    '--python_out=./proto_modules',
    '--grpc_python_out=./proto_modules',
    './protos/chat_server.proto'
))

print("====================")

# check for import generated code's import working
