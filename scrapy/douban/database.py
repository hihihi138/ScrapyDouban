#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql

MYSQL_DB = 'douban'
MYSQL_USER = 'root'
MYSQL_PASS = 'Pa55word'
MYSQL_HOST = 'localhost'

connection = pymysql.connect(host=MYSQL_HOST, port=3306, user=MYSQL_USER,
                             password=MYSQL_PASS, db=MYSQL_DB,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
