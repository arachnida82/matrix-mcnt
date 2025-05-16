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
  --bg                  Syncronize in the background
  --pass-path           A path to a password-store file (e.g., 'Matrix/my_user_name/pass')
  --homeserver SERVER   Matrix homeserver (default: matrix.org)
  --rooms ROOM_IDS      List of room IDs to include (all non-specified rooms will be excluded)
  --exclude-rooms IDS   List of room IDs to exclude
  --print-rooms         Print all available rooms and their unread counts
```

**Examples:**
- Get unread count for all rooms using pass:
```bash
$ python3 matrix-mcnt.py --username 'myusername' --pass-path 'Matrix/myusername/passwd'
42
$ python3 matrix-mcnt.py --username 'myusername' --pass-path 'Matrix/myusername/access-token'
42
```

- Using a custom home-server without `pass` and excluding a room from the result:
```bash
$ python3 matrix-mcnt.py --username 'myusername' --homeserver 'matrix.myserver.com' --exclude-room '!Abcdefghijklmnopqr'
Password for @myusername:matrix.myserver.com:
38 # 38 unread messages not including those from '!Abcdefghijklmnopqr'
```

- Include only a specific room
```bash
$ python3 matrix-mcnt.py --username 'myusername' --room '!Abcdefghijklmnopqr'
Password for @myusername:matrix.org:
4
```

- Pipe `stderr` to `/dev/null` while running in the background
```bash
$ (python3.13 matrix-mcnt.py --username 'myuser' --pass-path 'Matrix/myuser/passwd' --bg) 2> /dev/null
1 # Updates every FETCH_DELAY seconds
```


# Install
1. **Prerequisites**
- Python 3.x
- matrix-nio
- (Optional) [pass](https://www.passwordstore.org/) to prevent password prompting


2. **Clone the repo and satisfy its dependencies**
```bash
git clone https://github.com/arachnida82/matrix-mcnt
cd matrix-mcnt
python3.13 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

# Notes
**Rate limits**. Depends on the home servers configuration. 30 seconds should be sufficient, but you can update `FETCH_DELAY` in [matrix-mcnt.py](https://github.com/arachnida82/matrix-mcnt/blob/main/matrix-mcnt.py#L22)


# Licensing and Acknowledgement
The Matrix Message Count program (matrix-mcnt) is licensed under [GPL-3.0](https://www.gnu.org/licenses/gpl-3.0.en.html). It uses [matrix-nio](https://github.com/matrix-nio/matrix-nio) under the [Apache-2.0 license](https://www.apache.org/licenses/LICENSE-2.0.html) and [Internet Systems Consortium license (ISC)](https://www.isc.org/licenses/). A copy of the GPL-3.0 license has been produced [below](https://github.com/arachnida82/matrix-mcnt/blob/main/LICENSE.txt).
