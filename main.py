#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import subprocess
from multiprocessing import Process

import pymongo
import redis

from config import get_mysql


def get_content():
    m_cli = pymongo.MongoClient()
    while True:
        url = r_cli.spop('faileds')
        print url
        if not url:
            return
        try:
            #things = subprocess.check_output("node /home/ubuntu/Wappalyzer/src/Wappalyzer/src/drivers/npm/index.js {}".format(url).split())
            things = subprocess.check_output("docker run --rm wappalyzer/cli {}".format(url).split())
        except Exception as e:
            print e
            r_cli.sadd('faileds',url)
            continue
        print things
        things = json.loads(things)
        print things
        try:
            things['url'] = things.pop('urls')[0]
            m_cli['wappalyzer']['data'].insert_one(things)
        except pymongo.errors.DuplicateKeyError as e:
            print e


r_cli = redis.Redis()


def push_to_redis():
  #  for i in open('../1.txt'):
  #      r_cli.sadd('domain', i.strip())
  #  return
    mysql_cli, cursor = get_mysql()
    cursor.execute('select distinct domain from domain where status>0 ')
    for i in cursor.fetchall():
        i = i[0]
        r_cli.sadd('domain', i)


if __name__ == '__main__':
    #push_to_redis()
    print "load over"
    p_list = [Process(target=get_content) for i in range(120)]
    for i in p_list:
        i.start()
    for i in p_list:
        i.join()
