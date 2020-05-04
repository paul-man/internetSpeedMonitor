import re
import subprocess
from influxdb import InfluxDBClient
import configparser

config = configparser.ConfigParser()
config.read('../config.ini')

influxdb_c = config['influxdb']

response = subprocess.Popen('/usr/local/bin/speedtest-cli --simple', shell=True, stdout=subprocess.PIPE).stdout.read().decode('utf-8')
ping = re.findall('Ping:\s(.*?)\s', response, re.MULTILINE)
download = re.findall('Download:\s(.*?)\s', response, re.MULTILINE)
upload = re.findall('Upload:\s(.*?)\s', response, re.MULTILINE)

ping = ping[0].replace(',', '.')
download = download[0].replace(',', '.')
upload = upload[0].replace(',', '.')

speed_data = [
    {
        "measurement" : "internet_speed",
        "tags" : {
            "host": "RaspberryPiMyLifeUp"
        },
        "fields" : {
            "download": float(download),
            "upload": float(upload),
            "ping": float(ping)
        }
    }
]
client = InfluxDBClient(influxdb_c['HOST'], influxdb_c['PORT'], influxdb_c['USER'], influxdb_c['PASS'], influxdb_c['DATABASE'])
client.write_points(speed_data)
