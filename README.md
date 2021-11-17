# gRPC-Python-QuickStart

clean gRPC-Python start kit

Simple working exmample for Python gRPC

Because [example](https://github.com/grpc/grpc) given from the
[gRPC offical site](https://grpc.io/docs/languages/python/quickstart/) is too large to handle for those who just want to make with python.

I will add my own sample and also cover most of the examples from [gRPC repository](https://github.com/grpc/grpc/tree/master/examples/python)

## 1. Hello World - from [gRPC/gRPC](https://github.com/grpc/grpc)

Basic example from [gRPC/gRPC](https://github.com/grpc/grpc)

![hello_world_image](./hello_world/images/preview.PNG)

## 2. chat with GUI [chat](./chat/README.md)

Using basic gRPC server and client(Sync) with GUI(tkinter)

![chat_example_image](./chat/images/gRPC_chat.gif)

## 3. chat with GUI [chat_stream](./chat_stream/README.md)

Use same GUI script(gui.py) but use streaming connection

Changes from `2.chat with GUI`

1. GetMessages now return `Chat` stream

   - `protos/chat_server.proto` service has changes

   - so `chat_client.py` :: class MyChatClient :: GetMessages has changes

2. Removed DEV, CLI case at `chat_client.py`

   - it would be more clear to manipulate code, only concerning as gRPC::stub server side

3. added comment for more clear explaination

4. added more stream like example

   - read more about `chat_client_2.py`, `gui_2.py` at [chat_stream README](./chat_stream/README.md)
