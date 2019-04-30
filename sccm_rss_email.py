#! /usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from time import mktime, strftime
import feedparser
import smtplib
from email.message import EmailMessage

f = open("sccm_rss.txt")
RSS_URLS = f.readlines()

feeds = []
for url in RSS_URLS:
    feeds.append(feedparser.parse(url))

rss = []
lastHourDateTime = datetime.today() - timedelta(hours=48)

for feed in feeds:
    try:
        title = feed['entries'][0].title
        url = feed['entries'][0].link
        date_p = feed['entries'][0].updated_parsed

        # convert from struct_date to str
        # t = strftime("%Y-%m-%d %H:%M:%S", date_p)

        # convert struct date to datetime.datetime
        t = datetime.fromtimestamp(mktime(date_p))

        if t > lastHourDateTime:
            rss.append(title + ' ' + url + '<br>')

    except IndexError:
        pass


def send_email(username, rss):
    msg = EmailMessage()
    msg['Subject'] = 'ConfigMgr news'
    msg['From'] = 'username@contoso.com'
    msg['To'] = username + '@contoso.com'
    msg.add_alternative("""\
    <html>
      <head></head>
      <body>
        
      </body>
    </html>
    """.join((["<li> " + item for item in rss])), subtype='html')
    with smtplib.SMTP('mail.contoso.com', 587) as s:
        s.starttls()
        s.login('your_username', 'your_password')
        s.send_message(msg)


if rss:
    send_email('email_send_to@contoso.com', rss)
