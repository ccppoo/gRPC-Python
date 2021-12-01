from grpc import ServerInterceptor
from grpc import StatusCode
from grpc import unary_unary_rpc_method_handler, stream_unary_rpc_method_handler
from proto_modules import SecureMessageDetail


class HeaderInterceptor(ServerInterceptor):
    def __init__(self) -> None:
        self.key = 'grpc'
        super().__init__()

    def abort_handler(self, handler, details):

        if details.method == SecureMessageDetail.addTheseNumbers.name:
            return stream_unary_rpc_method_handler(handler)

        return unary_unary_rpc_method_handler(handler)

    def check_metadata(self, continuation, handler_call_details):

        valid = any(
            [self.key in datum for datum in handler_call_details.invocation_metadata])

        if valid:
            return continuation(handler_call_details)

        def abort(request, context):
            context.abort(StatusCode.PERMISSION_DENIED, 'No key')

        return unary_unary_rpc_method_handler(abort, handler_call_details)

    def intercept_service(self, continuation, handler_call_details):

        return self.check_metadata(continuation, handler_call_details)
