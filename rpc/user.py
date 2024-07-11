import jwt
import logging
from grpclib import GRPCError
import proto.users_service_pb2 as user_pb2
import proto.users_service_pb2_grpc as user_pb2_grpc
import proto.db_models_pb2 as db_models_pb2
from store import Storage
from rpc.clients import USER, create_channel, TOKEN, PUBLIC_KEY_PATH

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserManager:
    @staticmethod
    def get_user() -> dict:
        token = Storage.disk_get(TOKEN)
        if not token:
            return {}
        try:
            with open(PUBLIC_KEY_PATH, 'rb') as pub:
                public_key = pub.read()
            return jwt.decode(token, public_key, algorithms=['RS256'])
        except jwt.PyJWTError as e:
            logger.error(f"Error decoding token: {e}")
            return {}

    @staticmethod
    async def get_user_info(username: str) -> db_models_pb2.User:
        request = user_pb2.GetUserRequest(username=username)
        async with await create_channel(USER) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            try:
                response = await stub.GetUser(request)
                return response.user
            except GRPCError as error:
                logger.error(f"Error getting user info: {error.status}: {error.message}")
                return None

    @staticmethod
    async def edit_user_info(user: db_models_pb2.User) -> bool:
        request = user_pb2.EditUserRequest(user=user)
        async with await create_channel(USER) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            try:
                await stub.EditUser(request)
                return True
            except GRPCError as error:
                logger.error(f"Error editing user info: {error.status}: {error.message}")
                return False
