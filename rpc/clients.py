import grpc
import jwt
import logging
from grpc import aio as grpc_aio
from store import Storage
from typing import Optional

# Constants
USER = 50051
AUTH = 50052

TOKEN = 'token'
PUBLIC_KEY_PATH = 'pub.pem'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_host(service):
    return f'172.17.0.2:{service}'


def get_user() -> Optional[dict]:
    token = Storage.disk_get(TOKEN)
    if not token:
        return None
    try:
        with open(PUBLIC_KEY_PATH, 'rb') as pub:
            public_key = pub.read()
        return jwt.decode(token, public_key, algorithms=['RS256'])
    except jwt.PyJWTError as e:
        logger.error(f"Error decoding token: {e}")
        return None


class AuthInterceptor(grpc.aio.UnaryUnaryClientInterceptor):
    async def intercept_unary_unary(self, continuation, client_call_details, request):
        token = await Storage.async_disk_get(TOKEN)
        if token:
            if client_call_details.metadata is None:
                metadata = []
            else:
                metadata = list(client_call_details.metadata)

            if token:
                metadata.append(('authorization', token))
            # Create a new ClientCallDetails object with the updated metadata
            new_client_call_details = grpc.aio.ClientCallDetails(
                method=client_call_details.method,
                timeout=client_call_details.timeout,
                metadata=tuple(metadata),
                credentials=client_call_details.credentials,
                wait_for_ready=client_call_details.wait_for_ready
            )
        else:
            new_client_call_details = client_call_details

        return await continuation(new_client_call_details, request)


class InterceptedChannel:
    def __init__(self, channel, interceptor):
        self._channel = channel
        self._interceptor = interceptor

    def unary_unary(self, method, request_serializer=None, response_deserializer=None, _registered_method=None):
        original_unary_unary = self._channel.unary_unary(method, request_serializer, response_deserializer)

        async def intercepted_unary_unary(request, timeout=None, metadata=None, credentials=None):
            if metadata is None:
                metadata = []
            else:
                metadata = list(metadata)

            client_call_details = grpc.aio.ClientCallDetails(
                method=method,
                timeout=timeout,
                metadata=tuple(metadata),
                credentials=credentials,
                wait_for_ready=None
            )
            return await self._interceptor.intercept_unary_unary(
                lambda cd, req: original_unary_unary(req, timeout=cd.timeout,
                                                     metadata=cd.metadata, credentials=cd.credentials),
                client_call_details,
                request
            )

        return intercepted_unary_unary

    def __getattr__(self, name):
        return getattr(self._channel, name)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._channel.close()


async def create_channel(service):
    host = get_host(service)
    channel = grpc_aio.insecure_channel(host)
    return InterceptedChannel(channel, AuthInterceptor())
