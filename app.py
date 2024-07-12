import asyncio
import streamlit as st
from multiapp import MultiApp
from apps import login, profile, following
from rpc.clients import get_user
import logging
from rpc.broadcast import update_servers
from store import Storage

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Set page config at the very beginning of the script
st.set_page_config(layout='wide')


# Use st.cache_resource for initialization
@st.cache_resource
def initialize_app():
    user = get_user()
    app = MultiApp(user)
    app.add_app("Login", login.app)
    app.add_app("Profile", profile.app)
    app.add_app("Following users", following.app)
    return app


# Define a periodic task
async def periodic_task(interval, func):
    while True:
        print(f"Attempting to run {func.__name__}")
        try:
            if asyncio.iscoroutinefunction(func):
                await func()
            else:
                func()
            print(f"Successfully ran {func.__name__}")
        except Exception as e:
            print(f'Function {func.__name__} failed with exception: {e}')
        finally:
            print(f"Waiting {interval} seconds before next attempt")
            await asyncio.sleep(interval)


# Define a periodic task to update the servers
async def run_periodic_task():
    if not Storage.get('repeat'):
        Storage.store('repeat', True)
        await periodic_task(10, update_servers)


async def main():
    app = initialize_app()

    # Run the periodic task and the main app concurrently
    await asyncio.gather(
        run_periodic_task(),
        app.run()
    )


if __name__ == "__main__":
    asyncio.run(main())
