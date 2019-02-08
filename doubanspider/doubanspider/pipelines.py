# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import scrapy
from scrapy import Request
import mysql.connector
from mysql.connector import errorcode
from settings import mysqlconfig
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exceptions import DropItem


class DoubanspiderPipeline(object):
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
        sql = "insert into python_spider (movie_num,movie_name,movie_introduce,movie_star,movie_eval) values ('%s','%s','%s','%s','%s')" % (
            item['movie_num'], item['movie_name'], item['movie_introduce'], item['movie_star'], item['movie_eval'])
        cur = cnx.cursor()
        try:
            cur.execute(sql)
            cnx.commit()
            print('insert into success')
        except  mysql.connector.Error as err:
            print('insert into error')
            print item['movie_num'], item['movie_name'], item['movie_introduce'], item['movie_star'], item['movie_eval']
            print err
        cur.close()
        cnx.close()
        return item


class ImageDown(ImagesPipeline):
    print ("######我在下载")

    def get_media_requests(self, item, info):
        image_url = item['movie_image_url']
        yield scrapy.Request(image_url)

    def item_completed(self, results, item, info):
        # 创建图片存储路径
        path = [x['path'] for ok, x in results if ok]
        # 判断图片是否下载成功，若不成功则抛出DropItem提示
        if not path:
            print u'正在保存图片突突突突突突拖拖拖拖拖：', item['movie_image_url']
            raise DropItem('Item contains no images')
        print u'正在保存图片：', item['movie_image_url']
        print u'主题', item['movie_name']
        return item
