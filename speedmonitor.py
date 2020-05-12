#!/usr/bin/python

import sys
import re
import configparser
import os
from twython import Twython
from influxdb import InfluxDBClient
from os.path import dirname, abspath
from specdumbot import sendTweet
from speedtester import runSpeedTest

if not os.path.exists('./logs'):
    os.makedirs('./logs')

path = dirname(abspath(__file__))
config_path = path + '/config.ini'
config = configparser.ConfigParser()
config.read(config_path)

if len(config) == 0:
  print('Config file not found, please create \'config.ini\' file containing Twitter + InfluxDB configuration settings')
  exit()

if not config.has_section('influxdb') or not config.has_section('twitter'):
  print('Configuration missing from \'config.ini\'')
  exit()

db_config = config['influxdb']
tw_config = config['twitter']
action = sys.argv[1] if 1 < len(sys.argv) else None
if action == None or not re.match('--(tweet|speedtest)', sys.argv[1]):
  print('Accepted actions are \'--tweet\' or \'--speedtest\'')
  exit()

db_client = InfluxDBClient(db_config['HOST'], db_config['PORT'], db_config['USER'], db_config['PASS'], db_config['DATABASE'])

if action == "--tweet":
  #Create a copy of the Twython object with all our keys and secrets to allow easy commands.
  tw_client = Twython(tw_config['API_KEY'],tw_config['API_SECRET'],tw_config['ACCESS_KEY'],tw_config['ACCESS_SECRET'])
  sendTweet(db_client, tw_client)
elif action == "--speedtest":
  runSpeedTest(db_client)
