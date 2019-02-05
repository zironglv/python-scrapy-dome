# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import mysql.connector
from mysql.connector import errorcode
from settings import mysqlconfig


class DoubanspiderPipeline(object):
   # def __init__(self):


    def process_item(self, item, spider):

        cnx = cur = None
        try:
            cnx = mysql.connector.connect(**mysqlconfig)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print('Something is wrong with your user name or password')
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
       # item = dict(item)
        sql = "insert into python_spider (movie_num,movie_name,movie_introduce,movie_star,movie_eval) values ('%s','%s','%s','%s','%s')" %(item['movie_num'],item['movie_name'],item['movie_introduce'],item['movie_star'],item['movie_eval'])
        cur = cnx.cursor()
        try:
            cur.execute(sql)
            cnx.commit()
            print('insert into success')
        except  mysql.connector.Error as err:
            print('insert into error')
            print item['movie_num'],item['movie_name'],item['movie_introduce'],item['movie_star'],item['movie_eval']
            print err
        cur.close()
        cnx.close()
        return item
