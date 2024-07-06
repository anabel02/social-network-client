import jwt
import streamlit as st
import logging
from grpclib import GRPCError
import proto.auth_service_pb2 as auth_pb2
import proto.auth_service_pb2_grpc as auth_pb2_grpc
import proto.db_models_pb2 as db_models_pb2
import bcrypt
import grpc
from typing import Optional

# Constants
TOKEN = 'token'
SERVER_IP = '172.30.148.81'
SERVER_PORT = '50052'
PUBLIC_KEY_PATH = 'pub.pem'

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AuthManager:
    @staticmethod
    def get_user() -> Optional[dict]:
        token = st.session_state.get(TOKEN)
        if not token:
            return None
        try:
            with open(PUBLIC_KEY_PATH, 'rb') as pub:
                public_key = pub.read()
            return jwt.decode(token, public_key, algorithms=['RS256'])
        except jwt.PyJWTError as e:
            logger.error(f"Error decoding token: {e}")
            return None

    @staticmethod
    async def create_grpc_channel():
        return grpc.aio.insecure_channel(f'{SERVER_IP}:{SERVER_PORT}')

    @staticmethod
    async def signup(username: str, password: str, name: str, email: str) -> bool:
        logger.info(f"Creating user: username: {username}, name: {name}, email: {email}")
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode(), salt).decode()

        user = db_models_pb2.User(username=username, name=name, password_hash=hashed_password, email=email)
        request = auth_pb2.SignUpRequest(user=user)

        async with await AuthManager.create_grpc_channel() as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            try:
                await stub.SignUp(request)
                st.success("User created successfully!")
                login_success = await AuthManager.login(username, password)
                if login_success:
                    st.session_state['user_logged_in'] = True
                    st.experimental_rerun()
                    return True
                else:
                    st.warning("Account created, but automatic login failed. Please log in manually.")
                    return False
            except GRPCError as error:
                logger.error(f"An error occurred creating the user: {error.status}: {error.message}")
                st.error(f"Error: {error.message}")
                return False

            except Exception as e:
                logger.error(f"Unexpected error during signup: {str(e)}")
                st.error("An unexpected error occurred. Please try again later.")
                return False

    @staticmethod
    async def login(username: str, password: str) -> bool:
        logger.info(f"Logging in: username: {username}")
        request = auth_pb2.LoginRequest(username=username, password=password)

        async with await AuthManager.create_grpc_channel() as channel:
            stub = auth_pb2_grpc.AuthStub(channel)
            try:
                response = await stub.Login(request)
                st.session_state[TOKEN] = response.token
                st.success('Logged In Successfully')
                return True
            except GRPCError as error:
                logger.error(f"Login error: {error.message}")
                st.error(f"Login failed: {error.message}")
                return False

    @staticmethod
    async def logout():
        if TOKEN in st.session_state:
            del st.session_state[TOKEN]
            st.success('Logged Out Successfully')


class UIManager:
    @staticmethod
    def render_login_form():
        with st.form('login'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submitted = st.form_submit_button('Log In')
            if submitted:
                st.session_state['do_login'] = (username, password)
                st.experimental_rerun()

    @staticmethod
    def render_signup_form():
        with st.form('signup'):
            username = st.text_input('Username')
            name = st.text_input('Name')
            email = st.text_input('Email')
            password = st.text_input('Password', type='password')
            submitted = st.form_submit_button('Sign Up')
            if submitted:
                st.session_state['do_signup'] = (username, password, name, email)
                st.experimental_rerun()


async def app():
    if 'do_login' in st.session_state:
        username, password = st.session_state.pop('do_login')
        await AuthManager.login(username, password)

    if 'do_signup' in st.session_state:
        username, password, name, email = st.session_state.pop('do_signup')
        await AuthManager.signup(username, password, name, email)

    user = AuthManager.get_user()

    if user:
        st.write(f'Hello {user["name"]}, you are logged in')
        if st.button('Log Out'):
            await AuthManager.logout()
            st.experimental_rerun()
    else:
        nav_options = ['Login', 'SignUp']
        selected_option = st.sidebar.selectbox('', nav_options)

        st.title(selected_option)

        if selected_option == 'Login':
            UIManager.render_login_form()
        else:
            UIManager.render_signup_form()
