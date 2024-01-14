from ....api.auth_agent import auth_agent
from ....client import client
from ....client.subscription import subscribe
from ....core.asyncio import AsyncTask
from ....core.states import state
from ....core.utils.ui import redraw_area
from ....local_storage import set_storage


async def login(username: str, password: str) -> bool:
    login_result = await auth_agent.login(
        username=username,
        password=password,
    )

    state.is_logged_in = login_result.success
    state.token = login_result.token

    set_storage("token", login_result.token)

    if login_result.success:
        await client.restart_http()
        await client.restart_graphql()
        AsyncTask(subscribe).exec()

        redraw_area("VIEW_3D")

        # TODO: Initialize editor

    return login_result.success


async def logout() -> bool:
    success = await auth_agent.logout()

    if success:
        state.is_logged_in = False
        state.token = ""

        set_storage("token", "")

        await client.close_graphql()
        await client.restart_http()

        redraw_area("VIEW_3D")

    return success
