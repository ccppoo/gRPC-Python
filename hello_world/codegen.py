from grpc_tools import protoc

print("====================")
print("compile helloworld.proto")

result = protoc.main((
    '',
    '-I./protos',
    '--python_out=.',
    '--grpc_python_out=.',
    './protos/helloworld.proto',
))
