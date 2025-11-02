
# RPi Utilization Monitor Changelog

## [0.0] Initial Setup

- v0.0 Initial Setup
- v0.1 File Structure Setup
- v0.2 Installed libraries and added `requirements.txt`

## [1.0] Data and Communication
- v1.1 Added system utilization functions using psutil
- v1.2: Added basic client-server data communication
  - Implemented Flask server to serve system utilization
  - Set up client to connect and fetch data
- v1.3: Added basic UDP communication
  - Added test.py in for both pi and client
  - Added UDP.py with UDP related functions
  - v.3.1: Fixed errors in client-test.py and pi-test.py
- v1.4: Implemented ping-pong to detect connectivity
  - Added periodic ping from pi and pong reply from client
  - Renamed UDP.py to network.py
  - v1.4.1: Fixed bug when client disconnected, 'second chance' always resulted in script stopping
  - v1.4.2: Fixed bug where pi would not exit 1st while loop
- v1.5: Implemented Flask server communication in test scripts
  - Added flask server code as a class for graceful shutdown
  - v1.5.1: Fixed bug where a thread was started twice and fixed bug where pi would not connect to the correct IP for flask server
  - v1.5.2: Fixed bug with address missing http://
  - v1.5.3: Minor additions
- v1.6: Refactored code to be run from main.py
  - Added automatic role assignment
  - Moved code from test scripts into pi/ and client/
  - v1.6.1: Bug Fixes and Additions
    - Added warnings for not using a pi zero 2
    - Added sleep between "possible Pi disconnect" message
    - Fixed error when flask server did not setup route
  - v1.6.2: Fixed bug where pi would not print flask data
- v1.7: Auto git updating and config synchronisation
  - Automatically pull from GitHub if there is a new commit
  - If config values differ from pi and client, either match or raise error
  - Deleted original test scripts
  - v1.7.1: Fixed bug where UDP message was not encoded correctly
  - v1.7.2: Fixed bug where tuples would not be encoded correctly
  - v1.7.3: Fixed bug where tuples would not be encoded correctly #2
  - v1.7.4: Added debug to help fix bugs
  - v1.7.5 + .6: Added further debug to help fix bugs
  - v1.7.7: Fixed error where client would not send success message to pi so pi would never move onto main loop
- v.1.8: Config validation and client auto-reconnect
  - Added more values to config
  - Added config validation
  - Client automatically starts listener again and closes threads after pi disconnect

## [2.0] Display
- v2.1: Initial display code
  - Added assets folder
  - Added pi/display folder
  - Added eink.py, layout.py and renderer.py
  - Added simple script which displays "hello world"
  - v2.1.1: Fixed config importing error
  - v2.1.2: Moved test code into pi_role.py
  - v2.1.3: Fixed error where display module was incorrectly imported
  - v2.1.4: Moved display files into pi/
  - v2.1.5: Added debug
  - v2.1.6: Changed epaper import to import from epaper module instead of waveshare-epaper
  - v2.1.7: Fix: Instantiated Renderer
  - v2.1.8: Fix: Added size parameter to render_img
- v2.2: Feature: Added basic CPU, RAM, disk and network metrics to display
  - v2.2.1: Fix: Added get_data to Renderer class
  - v2.2.2: Fix: Corrected clearing code in eink_driver.py
  - v2.2.3: Fix: Corrected key names in renderer.py
  - v2.2.4: Fix: Corrected key names in utilization.py
  - v2.2.5: Fix: Corrected key names for disk in utilization.py
  - v2.2.6: Fix: Simplified data dict in utilization.py