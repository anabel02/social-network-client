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
import time
import threading
from streamlit.runtime.scriptrunner import add_script_run_ctx

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


def periodic_task(interval, task_function):
    def wrapper():
        while True:
            task_function()
            time.sleep(interval)
    return wrapper


def run_periodic_tasks():
    tasks = [
        periodic_task(13, update_servers),
        periodic_task(23, lambda: asyncio.run(process_requests())),
        periodic_task(107, lambda: asyncio.run(update_storage()))
    ]
    for task in tasks:
        t = threading.Thread(target=task, daemon=True)
        add_script_run_ctx(t)
        t.start()


async def main():
    user = get_user()
    app = MultiApp(user)
    app.add_app("Login", login.app)
    app.add_app("Profile", profile.app)
    app.add_app("Following users", following.app)

    run_periodic_tasks()

    await app.run()


if __name__ == "__main__":
    asyncio.run(main())
