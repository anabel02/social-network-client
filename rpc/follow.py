import logging
from grpclib import GRPCError
import proto.follow_service_pb2 as follow_pb2
import proto.follow_service_pb2_grpc as follow_pb2_grpc
from rpc.client import FOLLOW, create_channel, get_user

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FollowManager:
    @staticmethod
    async def follow_user(target_username: str) -> bool:
        user = get_user()
        request = follow_pb2.FollowUserRequest(user_id=user['sub'], target_user_id=target_username)

        async with await create_channel(FOLLOW) as channel:
            stub = follow_pb2_grpc.FollowServiceStub(channel)
            try:
                await stub.FollowUser(request)
                return True
            except GRPCError as error:
                logger.error(f"Error following user: {error.message}")
                return False

    @staticmethod
    async def unfollow_user(target_username: str) -> bool:
        user = get_user()
        request = follow_pb2.UnfollowUserRequest(user_id=user['sub'], target_user_id=target_username)

        async with await create_channel(FOLLOW) as channel:
            stub = follow_pb2_grpc.FollowServiceStub(channel)
            try:
                await stub.UnfollowUser(request)
                return True
            except GRPCError as error:
                logger.error(f"Error unfollowing user: {error.message}")
                return False

    @staticmethod
    async def get_following() -> list:
        user = get_user()
        request = follow_pb2.GetFollowingRequest(user_id=user['sub'])

        async with await create_channel(FOLLOW) as channel:
            stub = follow_pb2_grpc.FollowServiceStub(channel)
            try:
                response = await stub.GetFollowing(request)
                if not response.following:
                    return []
                return [user.username for user in response.following]
            except GRPCError as error:
                logger.error(f"Error getting following list: {error.message}")
                return []
