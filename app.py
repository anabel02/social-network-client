import asyncio
from multiapp import MultiApp
from apps import login, profile, following  # import your app modules here
from rpc.clients import get_user

loop = asyncio.get_event_loop_policy().new_event_loop()

app = MultiApp(get_user())

# Add all your application here
app.add_app("Login", login.app)
app.add_app("Profile", profile.app)
app.add_app("Following users", following.app)

# The main app
loop.run_until_complete(app.run())
