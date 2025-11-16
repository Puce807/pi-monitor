
# ----- General -----

ROLE = "auto" # pi, client, auto
AUTO_CORRECT_CONFIG = False # Should config values be autocorrected if bad
UPDATE_GIT = True # Should program auto check for new commits and pull from repo

# ----- Networking -----

UDP_PORT = 5005 # Port used to send/receive initial connection message
PING_PORT = 5006 # Port used to ping the client
DATA_PORT = 5000 # Port used by the flask server

# ----- Pi -----

POLLING_RATE = 5 # How often the Pi pings and fetches information from the client
DATA_TIMEOUT = 0.5 # How long the PI should wait for new data in the queue before moving on

# --- Display ---

FONT_PATH = "assets/Monocraft.ttc"
BACKGROUND = 255
FOREGROUND = 0

# ----- Client -----

RESOLVE_MISSMATCH = False # If config values differ, automatically make them the same
TIMEOUT_LIM = 25 # How many seconds after the last ping the client will terminate the script
TIMEOUT_THRESH = 16 # How many seconds after the last ping the client will print a warning to terminal
AUTO_RECONNECT = True # Should the listener start again once the pi has disconnected