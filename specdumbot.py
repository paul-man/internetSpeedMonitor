#!/usr/bin/env python

import datetime
from datetime import date
from textwrap import dedent

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def sendTweet(db_client, tw_client):
  # select all data from passed 24 hours
  results_set = db_client.query(
    '''
    SELECT download, upload, ping
    FROM internet_speed
    WHERE time >= now() - 24h;
    '''
  )
  daily_points = list(results_set.get_points())

  # init average data values
  download = {
    'low': float("inf"),
    'count': 0,
    'sum': 0,
    'dip_count': 0,
    'avg': 0
  }
  upload = {
    'low': float("inf"),
    'count': 0,
    'sum': 0,
    'avg': 0
  }
  ping = {
    'high': 0,
    'count': 0,
    'sum': 0,
    'avg': 0
  }

  # TODO: there's gotta be a better way to iterate through the points
  for point in daily_points:
    if point['download']: # skip empty datapoints
      download['count'] += 1
      download['sum'] += point['download']
      if point['download'] < 200:
        download['dip_count'] += 1
      if point['download'] < download['low']:
        download['low'] = round(point['download'], 1)
    if point['upload']:
      upload['count'] += 1
      upload['sum'] += point['upload']
      if point['upload'] < upload['low']:
        upload['low'] = round(point['upload'], 1)
    if point['ping']:
      ping['count'] += 1
      ping['sum'] += point['ping']
      if point['ping'] > ping['high']:
        ping['high'] = round(point['ping'], 1)

  # TODO: move logic to function? Calculate moving average while iterating data above?
  download['avg'] = round(download['sum'] / download['count'], 1)
  upload['avg'] = round(upload['sum'] / upload['count'], 1)
  ping['avg'] = round(ping['sum'] / ping['count'], 1)

  measurements_date = date.today().strftime("%B %d, %Y") # May 04, 2020

  tweet_text = f"""\
  Internet Speed metrics for {measurements_date} (Queens, NY):

  Download (Mbit/s): Average {download['avg']}, Low {download['low']}
  Upload (Mbit/s): Average {upload['avg']}, Low {upload['low']}
  Ping (ms): Average {ping['avg']}, High {ping['high']}

  Download speeds below 200 Mbit/s {download['dip_count']} times

  @GetSpectrum
  #spectrum #specdumb #internetSpeed #speedTest\
  """

  tweet_text = dedent(tweet_text)
  
  # update twitter status
  try:
    tw_client.update_status(status=tweet_text)
  except Exception as e:
    logs = open("./logs/tweet.log", "a+")
    logs.write(f'\n** [ERROR][{now}] Unable to send tweet:\n')
    logs.write(f'{str(e)}\n')
    logs.write(f'"{tweet_text}"\n')
    logs.close()
