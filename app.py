import asyncio
from multiapp import MultiApp
from apps import login, profile, following
from rpc.client import get_user
import logging
from rpc.broadcast import update_servers
from rpc.requests_queue import process_requests
from rpc.user import UserManager
from rpc.follow import FollowManager
from rpc.posts import PostManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def update_storage():
    logger.info("Updating storage")
    user = get_user()
    if user:
        try:
            await UserManager.get_user_info(user['sub'], force=True)
            await FollowManager.get_following(force=True)
            await PostManager.get_user_posts(force=True)
            logger.info("Storage updated successfully")
        except Exception as e:
            logger.error(f"Error updating storage: {str(e)}")
    else:
        logger.info("No storage to update. No user found.")


async def periodic_task(interval, func, *args, **kwargs):
    while True:
        try:
            logger.info("Trying to run function: {func.__name__}")
            if asyncio.iscoroutinefunction(func):
                await func(*args, **kwargs)
            else:
                func(*args, **kwargs)
        except Exception as e:
            logger.error(f'Function {func.__name__} failed with exception: {e}')
        finally:
            logger.info(f"Waiting {interval} seconds before next attempt")
            await asyncio.sleep(interval)


async def run_periodic_tasks():
    tasks = [
        periodic_task(10, update_servers),
        periodic_task(17, process_requests),
        # periodic_task(120, update_storage)
    ]
    await asyncio.gather(*tasks)


async def main():
    user = get_user()
    app = MultiApp(user)
    app.add_app("Login", login.app)
    app.add_app("Profile", profile.app)
    app.add_app("Following users", following.app)

    # Run the periodic task and the main app concurrently
    await asyncio.gather(
        run_periodic_tasks(),
        app.run()
    )


if __name__ == "__main__":
    asyncio.run(main())
