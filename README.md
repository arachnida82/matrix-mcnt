[![Built with matrix-nio](https://img.shields.io/badge/built%20with-matrix--nio-brightgreen)](https://github.com/poljar/matrix-nio)

# Matrix-mcnt
Matrix message count outputs the number of unread messages of all or of specified rooms to stdout. This can be useful to place in your status bar to see if you have new messages without explicitly checking in the app.


# Usage
```
python3 matrix-mcnt.py --username USERNAME [options]
```

```
Required arguments:
  --username USERNAME     Your Matrix username without the @username:matrix.org format

Optional arguments:
  --access-token TOKEN  Use access token instead of password authentication
  --passwd PASSWORD     Supply password in command line (otherwise will prompt)
  --homeserver SERVER   Matrix homeserver (default: matrix.org)
  --rooms ROOM_IDS      List of room IDs to include (all non-specified rooms will be excluded)
  --exclude-rooms IDS   List of room IDs to exclude
  --print-rooms         Print all available rooms and their unread counts
```

**Examples:**

- get unread count for all rooms

```
$: python3 matrix-mcnt.py --username 'alice' --passwd 'alicespassword123'
23 # 23 unread messages
```

- Get unread count for specific rooms
```
$: python3 matrix-mcnt.py --username 'alice' --passwd 'alicespassword123' --rooms '!Abcdefghijklmnopq' '!Bbcdefghijklmnopq'
4
```

- Using `pass` to supply user password
```
$: python3 matrix-mcnt.py --username 'alice' --passwd $(pass Element/alice)
12
```


# Install
1. **Prerequisites**
- Python 3.x
- matrix-nio
- (Optional) [pass](https://www.passwordstore.org/) to prevent password prompting


2. Clone the repo and satisfy its dependencies
```
git clone https://github.com/arachnida82/matrix-mcnt
cd matrix-mcnt
python3.13 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Notes
**Rate limits**. Depend on home server configuration. Use --bg instead.


# Licensing and Acknowledgement
The Matrix Message Count program (matrix-mcnt) is licensed under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). It uses [matrix-nio](https://github.com/matrix-nio/matrix-nio) under the [Apache-2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html) and [Internet Systems Consortium license (ISC)](https://www.isc.org/licenses/). A copy of the GPL-3.0 license has been produced [below](https://github.com/arachnida82/matrix-mcnt/blob/main/LICENSE.txt).
