# internetSpeedMonitor
Project running on linux used to monitor the network speed and tweet the details (WIP)

## speedtest/

Script runs every 15 minutes and stores the internet speedtest results in a local influxdb

## specdumb/

Script runs each day at 8pm and computes the average measurments for the passed 24 hours. The results are then formatted into a tweet and, well, tweeted

# TODO
- cleanup project structure
- create setup script to create cronjob
- create setup instructions
  - influxdb
  - python dependancies
  - twitter bot?
