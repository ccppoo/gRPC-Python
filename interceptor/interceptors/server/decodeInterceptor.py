from grpc import ServerInterceptor


class DecodeInterceptor(ServerInterceptor):
    def __init__(self) -> None:
        super().__init__()

    def intercept_service(self, continuation, handler_call_details):
        return continuation(handler_call_details)
