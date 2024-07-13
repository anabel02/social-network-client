import asyncio
from multiapp import MultiApp
from pages import login, profile, following
from rpc.client import get_user
import logging
from rpc.broadcast import update_servers

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        periodic_task(10, update_servers)
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
