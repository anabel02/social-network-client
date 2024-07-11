import asyncio
from multiapp import MultiApp
from apps import login, profile  # import your app modules here

loop = asyncio.get_event_loop_policy().new_event_loop()

app = MultiApp(login.AuthManager.get_user())

# Add all your application here
app.add_app("Login", login.app)
app.add_app("Profile", profile.app)

# The main app
loop.run_until_complete(app.run())
