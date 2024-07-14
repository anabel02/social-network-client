import logging
import proto.follow_service_pb2 as follow_pb2
import proto.follow_service_pb2_grpc as follow_pb2_grpc
from rpc.client import FOLLOW, create_channel, get_user
from store import Storage
import grpc.aio

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FollowManager:
    @staticmethod
    async def follow_user(target_username: str) -> bool:
        current_user_username = get_user()['sub']

        # Check if the user is already following the target user in the cache
        is_following = await Storage.async_disk_get(f"{current_user_username}_following_{target_username}", False)
        if is_following:
            return True

        request = follow_pb2.FollowUserRequest(user_id=current_user_username, target_user_id=target_username)

        async with await create_channel(FOLLOW) as channel:
            stub = follow_pb2_grpc.FollowServiceStub(channel)
            try:
                await stub.FollowUser(request)
                # Store the follow action in the cache
                await Storage.async_disk_store(f"{current_user_username}_following_{target_username}", True)
                # Update the user's following list in the cache
                following = await Storage.async_disk_get(f"{current_user_username}_following", default=[])
                following.append(target_username)
                await Storage.async_disk_store(f"{current_user_username}_following", following)
                return True
            except grpc.aio.AioRpcError as e:
                logger.error(f"Error following user: {e.code()}; {e.details()}")
                return False
            except Exception as e:
                logger.error(f"Error during follow: {str(e)}")
                return False

    @staticmethod
    async def unfollow_user(target_username: str) -> bool:
        current_user_username = get_user()['sub']

        request = follow_pb2.UnfollowUserRequest(user_id=current_user_username, target_user_id=target_username)

        async with await create_channel(FOLLOW) as channel:
            stub = follow_pb2_grpc.FollowServiceStub(channel)
            try:
                await stub.UnfollowUser(request)
                # Remove the follow action from the cache
                await Storage.async_disk_delete(f"{current_user_username}_following_{target_username}")
                # Update the user's following list in the cache
                following = await Storage.async_disk_get(f"{current_user_username}_following", default=[])
                following = [user for user in following if user != target_username]
                await Storage.async_disk_store(f"{current_user_username}_following", following)
                return True
            except grpc.aio.AioRpcError as e:
                logger.error(f"Error unfollowing user: {e.code()}; {e.details()}")
                return False
            except Exception as e:
                logger.error(f"Error during unfollow: {str(e)}")
                return False

    @staticmethod
    async def get_following() -> list:
        current_user_username = get_user()['sub']

        # Check if the user's following list is cached
        cached_following = await Storage.async_disk_get(f"{current_user_username}_following", default=None)
        if cached_following is not None:
            return cached_following

        request = follow_pb2.GetFollowingRequest(user_id=current_user_username)

        async with await create_channel(FOLLOW) as channel:
            stub = follow_pb2_grpc.FollowServiceStub(channel)
            try:
                response = await stub.GetFollowing(request)
                if not response.following_usernames:
                    return []
                following = [username for username in response.following_usernames]
                # Store the following list in the cache
                await Storage.async_disk_store(f"{current_user_username}_following", following)
                return following
            except grpc.aio.AioRpcError as e:
                logger.error(f"Error getting following list: {e.code()}; {e.details()}")
                return []
            except Exception as e:
                logger.error(f"Error during get following: {str(e)}")
                return []
