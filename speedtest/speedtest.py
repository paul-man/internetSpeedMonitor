#!/usr/bin/env python
import re
import subprocess
import configparser
from influxdb import InfluxDBClient
from os.path import dirname, abspath

project_root = dirname(dirname(abspath(__file__)))

config = configparser.ConfigParser()
config.read(project_root + '/config.ini')

db_config = config['influxdb']

# run speedtest tool and parse results
speedtest_response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
ping = re.findall('Ping:\s(.*?)\s', speedtest_response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', speedtest_response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', speedtest_response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')

speed_measurement_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "pi"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping)
        }
    }
]

# Create DB client
client = InfluxDBClient(db_config['HOST'], db_config['PORT'], db_config['USER'], db_config['PASS'], db_config['DATABASE'])
client.write_points(speed_measurement_data)
