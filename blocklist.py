"""
blocklist.py

This file contains the blocklist for the JWT tokens. It is used to blacklist tokens that have been revoked.
It will be imported into app.py and used in the JWT configuration. It is used by 
logout resource so that the token is added to the blocklist when the user logs out.
"""


BLOCKLIST = set()
