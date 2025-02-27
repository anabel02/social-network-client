import streamlit as st
from rpc.user import UserManager
from rpc.client import get_user
from rpc.posts import PostManager


class ProfileUIManager:
    @staticmethod
    def initialize_session_state():
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        if 'user_info' not in st.session_state:
            st.session_state.user_info = None
        if 'do_post' not in st.session_state:
            st.session_state.do_post = None
        if 'do_repost' not in st.session_state:
            st.session_state.do_repost = None
        if 'do_delete' not in st.session_state:
            st.session_state.do_delete = None

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
        response = await UserManager.edit_user_info(user_info)
        if response == 0:
            st.success("Profile updated successfully!")
            st.session_state.edit_mode = False
            st.session_state.user_info = user_info
        elif response == 1:
            st.error("Failed to update profile. Please try again.")
        elif response == 2:
            st.error("Failed to update profile. Request stored locally. Check your connection.")

    @staticmethod
    def render_post_form():
        with st.form('create_post'):
            content = st.text_area('Write your post here')
            submitted = st.form_submit_button('Post')
            if submitted:
                st.session_state['do_post'] = content
                st.rerun()

    @staticmethod
    async def display_posts():
        posts = await PostManager.get_user_posts()
        st.subheader("Your Posts:")
        if posts:
            for post in posts:
                col1, col2, col3 = st.columns([3, 1, 1])
                with col1:
                    if post.original_post_id:
                        st.write(f"Reposted on {post.timestamp}")
                    else:
                        st.write(f"Posted on {post.timestamp}")
                    st.write(post.content)
                with col2:
                    if st.button("Delete", key=f"delete_{post.post_id}"):
                        st.session_state['do_delete'] = post.post_id
                        st.rerun()
                with col3:
                    if st.button("Repost", key=f"repost_{post.post_id}"):
                        st.session_state['do_repost'] = post.post_id
                        st.rerun()
                st.markdown("---")
        else:
            st.write("You hasn't posted anything yet.")


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

        # Post functionality
        ProfileUIManager.render_post_form()

        if st.session_state['do_post']:
            content = st.session_state.pop('do_post')
            response = await PostManager.create_post(content)
            if response == 0:
                st.success("Post created successfully!")
            elif response == 1:
                st.error("Failed to create post. Please try again.")
            elif response == 2:
                st.error("Failed to create post. Request stored locally. Check your connection.")
            st.rerun()

        if st.session_state['do_repost']:
            original_post_id = st.session_state.pop('do_repost')
            response = await PostManager.repost(original_post_id)
            if response == 0:
                st.success("Repost created successfully!")
            else:
                st.error("Failed to repost. Please try again.")
            st.rerun()

        if st.session_state['do_delete']:
            post_id = st.session_state.pop('do_delete')
            response = await PostManager.delete_post(post_id)
            if response == 0:
                st.success("Post deleted successfully!")
            else:
                st.error("Failed to delete post. Please try again.")
            st.rerun()

        await ProfileUIManager.display_posts()
