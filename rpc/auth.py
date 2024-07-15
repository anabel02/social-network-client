import logging
import proto.auth_service_pb2 as auth_pb2
import proto.auth_service_pb2_grpc as auth_pb2_grpc
import proto.db_models_pb2 as db_models_pb2
import bcrypt
from rpc.client import AUTH, create_channel, TOKEN
from store import Storage
import grpc.aio


logger = logging.getLogger(__name__)


class AuthManager:
    @staticmethod
    async def signup(username: str, password: str, name: str, email: str) -> bool:
        logger.info(f"Creating user: username: {username}, name: {name}, email: {email}")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

        user = db_models_pb2.User(username=username, name=name, password_hash=hashed_password, email=email)
        request = auth_pb2.SignUpRequest(user=user)

        async with await create_channel(AUTH) as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            try:
                await stub.SignUp(request)
                # Store the user's information in the cache
                await Storage.async_disk_store(f"user_{username}", user)
                return True
            except grpc.aio.AioRpcError as e:
                logger.error(f"An error occurred creating the user: {e.code()}; {e.details()}")
                raise e
            except Exception as e:
                logger.error(f"Error during signup: {str(e)}")
                return False

    @staticmethod
    async def login(username: str, password: str) -> bool:
        logger.info(f"Logging in: username: {username}")
        request = auth_pb2.LoginRequest(username=username, password=password)

        async with await create_channel(AUTH) as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            try:
                response = await stub.Login(request)
                await Storage.async_disk_store(TOKEN, response.token)
                return True
            except grpc.aio.AioRpcError as e:
                logger.error(f"Login error: {e.code()}; {e.details()}")
                return False
            except Exception as e:
                logger.error(f"Error during login: {str(e)}")
                return False
