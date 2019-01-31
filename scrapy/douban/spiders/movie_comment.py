#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import random
import string

import douban.database as db
from douban.items import Comment

from scrapy import Request, Spider

cursor = db.connection.cursor()


class MovieCommentSpider(Spider):
    name = 'movie_comment'
    allowed_domains = ['movie.douban.com']
    sql = 'SELECT douban_id FROM movies WHERE douban_id NOT IN \
           (SELECT douban_id FROM comments GROUP BY douban_id) ORDER BY douban_id DESC'
    cursor.execute(sql)
    movies = cursor.fetchall()
    movie_list = {'26394152': '大黄蜂',
                  '3878007': '海王',
                  '26374197': '蜘蛛侠：平行宇宙',
                  '26796664': '叶问外传：张天志',
                  '26994789': '天气预爆',
                  '26336252': '碟中谍6',
                  '26416062': '侏罗纪世界2',
                  '26426194': '巨齿鲨',
                  '26752088': '我不是药神',
                  '24773958': '复仇者联盟3',
                  '26804147': '摩天营救',
                  '26425063': '无双',
                  '27092785': '李茶的姑妈',
                  '25882296': '狄仁杰之四大天王',
                  '26636712': '蚁人2：黄蜂女现身',
                  '27605698': '西红市首富',
                  '25849049': '超人总动员2',
                  '26366496': '邪不压正',
                  '25917789': '铁血战士',
                  '26810318': '阿尔法：狼伴归途',
                  '27069427': '黄金兄弟',
                  '25986662': '疯狂的外星人',
                  '30163509': '飞驰人生',
                  '26266893': '流浪地球',
                  '4221462': '掠食城市',
                  '26744597': '云南虫谷',
                  '26425062': '武林怪兽',
                  }

    url_template = 'https://m.douban.com/rexxar/api/v2/movie/{}/interests?count=20&start={}&order_by=hot'

    def start_requests(self):
        for (id, title) in self.movie_list.items():
            print(title)
            for i in range(0, 500, 20):
                headers = {
                    # 'Referer': 'https://m.douban.com/movie/subject/%s/comments' % key
                    'Referer': 'https://m.douban.com/movie/subject/{}/comments'.format(id)
                }
                bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
                cookies = {
                    'bid': bid,
                    'dont_redirect': True,
                    'handle_httpstatus_list': [302],
                }
                yield Request(self.url_template.format(id, i), headers=headers, cookies=cookies)

    def parse(self, response):
        if 302 == response.status:
            print(response.url)
        else:
            douban_id = response.url.split('/')[-2]
            items = json.loads(response.body)['interests']
            for item in items:
                comment = Comment()
                comment['douban_id'] = douban_id
                comment['douban_comment_id'] = item['id']
                comment['douban_user_nickname'] = item['user']['name']
                comment['douban_user_avatar'] = item['user']['avatar']
                comment['douban_user_url'] = item['user']['url']
                comment['content'] = item['comment']
                comment['votes'] = item['vote_count']
                yield comment
