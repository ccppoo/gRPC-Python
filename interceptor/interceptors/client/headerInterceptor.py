from grpc import UnaryUnaryClientInterceptor, StreamUnaryClientInterceptor, ClientCallDetails
from collections import namedtuple


class _ClientCallDetails(
        namedtuple(
            '_ClientCallDetails',
            ('method', 'timeout', 'metadata', 'credentials', 'wait_for_ready', 'compression')),
        ClientCallDetails):
    pass


class HeaderInterceptor(UnaryUnaryClientInterceptor, StreamUnaryClientInterceptor):
    def __init__(self) -> None:
        self.key = 'grpc'
        self.value = 'I am client'
        super().__init__()

    def add_header_info(self, continuation, client_call_details, request):

        method, timeout, metadata, credentials, wait_for_ready, compression = client_call_details

        if client_call_details.metadata is not None:
            metadata = client_call_details.metadata
        else:
            metadata = []

        metadata.append((self.key, self.value), )

        new_client_call_details = _ClientCallDetails(
            method, timeout, metadata, credentials, wait_for_ready, compression)

        return continuation(new_client_call_details, request)

    def intercept_unary_unary(self, continuation, client_call_details, request):

        return self.add_header_info(continuation, client_call_details, request)

    def intercept_stream_unary(self, continuation, client_call_details, request):

        return self.add_header_info(continuation, client_call_details, request)
