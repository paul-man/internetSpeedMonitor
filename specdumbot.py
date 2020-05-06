#!/usr/bin/env python

from datetime import date

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
  download_count, download_sum = 0, 0
  upload_count, upload_sum = 0, 0
  ping_count, ping_sum = 0, 0

  for point in daily_points:
    if point['download']: # skip empty datapoints
      download_count += 1
      download_sum += point['download']
    if point['upload']:
      upload_count += 1
      upload_sum += point['upload']
    if point['ping']:
      ping_count += 1
      ping_sum += point['ping']

  download_avg = round(download_sum / download_count, 2)
  upload_avg = round(upload_sum / upload_count, 2)
  ping_avg = round(ping_sum / ping_count, 2)

  measurements_date = date.today().strftime("%B %d, %Y") # May 04, 2020

  tweet_text = """Average Internet Speed metrics for {0} (Queens, NY):

  Download: {1} Mbit/s
  Upload: {2} Mbit/s
  Ping: {3} ms

  @GetSpectrum
  #spectrum #specdumb #internetSpeed #speedTest""".format(measurements_date, download_avg, upload_avg, ping_avg)

  # update twitter status
  tw_client.update_status(status=tweet_text)

