from BeautifulSoup import BeautifulSoup
from feedparser import parse
from time import sleep
from datetime import datetime, timedelta
import re
import jira_feed_config
from lib import api


latest = None

def strtodt(string):
    return datetime.strptime(string, '%Y-%m-%dT%H:%M:%SZ')

while True:

    feed = parse(jira_feed_config.feed_url)
    if latest is None:
        latest = strtodt(feed['entries'][0].updated) - timedelta(seconds=1)
    entries = [entry for entry in feed['entries'] if strtodt(entry.updated) > latest]
    for entry in entries:
        if strtodt(entry.updated) > latest:
            latest = strtodt(entry.updated)
        bs = BeautifulSoup(entry.title)
        message = ''.join(bs.findAll(text=True))
        if not ('created' in message or 'resolved' in message or 'reopened' in message):
            continue
            api.send_privmsg(jira_feed_config.channel,
                             'JIRA - %s' % re.sub('(\w\w-\d+)',
                                                  '%sbrowse/\\1'%jira_feed_config.url,
                                                  message))

    sleep(jira_feed_config.poll_rate)
