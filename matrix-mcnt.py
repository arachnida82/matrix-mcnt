#!/usr/bin/env python3

"""
matrix-mcnt: A CLI script to count unread messages from a Matrix account.
"""

import asyncio
import argparse
import getpass
import sys
from nio import(
        AsyncClient,
        MatrixRoom,
        RoomMessageText,
        LoginResponse,
        RoomInfo,
        responses
)
from typing import Optional

async def client_login(
        hserv: str,
        usr_id: str,
        tkn: str,
        pw: str
) -> Optional[AsyncClient]:
    client = AsyncClient(hserv, usr_id)

    if tkn:
        client.access_token = tkn
        return client

    passwd = pw if pw else getpass.getpass()
    if not isinstance(await client.login(passwd), LoginResponse):
        return None
    return client


async def main(args) -> None:
    client = None

    HOME = args.homeserver
    USERNAME = args.username
    USER_ID = f"@{USERNAME}:{HOME}"
    EXCLUDE = args.exclude_rooms
    INCLUDE = args.rooms
    # TODO FIX: Bad
    ACCESS_TOKEN = args.access_token
    USER_PASS = args.passwd

    try:
        client = await client_login(
               f"https://{HOME}", USER_ID, ACCESS_TOKEN, USER_PASS)
        if not client:
            sys.exit(1)

        sync_resp = await client.sync(timeout=30000, full_state=True)
        rooms = await get_rooms(
                client,
                sync_resp,
                INCLUDE,
                EXCLUDE
                )
        if args.print_rooms:
            for room in rooms:
                print(f"{room['room_id']} | {room['display_name']} | Unread: {room['unread_count']}")

        print(await sum_unread(client, rooms))

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if client:
            await client.logout()
            await client.close()

async def sum_unread(client: AsyncClient, rooms: list[dict]) -> int:
    return sum(room["unread_count"] for room in rooms)

async def get_rooms(
        client: AsyncClient,
        sync_response,
        INCLUDE_ONLY_ROOM_IDS: list[str],
        EXCLUDE_ROOM_IDS: list[str]
) -> list[dict]:

    rooms = []
    for room_id, room in client.rooms.items():
        if INCLUDE_ONLY_ROOM_IDS and room_id not in INCLUDE_ONLY_ROOM_IDS:
            continue
        if room_id in EXCLUDE_ROOM_IDS:
            continue

        unread = 0
        if room_id in sync_response.rooms.join:
            room_info = sync_response.rooms.join[room_id]
            if hasattr(room_info, "unread_notifications"):
                unread = room_info.unread_notifications.notification_count

        rooms.append({
            "room_id": room_id,
            "display_name": room.display_name,
            "unread_count": unread
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
            default="matrix.org",
            help="eg. 'matrix.org' or 'matrix.server.com'"
    )

    parser.add_argument(
            "--rooms",
            help="A list of Room(s) ID(s) to strictly include (eg. '!Abcdefghijklmnopqr' '!2Abcdefghijklmnopq')",
            nargs="+",
            default=[],
    )

    parser.add_argument(
            "--exclude-rooms",
            help="Room IDs to strictly exclude eg. '!Abcdefghijklmnopqr' '!2Abcdefghijklmnopq'",
            nargs="+",
            default=[],
    )

    parser.add_argument(
            "--print-rooms",
            help="Print all matching rooms",
            action="store_true"
    )

    parser.add_argument(
            "--bg",
            help="Run script in background"
            # TODO: let run in background, updating in real time.
    )

    asyncio.run(main(parser.parse_args()))
