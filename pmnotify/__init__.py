#!/usr/bin/env python
import requests, bs4, os, sys
from pync import Notifier


def daemonize():
    fpid = os.fork()
    if fpid!=0:
      # Running as daemon now. PID is fpid
        sys.exit(0)

daemonize()
save_to_array = []
def main():
 while 1:
  base_url = 'https://www.avanza.se/placera/pressmeddelanden.html'
  url = 'https://www.avanza.se'
  html = requests.get(base_url)
  html.raise_for_status()
  getSoup = bs4.BeautifulSoup(html.text)
  elems = getSoup.find('ul', {'class': 'feedArticleList'})
  header = elems.find('div', {'class': 'fLeft'}).extract().get_text().encode('utf-8')
  url_date_rest =  elems.find('a', {'class': 'clearFix'})
  url_date = url_date_rest.find('span', {'class': 'fRight'}).get_text()
  full_url = url+url_date_rest['href'].encode('utf-8')

  # so that we don't notify the same PM multiple times
  if header not in save_to_array:
    Notifier.notify(header, open=full_url, title='Pressmeddelande')
    save_to_array.append(header)

