import sys
from collections import namedtuple
sys.path.append('proto_modules')

method = namedtuple('_method', field_names=['name', 'type'])
details = namedtuple('_details', field_names=[
                     'pingRequest', 'sendMessage', 'addTheseNumbers'])

# accessible method name generated script from `*_pb2_grpc.py`
# By doing this, method could be dispatched for specific interceptors
SecureMessageDetail = details(
    method(r'/interceptors.SecureMessage/PingRequest', 'unary_unary'),
    method(r'/interceptors.SecureMessage/sendMessage', 'unary_unary'),
    method(r'/interceptors.SecureMessage/addTheseNumbers', 'stream_unary')
)
