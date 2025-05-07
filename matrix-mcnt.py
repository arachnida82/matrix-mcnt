#!/usr/bin/env python3

import asyncio
import argparse
import getpass
import sys
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
USER_PASS = None

async def client_login(
        hserv: str,
        usr_id: str,
        tk: str,
        pw: str
)-> AsyncClient:
    client = AsyncClient(HOME_SERVER, USER_ID)

    if ACCESS_TOKEN:
        client.access_token = ACCESS_TOKEN
        return client

    passwd = USER_PASS if USER_PASS else getpass.getpass()
    if isinstance(await client.login(passwd), LoginResponse):
        return client
    return None


async def main() -> None:
    client = None

    try:
        client = await client_login(HOME_SERVER, USER_ID, ACCESS_TOKEN, USER_PASS)
        if not client:
            print(f"Could not log on to {USERNAME} to {HOME}")
            sys.exit(1)
        print(f"Logged on as {USERNAME} to {HOME}")
        await client.sync(timeout=30000)

        tmp_rooms = await get_rooms(client)
        rooms = []
        for room in tmp_rooms:
            if room["room_id"] not in EXCLUDE_ROOM_IDS:
                rooms.append(room)

        for room in rooms:
            print(f"{room['room_id']} | {room['display_name']}")

        # TODO: unread = sum_unread(rooms)

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client:
            print("logging out.")
            await client.logout()
            await client.close()


async def sum_unread(client: AsyncClient, rooms: list[dict]):
    print("TODO")

async def get_rooms(client: AsyncClient) -> list[dict]:
    rooms = []

    for room_id, room in client.rooms.items():
        rooms.append({
            "room_id": room_id,
            "display_name": room.display_name,
        })

    return rooms

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
            "--passwd",
            help="Supply a password to prevent prompting"
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
            help="A list of Room(s) ID(s) to exclude (eg. '!Abcdefghijklmnopqr' '!2Abcdefghijklmnopq')",
            nargs="+",
            default=[],
    )

    parser.add_argument(
            "--print-rooms",
            help="Print all available rooms"
    )

    args = parser.parse_args()

    HOME = args.homeserver
    USERNAME = args.username
    USER_ID = f"@{USERNAME}:{HOME}"
    ROOM_IDS = args.rooms
    EXCLUDE_ROOM_IDS = args.exclude_rooms
    ACCESS_TOKEN = args.access_token
    USER_PASS = args.passwd

    asyncio.run(main())
