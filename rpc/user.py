import logging
import proto.users_service_pb2 as user_pb2
import proto.users_service_pb2_grpc as user_pb2_grpc
import proto.db_models_pb2 as db_models_pb2
from rpc.client import USER, create_channel
from store import Storage
import grpc.aio
from rpc.requests_queue import add_request, Request


logger = logging.getLogger(__name__)


class UserManager:
    @staticmethod
    async def get_user_info(username: str, force=False) -> db_models_pb2.User:

        if not force:
            # Check if the user's information is cached
            cached_user = await Storage.async_disk_get(f"user_{username}", None)
            if cached_user is not None:
                return cached_user

        request = user_pb2.GetUserRequest(username=username)
        async with await create_channel(USER) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            try:
                response = await stub.GetUser(request)
                # Store the user's information in the cache
                await Storage.async_disk_store(f"user_{username}", response.user)
                return response.user
            except grpc.aio.AioRpcError as e:
                logger.error(f"Error getting user info: {e.code()}; {e.details()}")
                return None
            except Exception as e:
                logger.error(f"Error during get user info: {str(e)}")
                return None

    @staticmethod
    async def edit_user_info(user: db_models_pb2.User) -> bool:
        request = user_pb2.EditUserRequest(user=user)
        async with await create_channel(USER) as channel:
            stub = user_pb2_grpc.UserServiceStub(channel)
            try:
                await stub.EditUser(request)
                # Update the cached user information
                await Storage.async_disk_store(f"user_{user.username}", user)
                return 0
            except grpc.aio.AioRpcError as e:
                logger.error(f"Error editing user info: {e.code()}; {e.details()}")
                if e.code() == grpc.StatusCode.UNAVAILABLE:
                    add_request(Request(USER, request))
                    return 2
                return 1
            except Exception as e:
                logger.error(f"Error during edit user info: {str(e)}")
                add_request(Request(USER, request))
                return 2
