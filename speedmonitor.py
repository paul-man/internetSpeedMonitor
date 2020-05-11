#!/usr/bin/python

import sys
import re
import configparser
from twython import Twython
from influxdb import InfluxDBClient
from os.path import dirname, abspath
from specdumbot import sendTweet
from speedtester import runSpeedTest

path = dirname(abspath(__file__))

config = configparser.ConfigParser()
config.read(path + '/config.ini')
db_config = config['influxdb']
tw_config = config['twitter']

db_client = InfluxDBClient(db_config['HOST'], db_config['PORT'], db_config['USER'], db_config['PASS'], db_config['DATABASE'])

action = re.sub('--', '', sys.argv[1])

if action == "tweet":
  #Create a copy of the Twython object with all our keys and secrets to allow easy commands.
  tw_client = Twython(tw_config['API_KEY'],tw_config['API_SECRET'],tw_config['ACCESS_KEY'],tw_config['ACCESS_SECRET'])
  sendTweet(db_client, tw_client)
elif action == "speedtest":
  runSpeedTest(db_client)
