import oauth2 as oauth
import urllib2 as urllib
import json 
import urllib as ulib
import datetime
import sys
import sqlite3 as lite
import string
import httplib

# See Assignment 1 instructions or README for how to get these credentials
access_token_key = "292576546-r3kpdtSQLWDbKkVpxaCUbxFBhPyzAGtNKKPYAT8v"
access_token_secret = "EaiVekrFfMOsedbLdlECkbFf3a9sLNTPjf6ZktuoQ"

consumer_key = "aU490k8rRu82CDqUkzvtVQ"
consumer_secret = "vppipXrVQA3X1dSYLOhELvvCRinaXBybHH4ov6rJcdo"

_debug = 0

oauth_token    = oauth.Token(key=access_token_key, secret=access_token_secret)
oauth_consumer = oauth.Consumer(key=consumer_key, secret=consumer_secret)

signature_method_hmac_sha1 = oauth.SignatureMethod_HMAC_SHA1()

http_method = "GET"


http_handler  = urllib.HTTPHandler(debuglevel=_debug)
https_handler = urllib.HTTPSHandler(debuglevel=_debug)

'''
Construct, sign, and open a twitter request
using the hard-coded credentials above.
'''
def twitterreq(url, method, parameters):
  req = oauth.Request.from_consumer_and_token(oauth_consumer,
                                             token=oauth_token,
                                             http_method=http_method,
                                             http_url=url, 
                                             parameters=parameters)

  req.sign_request(signature_method_hmac_sha1, oauth_consumer, oauth_token)

  headers = req.to_header()

  if http_method == "POST":
    encoded_post_data = req.to_postdata()
  else:
    encoded_post_data = None
    url = req.to_url()

  opener = urllib.OpenerDirector()
  opener.add_handler(http_handler)
  opener.add_handler(https_handler)

  response = opener.open(url, encoded_post_data)

  return response

def fetchsearchquery():
  params = {'q' : ' ', 'geocode' : '41.6573,-87.8576,10mi', 'lang' : 'en', 'since' : '2012-12-11', 'until' : '2012-12-12'}
  url = "https://api.twitter.com/1.1/search/tweets.json?" + ulib.urlencode(params)
  response = twitterreq(url, "GET", {})
  #output = open('tweets.txt', 'w')
  counter = 0
  print(response)
  for line in response:
    parsed = json.loads(line.strip())
    if "text" in parsed:
      text = parsed["text"].encode('utf-8')
      print(text + '\n')
      #output.write(text)
      #output.write('\n')
      counter += 1
      if counter >= 20:
        output.close()
        break

def fetchsamples():
  con = lite.connect("tweets.db")
  exclude = set(string.punctuation)
  with con: 
    cur = con.cursor()
    url = "https://stream.twitter.com/1/statuses/filter.json"
    parameters = {'language' : 'en', 'locations' : '-87.73666, 41.60297, -87.50844, 41.87888'}
    while True:
      response = twitterreq(url, "POST", parameters)
      try:
        for line in response:
          try:
            parsed = json.loads(line.strip())
            if "text" in parsed:
              coordinates = parsed["coordinates"]
              if not coordinates == None and coordinates["type"] == "Point":
                coordinates = coordinates["coordinates"]
                timestamp = str(datetime.datetime.now())
                username = parsed["user"]["screen_name"]
                if coordinates:
                  text = parsed["text"].encode('utf-8')
                  print(text + " ||")
                  line = ''.join(ch for ch in text if ch not in exclude).strip()
                  line = line.replace("'", "").strip()
                  cur.execute("INSERT INTO TweetData(tweet, coord1, coord2, timestamp, username) VALUES ('{0}', {1}, {2}, '{3}', '{4}');".format(line, coordinates[0], coordinates[1], timestamp, username))
                  con.commit()
          except ValueError:
            continue
      except httplib.IncompleteRead, e:
        continue

if __name__ == '__main__':
  fetchsamples()
  #fetchsearchquery()
