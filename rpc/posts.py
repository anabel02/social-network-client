import logging
from grpclib import GRPCError
import proto.posts_service_pb2 as post_pb2
import proto.posts_service_pb2_grpc as post_pb2_grpc
from rpc.clients import POST, create_channel, get_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PostManager:
    @staticmethod
    async def create_post(content: str) -> bool:
        user = get_user()
        request = post_pb2.CreatePostRequest(user_id=user['sub'], content=content)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                response = await stub.CreatePost(request)
                return response.post
            except GRPCError as error:
                logger.error(f"Error creating post: {error.message}")
                return None

    @staticmethod
    async def repost(original_post_id: str, content: str) -> bool:
        user = get_user()
        request = post_pb2.RepostRequest(user_id=user['sub'], original_post_id=original_post_id, content=content)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                response = await stub.Repost(request)
                return response.post
            except GRPCError as error:
                logger.error(f"Error reposting: {error.message}")
                return None

    @staticmethod
    async def delete_post(post_id: str) -> bool:
        request = post_pb2.DeletePostRequest(post_id=post_id)

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                await stub.DeletePost(request)
                return True
            except GRPCError as error:
                logger.error(f"Error deleting post: {error.message}")
                return False

    @staticmethod
    async def get_user_posts() -> list:
        user = get_user()
        request = post_pb2.GetUserPostsRequest(user_id=user['sub'])

        async with await create_channel(POST) as channel:
            stub = post_pb2_grpc.PostServiceStub(channel)
            try:
                response = await stub.GetUserPosts(request)
                return response.posts
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
