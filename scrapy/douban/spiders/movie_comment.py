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
    # start_urls = {
    #     # str(i['douban_id']): ('https://m.douban.com/rexxar/api/v2/movie/%s/interests?count=5&order_by=hot' % i['douban_id']) for i in movies
    #     '26394152': ('https://m.douban.com/rexxar/api/v2/movie/26394152/interests?count=20&start=%s&order_by=hot' % i) for i in range(0, 100, 25)
    # }
    url_template = 'https://m.douban.com/rexxar/api/v2/movie/26394152/interests?count=20&start={}&order_by=hot'

    def start_requests(self):
        # for (key, url) in self.start_urls.items():
        for i in range(500, 60000, 20):
            headers = {
                # 'Referer': 'https://m.douban.com/movie/subject/%s/comments' % key
                'Referer': 'https://m.douban.com/movie/subject/26394152/comments'
            }
            bid = ''.join(random.choice(string.ascii_letters + string.digits) for x in range(11))
            cookies = {
                'bid': bid,
                'dont_redirect': True,
                'handle_httpstatus_list': [302],
            }
            yield Request(self.url_template.format(i), headers=headers, cookies=cookies)

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
