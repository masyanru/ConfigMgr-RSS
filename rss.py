#! /usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
from datetime import datetime, timedelta
from time import mktime, strftime
import telebot
import feedparser
import pickle
import os

"""
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
"""

telegramToken = os.environ['TELEGRAMTOKEN']

# создание бота с его токеном API и подгружаем конфиг
config = configparser.ConfigParser()
config.read("config.ini")
bot = telebot.TeleBot(telegramToken)


def auto_posting():
    bot.send_message('-179710499', 'Test')

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
            rss.append(title + ' ' + url + '\n\n')

    except IndexError:
        pass

print('лента', rss)

if rss is None:
    # sccm channel
    bot.send_message('-1001054149356', "Сегодня новостей нет! ;( ")
    # test channel
    # bot.send_message('-179710499', "Сегодня новостей нет! ;( ")
else:
    # sccm channel
    bot.send_message('-1001054149356', "Configuration Manager news: \n\n" + "".join(rss), parse_mode="Markdown",disable_web_page_preview=True)
    # test channel
    with open('rss_sccm.txt', 'w') as f:
        f.write(str(rss))

    # bot.send_message('-179710499', "Configuration Manager news: \n\n" + "".join(rss), parse_mode="Markdown", disable_web_page_preview=True)
    f.close()
    # bot.send_message('-179710499', title + ' ' + url, disable_web_page_preview=True)
