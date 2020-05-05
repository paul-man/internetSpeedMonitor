#!/usr/bin/env python
import sys
from twython import Twython
from influxdb import InfluxDBClient
from datetime import date
import configparser
from os.path import dirname, abspath

project_root = dirname(dirname(abspath(__file__)))

config = configparser.ConfigParser()
config.read(project_root + '/config.ini')

twitter_c = config['twitter']
influxdb_c = config['influxdb']

#Create a copy of the Twython object with all our keys and secrets to allow easy commands.
api = Twython(twitter_c['API_KEY'],twitter_c['API_SECRET'],twitter_c['ACCESS_KEY'],twitter_c['ACCESS_SECRET'])

#Create DB client
client = InfluxDBClient(influxdb_c['HOST'], influxdb_c['PORT'], influxdb_c['USER'], influxdb_c['PASS'], influxdb_c['DATABASE'])

rs = client.query('SELECT * FROM "internet_speed" WHERE time >= now() - 24h;')
daily_points = list(rs.get_points())

download_count, download_sum = 0, 0
upload_count, upload_sum = 0, 0
ping_count, ping_sum = 0, 0

for point in daily_points:
  if point['download']:
    download_count+=1
    download_sum+=point['download']
  if point['upload']:
    upload_count+=1
    upload_sum+=point['upload']
  if point['ping']:
    ping_count+=1
    ping_sum+=point['ping']

download_avg = round(download_sum / download_count, 2)
upload_avg = round(upload_sum / upload_count, 2)
ping_avg = round(ping_sum / ping_count, 2)


today = date.today()
speed_date = today.strftime("%B %d, %Y")

tweet_text = """Average Internet Speed metrics for {0} (Queens, NY):
Download: {1} Mbit/s
Upload: {2} Mbit/s
Ping: {3} ms

@GetSpectrum
#spectrum #specdumb #internetSpeed #speedTest""".format(speed_date, download_avg, upload_avg, ping_avg)

#Using our newly created object, utilize the update_status to send in the text passed in through CMD
api.update_status(status=tweet_text)

