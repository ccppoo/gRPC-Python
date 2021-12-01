from grpc import UnaryUnaryClientInterceptor

from proto_modules import SecureMessageDetail


class MessageFormatInterceptor(UnaryUnaryClientInterceptor):

    def __init__(self) -> None:
        super().__init__()

    def modifyMessage(self, continuation, client_call_details, request):
        request.value = request.value.capitalize()
        return continuation(client_call_details, request)

    def intercept_unary_unary(self, continuation, client_call_details, request):

        # /<package name>.<service name>/<method name>
        if client_call_details.method == SecureMessageDetail.sendMessage.name:
            return self.modifyMessage(continuation, client_call_details, request)

        return continuation(client_call_details, request)
