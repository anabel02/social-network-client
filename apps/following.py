import streamlit as st
from rpc.follow import FollowManager
from rpc.posts import PostManager
from rpc.client import get_user
from rpc.user import UserManager


class FollowUIManager:
    @staticmethod
    def initialize_session_state():
        if 'edit_mode' not in st.session_state:
            st.session_state.edit_mode = False
        if 'user_info' not in st.session_state:
            st.session_state.user_info = None
        if 'view_user_posts' not in st.session_state:
            st.session_state.view_user_posts = None

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
        else:
            st.warning("You are not logged in. Please log in to view your profile.")

    @staticmethod
    def render_follow_form():
        with st.form('follow_user'):
            target_username = st.text_input('Enter username to follow')
            submitted = st.form_submit_button('Follow')
            if submitted:
                st.session_state['do_follow'] = target_username
                st.rerun()

    @staticmethod
    async def display_following():
        following = await FollowManager.get_following()
        st.subheader("Users you're following:")
        for username in following:
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                st.write(username)
            with col2:
                if st.button(f"Unfollow {username}", key=f"unfollow_{username}"):
                    st.session_state['do_unfollow'] = username
                    st.rerun()
            with col3:
                if st.button("View Posts", key=f"view_posts_{username}"):
                    st.session_state['view_user_posts'] = username
                    st.rerun()

    @staticmethod
    async def display_user_posts(username):
        st.subheader(f"Posts by {username}")
        posts = await PostManager.get_user_posts_by_username(username)
        if posts:
            for post in posts:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.write(f"{post.content}")
                    st.write(f"Posted on: {post.timestamp}")
                    if post.post_type == 1:  # Assuming 1 is the value for REPOST
                        st.write("(Repost)")
                with col2:
                    if st.button("Repost", key=f"repost_{post.post_id}"):
                        st.session_state['do_repost'] = post.post_id
                        st.rerun()
                st.markdown("---")
        else:
            st.write(f"{username} hasn't posted anything yet.")

    @staticmethod
    async def handle_repost(post_id):
        repost_content = st.text_input("Add a comment to your repost (optional):")
        if st.button("Confirm Repost"):
            reposted = await PostManager.repost(post_id, repost_content)
            if reposted:
                st.success("Post reposted successfully!")
            else:
                st.error("Failed to repost. Please try again.")
            st.session_state['do_repost'] = None
            st.rerun()


async def app():
    FollowUIManager.initialize_session_state()

    if not st.session_state.user_info:
        await FollowUIManager.load_user_info()

    FollowUIManager.display_user_info()

    if st.session_state.user_info:
        FollowUIManager.render_follow_form()

        if 'do_follow' in st.session_state:
            target_username = st.session_state.pop('do_follow')
            success = await FollowManager.follow_user(target_username)
            if success:
                st.success(f"You are now following {target_username}")
            else:
                st.error(f"Failed to follow {target_username}")

        if 'do_unfollow' in st.session_state:
            target_username = st.session_state.pop('do_unfollow')
            success = await FollowManager.unfollow_user(target_username)
            if success:
                st.success(f"You have unfollowed {target_username}")
            else:
                st.error(f"Failed to unfollow {target_username}")

        if 'do_repost' in st.session_state and st.session_state['do_repost']:
            await FollowUIManager.handle_repost(st.session_state['do_repost'])
        elif 'view_user_posts' in st.session_state and st.session_state['view_user_posts']:
            username = st.session_state.pop('view_user_posts')
            await FollowUIManager.display_user_posts(username)
        else:
            await FollowUIManager.display_following()