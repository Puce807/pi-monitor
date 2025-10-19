
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
