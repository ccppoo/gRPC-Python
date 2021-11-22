from grpc import UnaryUnaryClientInterceptor, StreamUnaryClientInterceptor


class MessageFormatInterceptor(UnaryUnaryClientInterceptor, StreamUnaryClientInterceptor):

    def __init__(self) -> None:
        super().__init__()

    def intercept_unary_unary(self, continuation, client_call_details, request):
        return continuation(client_call_details, request)

    def intercept_stream_unary(self, continuation, client_call_details, request):
        return continuation(client_call_details, request)
