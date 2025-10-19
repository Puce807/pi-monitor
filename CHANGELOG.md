
# RPi Utilization Monitor Changelog

## [0.0] Initial Setup

- v0.0 Initial Setup
- v0.1 File Structure Setup
- v0.2 Installed libraries and added `requirements.txt`

## [1.0] Data
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