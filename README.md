# internetSpeedMonitor
Project running on linux used to monitor the network speed and tweet the details (WIP)

## Prerequisites

- Python 3.7.X
- Local InfluxDB setup to accept internet speed measurement data

    TODO: add influxdb setup
- Twitter dev account

    TODO: add twitter bot setup
- Install dependencies within `requirements.txt`
- Add twitter + influx data to `config.ini` 

## Usage

`python3 speedmonitor.py --tweet`
- Queries the configured InfluxDB for measurements within passed 24 hours
- Calculates averages for each metric
- Creates and posts tweet to configured account
_____

`python3 speedmonitor.py --speedtest`
- Executes `speedtest-cli` and stores `download, upload, ping` data to configured InfluxDB


## Cron setup

You'll need data throughout the dat which is why setting up a cron job is useful. You can edit your system's crontab directly or run the following command. The job will be run every 15 minutes for as long as the server is running.
```
$> (crontab -u userhere -l; echo "*/15 * * * * python3 /<path/to>/speedmonitor.py --speedtest" ) | crontab -u <user> -
```
_____

The tweet can also be scheduled. The following cron job will run the command everyday at 8 PM (20:00). `0 20` means 0 minutes and 20 hours.
```
$> (crontab -u userhere -l; echo "0 20 * * * python3 /<path/to>/speedmonitor.py --tweet" ) | crontab -u <user> -`
```

## TODO
- [X] cleanup project structure
- [ ] create setup script to create cronjob
- [ ] create setup instructions
  - [ ] influxdb
  - [ ] python dependancies
  - [ ] twitter bot?
