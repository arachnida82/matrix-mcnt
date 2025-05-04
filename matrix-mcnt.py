#!/usr/bin/env python3

"""matrix-mcnt
Matrix message count outputs the number of unread messages to stdout.

Run:
    ./matrix-mcnt --all-rooms        (default)

    ./matrix-mcnt --room '!Idstring:matrix.org'

    ./matrix-mcnt --room '!Idstring1:matrix.org' '!Idstring2:matrix.org' '!Idstringn:matrix.org'

"""

if __name__ == "__main__":
    main()
