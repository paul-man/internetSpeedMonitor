#!/usr/bin/env python

import re
import subprocess

def runSpeedTest(db_client):

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
              "host": "pi",
              "download": "Mbit/s",
              "upload": "Mbit/s",
              "ping": "ms"
          },
          "fields" : {
              "download": float(download),
              "upload": float(upload),
              "ping": float(ping)
          }
      }
  ]

  db_client.write_points(speed_measurement_data)
