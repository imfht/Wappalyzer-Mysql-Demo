#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql

def get_mysql():
    m_cli = pymysql.connect(port=3306, user='', host="", charset='utf8mb4', db='',
                            passwd='')
    return m_cli, m_cli.cursor()
