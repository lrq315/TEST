import urllib
import requests
import json
import os

class URLShortenerService:

    def __init__(self, long_url):
        self.long_url = long_url
    
    def generate_short_url(self):
        key = os.getenv('key')
        url = urllib.parse.quote(self.long_url)
        try:
            response = requests.get('http://cutt.ly/api/api.php?key={}&short={}'.format(key, url))
            return json.loads(response.text)['url']['shortLink']
        except:
            # return None
            return "cutt down"
        