#!/usr/bin/env python

import re
import subprocess
import speedtest

def runSpeedTest(db_client):

  # run speedtest tool and parse results
  speedtester = speedtest.Speedtest()
  speedtester.get_best_server()
  speedtester.download()
  speedtester.upload()
  speedtester.results.share()
  results_dict = speedtester.results.dict()

  download = results_dict['download']/1000000
  upload = results_dict['upload']/1000000
  ping = results_dict['ping']

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
