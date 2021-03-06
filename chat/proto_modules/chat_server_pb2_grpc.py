# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

import chat_server_pb2 as chat__server__pb2
import message_pb2 as message__pb2


class ChatServerStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.Login = channel.unary_unary(
                '/chating.server.ChatServer/Login',
                request_serializer=chat__server__pb2.Hello.SerializeToString,
                response_deserializer=chat__server__pb2.Ok.FromString,
                )
        self.PingRequest = channel.unary_unary(
                '/chating.server.ChatServer/PingRequest',
                request_serializer=chat__server__pb2.Ping.SerializeToString,
                response_deserializer=chat__server__pb2.Pong.FromString,
                )
        self.GetMessage = channel.unary_unary(
                '/chating.server.ChatServer/GetMessage',
                request_serializer=chat__server__pb2.Ok.SerializeToString,
                response_deserializer=message__pb2.ChatMessages.FromString,
                )
        self.SendMessage = channel.unary_unary(
                '/chating.server.ChatServer/SendMessage',
                request_serializer=message__pb2.ChatMessages.SerializeToString,
                response_deserializer=chat__server__pb2.Ok.FromString,
                )


class ChatServerServicer(object):
    """Missing associated documentation comment in .proto file."""

    def Login(self, request, context):
        """add new user to server, Ok message with new User id
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def PingRequest(self, request, context):
        """ping method :: ask new messages to server
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def GetMessage(self, request, context):
        """contains chat message 
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendMessage(self, request, context):
        """send message from client to server
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ChatServerServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'Login': grpc.unary_unary_rpc_method_handler(
                    servicer.Login,
                    request_deserializer=chat__server__pb2.Hello.FromString,
                    response_serializer=chat__server__pb2.Ok.SerializeToString,
            ),
            'PingRequest': grpc.unary_unary_rpc_method_handler(
                    servicer.PingRequest,
                    request_deserializer=chat__server__pb2.Ping.FromString,
                    response_serializer=chat__server__pb2.Pong.SerializeToString,
            ),
            'GetMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.GetMessage,
                    request_deserializer=chat__server__pb2.Ok.FromString,
                    response_serializer=message__pb2.ChatMessages.SerializeToString,
            ),
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=message__pb2.ChatMessages.FromString,
                    response_serializer=chat__server__pb2.Ok.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'chating.server.ChatServer', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class ChatServer(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def Login(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chating.server.ChatServer/Login',
            chat__server__pb2.Hello.SerializeToString,
            chat__server__pb2.Ok.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def PingRequest(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chating.server.ChatServer/PingRequest',
            chat__server__pb2.Ping.SerializeToString,
            chat__server__pb2.Pong.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def GetMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chating.server.ChatServer/GetMessage',
            chat__server__pb2.Ok.SerializeToString,
            message__pb2.ChatMessages.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/chating.server.ChatServer/SendMessage',
            message__pb2.ChatMessages.SerializeToString,
            chat__server__pb2.Ok.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
