import streamlit as st
import logging
from grpclib import GRPCError
import proto.auth_service_pb2 as auth_pb2
import proto.auth_service_pb2_grpc as auth_pb2_grpc
import proto.db_models_pb2 as db_models_pb2
import bcrypt
from rpc.client import AUTH, create_channel, TOKEN
from store import Storage


# Configure logging
logging.basicConfig(level=logging.INFO)
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
            except GRPCError as error:
                logger.error(f"An error occurred creating the user: {error.status}: {error.message}")
                return False
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
            except GRPCError as error:
                logger.error(f"Login error: {error.message}")
                return False
            except Exception as e:
                logger.error(f"Error during login: {str(e)}")
                return False

    @staticmethod
    async def logout():
        Storage.clear()
        st.success('Logged Out Successfully')
        st.rerun()
