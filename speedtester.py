#!/usr/bin/env python

import speedtest
import datetime

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def runSpeedTest(db_client):

  # run speedtest tool and parse results
  speedtester = speedtest.Speedtest()
  speedtester.get_best_server()
  speedtester.download()
  speedtester.upload()
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

  try:
    db_client.write_points(speed_measurement_data)
  except Exception as e:
    logs = open("./logs/speed.log", "a+")
    logs.write(f'\n** [ERROR][{now}] Unable to write speed metrics:\n')
    logs.write(f'{str(e)}\n')
    logs.write(f'{speed_measurement_data}\n')
    logs.close()
    exit()