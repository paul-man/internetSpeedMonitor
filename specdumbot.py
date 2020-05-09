#!/usr/bin/env python

from datetime import date
from textwrap import dedent

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

  # TODO: improve average calculation
  # init average data values
  download_count, download_sum , dowload_dip_count = 0, 0, 0
  upload_count, upload_sum = 0, 0
  ping_count, ping_sum = 0, 0
  download_low, upload_low, ping_high = float("inf"), float("inf"), 0

  for point in daily_points:
    if point['download']: # skip empty datapoints
      download_count += 1
      download_sum += point['download']
      if point['download'] < 200:
        dowload_dip_count += 1
      if point['download'] < download_low:
        download_low = point['download']
    if point['upload']:
      upload_count += 1
      upload_sum += point['upload']
      if point['upload'] < upload_low:
        upload_low = point['upload']
    if point['ping']:
      ping_count += 1
      ping_sum += point['ping']
      if point['ping'] > ping_high:
        ping_high = point['ping']

  download_avg = round(download_sum / download_count, 1)
  upload_avg = round(upload_sum / upload_count, 1)
  ping_avg = round(ping_sum / ping_count, 1)

  download_low = round(download_low, 1)
  upload_low = round(upload_low, 1)
  ping_high =  round(ping_high, 1)

  measurements_date = date.today().strftime("%B %d, %Y") # May 04, 2020

  tweet_text = f"""\
  Internet Speed metrics for {measurements_date} (Queens, NY):

  Download (Mbit/s): Average {download_avg}, Low {download_low}
  Upload (Mbit/s): Average {upload_avg}, Low {upload_low}
  Ping (ms): Average {ping_avg}, High {ping_high}

  Download speeds below 200 Mbit/s {dowload_dip_count} times

  @GetSpectrum
  #spectrum #specdumb #internetSpeed #speedTest\
  """

  tweet_text = dedent(tweet_text)
  
  # update twitter status
  tw_client.update_status(status=tweet_text)

