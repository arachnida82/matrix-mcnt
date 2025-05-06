#!/usr/bin/env python3

import asyncio
import argparse
import getpass
from nio import (
        AsyncClient,
        MatrixRoom,
        RoomMessageText,
        LoginResponse,
        RoomInfo
)


HOME = "matrix.org"
HOME_SERVER = f"https://{HOME}"
USERNAME = None
USER_ID = f"@{USERNAME}:{HOME}"
ROOM_IDS = []
EXCLUDE_ROOM_IDS = []
ACCESS_TOKEN = None


async def client_login() -> AsyncClient:
    client = AsyncClient(HOME_SERVER, USER_ID)
    #client = AsyncClient(f"https://{HOME}", f"@{USERNAME}:{HOME}") # need to decide on username format
    if ACCESS_TOKEN:
        client.access_token = ACCESS_TOKEN
        # TODO: implement try-exception
        return client
    passwd = getpass.getpass()
    if isinstance(await client.login(passwd), LoginResponse):
        return client

    return None

async def main() -> None:
    client = await client_login()

    if not client:
        print(f"Could not log on to {USERNAME}")
        exit()
    else:
        print(f"Logged on as {USERNAME}.")

    await client.sync_forever(timeout=30000)

async def fetch_unread(client: AsyncClient):
    exit() # TODO:

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
            description="matrix-mcnt: Matrix Unread Message Count"
    )

    parser.add_argument(
            "--username",
            required=True,
            help="eg. 'myusername' not '@myusername:matrix.org'"
            # otherwise conflict arises if --homeserver is supplied
    )

    parser.add_argument(
            "--access-token",
            help="Supply an access token to prevent password prompting"
    )

    parser.add_argument(
            "--homeserver",
            default=HOME,
            help="Supply homeserver domain (eg. 'matrix.org' or 'matrix.server.com')"
    )

    parser.add_argument(
            "--rooms",
            help="Room ID(s) (eg. '!Abcdefghijklmnopqr' '!2Abcdefghijklmnopq')." +
                 "matrix-mcnt will only count the supplied ID(s).",
            default=[],
            action="append",
    )

    parser.add_argument(
            "--exclude-rooms",
            help="A list of Room(s) ID(s) to exclude (eg. '!Abcdefghijklmnopqr')",
            default=[],
            action="append",
    )

    parser.add_argument(
            "--print-rooms",
            help="Print all available rooms"
    )

    args = parser.parse_args()

    HOME = args.homeserver
    USERNAME = args.username
    ROOM_IDS = args.rooms
    EXCLUDE_ROOM_IDS = args.exclude_rooms
    ACCESS_TOKEN = args.access_token

    asyncio.run(main())
