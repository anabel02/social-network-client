import logging
from grpclib import GRPCError
import proto.posts_service_pb2 as post_pb2
import proto.posts_service_pb2_grpc as post_pb2_grpc
from rpc.client import POST, create_channel, get_user
from store import Storage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostManager:
    @staticmethod
    async def create_post(content: str) -> bool:
        current_user_username = get_user()['sub']
        request = post_pb2.CreatePostRequest(user_id=current_user_username, content=content)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                response = await stub.CreatePost(request)
                # Store the new post in the cache
                posts = await Storage.async_disk_get(f"{current_user_username}_posts", [])
                await Storage.async_disk_store(f"{current_user_username}_posts", posts + [response.post])
                return response.post
            except GRPCError as error:
                logger.error(f"Error creating post: {error.message}")
                return None

    @staticmethod
    async def repost(original_post_id: str, content: str) -> bool:
        current_user_username = get_user()['sub']
        request = post_pb2.RepostRequest(user_id=current_user_username, original_post_id=original_post_id,
                                         content=content)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                response = await stub.Repost(request)
                # Store the new repost in the cache
                posts = await Storage.async_disk_get(f"{current_user_username}_posts", [])
                await Storage.async_disk_store(f"{current_user_username}_posts", posts + [response.post])
                return response.post
            except GRPCError as error:
                logger.error(f"Error reposting: {error.message}")
                return None

    @staticmethod
    async def delete_post(post_id: str) -> bool:
        current_user_username = get_user()['sub']
        request = post_pb2.DeletePostRequest(post_id=post_id)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                await stub.DeletePost(request)
                # Remove the deleted post from the cache
                posts = await Storage.async_disk_get(f"{current_user_username}_posts", [])
                posts = [p for p in posts if p.post_id != post_id]
                await Storage.async_disk_store(f"{current_user_username}_posts", posts)
                return True
            except GRPCError as error:
                logger.error(f"Error deleting post: {error.message}")
                return False

    @staticmethod
    async def get_user_posts() -> list:
        user = get_user()
        current_user_username = user['sub']

        # Check if the user's posts are cached
        cached_posts = await Storage.async_disk_get(f"{current_user_username}_posts", None)
        if cached_posts is not None:
            return cached_posts

        request = post_pb2.GetUserPostsRequest(user_id=current_user_username)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                response = await stub.GetUserPosts(request)
                # Convert the RepeatedCompositeContainer to a list of db_models_pb2.Post objects
                posts = [post for post in response.posts]
                # Store the user's posts in the cache
                await Storage.async_disk_store(f"{current_user_username}_posts", posts)
                return posts
            except GRPCError as error:
                logger.error(f"Error getting user posts: {error.message}")
                return []

    @staticmethod
    async def get_user_posts_by_username(user_id: str) -> list:
        request = post_pb2.GetUserPostsRequest(user_id=user_id)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                response = await stub.GetUserPosts(request)
                return response.posts
            except GRPCError as error:
                logger.error(f"Error getting user posts: {error.message}")
                return []
