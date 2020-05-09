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


- Create `config.ini` and add twitter API credentials + Influx client data
    ```
    [twitter]
    API_KEY = {API_KEY}
    API_SECRET = {API_SECRET}
    ACCESS_KEY = {ACCESS_KEY}
    ACCESS_SECRET = {ACCESS_SECRET}

    [influxdb]
    HOST= localhost
    PORT = 8086
    USER = {INFLUX USER}
    PASS = {INFLUX PASSWORD}
    DATABASE = internetspeed
    ```

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

_____

<a href="https://www.buymeacoffee.com/paulman" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>
