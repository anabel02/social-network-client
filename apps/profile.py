import streamlit as st
from rpc.user import UserManager
from rpc.clients import get_user


class ProfileUIManager:
    @staticmethod
    def initialize_session_state():
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        if 'user_info' not in st.session_state:
            st.session_state.user_info = None

    @staticmethod
    async def load_user_info():
        user = get_user()
        if user:
            st.session_state.user_info = await UserManager.get_user_info(user['sub'])
        else:
            st.session_state.user_info = None

    @staticmethod
    def display_user_info():
        user_info = st.session_state.user_info
        if user_info:
            st.title(f"Welcome, {user_info.name}!")
            st.write(f"Username: {user_info.username}")
            st.write(f"Email: {user_info.email}")
        else:
            st.warning("You are not logged in. Please log in to view your profile.")

    @staticmethod
    def toggle_edit_mode():
        if st.button("Edit Profile" if not st.session_state.edit_mode else "Cancel Edit"):
            st.session_state.edit_mode = not st.session_state.edit_mode

    @staticmethod
    def edit_profile_form():
        user_info = st.session_state.user_info
        with st.form("edit_profile"):
            new_name = st.text_input("Name", value=user_info.name)
            new_email = st.text_input("Email", value=user_info.email)
            submitted = st.form_submit_button("Save Changes")
            if submitted:
                user_info.name = new_name
                user_info.email = new_email
                return user_info
        return None

    @staticmethod
    async def update_user_profile(user_info):
        try:
            success = await UserManager.edit_user_info(user_info)
            if success:
                st.success("Profile updated successfully!")
                st.session_state.edit_mode = False
                st.session_state.user_info = user_info
            else:
                st.error("Error updating profile. Please try again.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")


async def app():
    ProfileUIManager.initialize_session_state()

    if not st.session_state.user_info:
        await ProfileUIManager.load_user_info()

    ProfileUIManager.display_user_info()

    if st.session_state.user_info:
        ProfileUIManager.toggle_edit_mode()

        if st.session_state.edit_mode:
            updated_info = ProfileUIManager.edit_profile_form()
            if updated_info:
                await ProfileUIManager.update_user_profile(updated_info)
                st.rerun()
