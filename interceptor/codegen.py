from grpc_tools import protoc

print("====================")
print("compile interceptSample.proto")

result = protoc.main((
    '',
    '-I./protos',
    '--python_out=./proto_modules',
    '--grpc_python_out=./proto_modules',
    './protos/interceptSample.proto',
))

print()
print("compile utils.proto")

protoc.main((
    '',
    '-I./protos',
    '--python_out=./proto_modules',
    './protos/utils.proto'
))

print("====================")
