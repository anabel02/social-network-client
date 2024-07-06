import jwt
import streamlit as st

import logging
import proto
from grpclib.client import Channel
from grpclib import GRPCError
import proto.auth_service_pb2
import proto.auth_service_pb2_grpc
import proto.db_models_pb2
import proto.db_models_pb2_grpc
import bcrypt
import asyncio as aio
import grpc

TOKEN = 'token'


def get_user():
    token = st.session_state.get(TOKEN)
    if not token:
        return None

    with open('pub.pem', 'rb') as pub:
        public_key = pub.read()

    info = jwt.decode(token, public_key, algorithms=['RS256'])

    return info


async def app():

    loop = aio.get_event_loop()

    token: str = st.session_state.get(TOKEN)

    if token:

        user = get_user()
        print(user)

        st.write(f'Hello {user["name"]}, you are already logged in')

        clicked = st.button('Log Out')
        if clicked:
            await logout()
            st.experimental_rerun()
        return

    # Create a navigation bar using selectbox
    nav_options = ['Login', 'SignUp']
    signup_state = st.sidebar.selectbox('', nav_options)

    st.title(signup_state)
    signup_state = signup_state == 'SignUp'

    ip = '172.30.148.81'

    with st.form('login') as form:
        username = st.text_input('Username')
        if signup_state:
            name = st.text_input('Name')
            email = st.text_input('Email')
        password = st.text_input('Password', type='password')

        if signup_state:
            submitted = st.form_submit_button('Sign Up')
            if submitted:
                result = await signup(username, password, name, email, ip)
        else:
            submitted = st.form_submit_button('Log In')
            if submitted:
                result = await login(username, password, ip)
                if result:
                    st.experimental_rerun()


def sync(f, loop):
    def wrapper(*args, **kwargs):
        return loop.run_until_complete(f(*args, **kwargs))
    return wrapper


async def signup(username: str, password: str, name: str, email: str,  ip: str):
    logging.info(f"Creating user: username: {username}, name: {name}, email: {email}, password: {'*' * len(password)}")
    salt = bcrypt.gensalt()

    user = proto.db_models_pb2.User(username=username, name=name,
                                    password_hash=bcrypt.hashpw(password.encode(), salt).decode(), email=email)

    request = proto.auth_service_pb2.SignUpRequest(user=user)

    channel = grpc.insecure_channel(f'{ip}:50052')  # Adjust port as needed
    stub = proto.auth_service_pb2_grpc.AuthStub(channel)

    try:
        stub.SignUp(request)
        st.success("User created!")
        return True
    except GRPCError as error:
        logging.error(f"An error occurred creating the user: {error.status}: {error.message}")
        st.error(error.message)


async def login(username: str, password: str, ip: str):
    logging.info(f"Logging in: username: {username}, password: {'*' * len(password)}")

    request = proto.auth_service_pb2.LoginRequest(username=username, password=password)

    channel = grpc.insecure_channel(f'{ip}:50052')  # Adjust port as needed
    stub = proto.auth_service_pb2_grpc.AuthStub(channel)

    try:
        response = stub.Login(request)
        st.session_state[TOKEN] = response.token
        st.success('Logged In')
        return True
    except GRPCError as error:
        logging.error(error.message)
        st.error(error.message)


async def logout():
    if st.session_state.get(TOKEN):
        del st.session_state[TOKEN]
        st.success('Logged Out')
