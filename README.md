internetSpeedMonitor
======
###### Open a pull request with a better name

This project is twofold -- periodically test and store internet speed metrics in InfluxDB, and tweet the average measurements out daily.

For the speed tests a Python library called speedtest-cli is used to calculate download (Mbit/s), upload (Mbit/s), and ping (ms)

## Requirements
- Python 3.X.X + pip
    - [speedtest-cli][1]
    - [Twython][2]
    - [InfluxDB][3]
- Local InfluxDB
    - [Setting up InfluxDB on raspberryPi][4]
- Twitter dev account
    - [Setting up a Twitter bot on raspberryPi][4]
    
[4]: https://pimylifeup.com/raspberry-pi-influxdb/
[5]: https://pimylifeup.com/raspberry-pi-twitter-bot/
## Usage


- Add twitter API credentials + Influx client data to `config.ini`
- `$ pip3 install requirements.txt`

    Install Python requirements
- `python3 speedmonitor.py --speedtest`
    
    Executes `speedtest-cli` and stores `download, upload, ping` data to configured InfluxDB
- `python3 speedmonitor.py --tweet`
    
    Queries InfluxDB and tweets the average for each metric (download, upload, ping) for measurements within passed 24 hours
_____

## Cron setup
You'll need data throughout the day which is why we'll use cron jobs to run our script every 15 minutes. You can add your own using `sudo crontab -e` or run the following command:
```
$> (crontab -u userhere -l; echo "*/15 * * * * python3 /<path/to>/speedmonitor.py --speedtest" ) | crontab -u <user> -
```
_____

You can schedule the tweet to be sent at 8 PM using this command:
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


[1]: https://github.com/sivel/speedtest-cli
[2]: https://github.com/ryanmcgrath/twython
[3]: https://github.com/influxdata/influxdb-python
