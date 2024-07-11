import streamlit as st
from store import Storage
from rpc.auth import AuthManager
from grpclib import GRPCError
from rpc.clients import TOKEN, get_user


class UIManager:
    @staticmethod
    def render_login_form():
        with st.form('login'):
            username = st.text_input('Username')
            password = st.text_input('Password', type='password')
            submitted = st.form_submit_button('Log In')
            if submitted:
                st.session_state['do_login'] = (username, password)
                st.rerun()

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
                st.rerun()


async def app():
    if 'do_login' in st.session_state:
        username, password = st.session_state.pop('do_login')
        if await AuthManager.login(username, password):
            st.success("Logged in successfully!")
        else:
            st.error("Error logging in. Please check your credentials and try again.")

    if 'do_signup' in st.session_state:
        username, password, name, email = st.session_state.pop('do_signup')
        try:
            await AuthManager.signup(username, password, name, email)
            login_success = await AuthManager.login(username, password)
            if not login_success:
                st.warning("Account created, but automatic login failed. Please log in manually.")
        except GRPCError as error:
            st.error(f"Sign up failed: {error.message}")

    token: str = await Storage.async_disk_get(TOKEN)

    if token:
        user = get_user()
        st.write(f'Hello {user["name"]}, you are logged in')
        if st.button('Log Out'):
            await AuthManager.logout()
    else:
        nav_options = ['Login', 'Sign Up']
        selected_option = st.sidebar.selectbox('', nav_options)

        st.title(selected_option)

        if selected_option == 'Login':
            UIManager.render_login_form()
        else:
            UIManager.render_signup_form()
