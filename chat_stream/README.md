## changes from `chat` example

1. GetMessages now return `Chat` stream

   - `protos/chat_server.proto` service has changes

   - so `chat_client.py` :: class MyChatClient :: GetMessages has changes

2. Removed DEV, CLI case at `chat_client.py`

   - it would be more clear to manipulate code, only concerning as gRPC::stub server side

3. added comment for more clear explaination

4. added more stream like example

# 3-1. Chat with stream

Usage:

First, Start server

```
path/to/GRPC-PYTHON-QUICKSTART/chat_stream> python chat_server.py
```

Then, run multiple client(GUI)

```
path/to/GRPC-PYTHON-QUICKSTART/chat_stream> python gui.py <YOUR_NICK_NAME>
```

# 3-2. Chat with stream (more stream like usage)

Usage:

First, Start server

```
path/to/GRPC-PYTHON-QUICKSTART/chat_stream> python chat_server.py
```

Then, run multiple client(GUI)

doesn't matter with running with 2-1 `gui.py`

```
path/to/GRPC-PYTHON-QUICKSTART/chat_stream> python gui_2.py <YOUR_NICK_NAME>
```

## summary

After receiving stream at stub, **it's all python stuff**.

note the small changes between `chat_client.py` vs `chat_client_2.py`

```py
# chat_client.py
def GetMessage(self, fromMsgCount: int = 0) -> Iterable[ChatData]:
    ...
    response = self.__stub.GetMessage(self.__makeOk(fromMsgCount))

    sendLoad = []
    for m in response:
        sendLoad.append(
            ChatData(m.messageCount, m.user.name, m.user.id, m.message))

    return sendLoad
```

```py
# chat_client_2.py
def GetMessage(self, fromMsgCount: int = 0) -> Iterable[ChatData]:
    ...
    response = self.__stub.GetMessage(self.__makeOk(fromMsgCount))

    for m in response:
        yield ChatData(m.messageCount, m.user.name, m.user.id, m.message)
    return
```

and

`gui.py` vs `gui_2.py`

```py
# gui.py
def stubHandler(self, ):
    ...
    msgs: List[ChatData] = self.grpcClient.GetMessage(self.msgCount)

    for msg in msgs:
        self.msg_list.insert(
            msg.msgCOUNT,
            CHATFORMAT.format(*msg.all())
        )
        self.msg_list.yview_moveto(1)
    self.msgCount = self.msgCount + len(msgs)
```

```py
# gui_2.py
def stubHandler(self, ):
    ...
    msgs: Iterable[ChatData] = self.grpcClient.GetMessage(self.msgCount)
    count = 0
    for msg in msgs:
        self.msg_list.insert(
            msg.msgCOUNT,
            CHATFORMAT.format(*msg.all())
        )
        self.msg_list.yview_moveto(1)
        count += 1
    self.msgCount = self.msgCount + count
```

Just like case 2-1, you could use it after receiving data from gRPC server side's stream

receiving all data after looping for-loop. (_sync + blocking_)

In case 2-2, you could use like generator. (_sync + non-blocking_)

you could implement threading, event-base,

depending on the design, or the expected time it would cost at gRPC server side
