# -*- coding: utf-8 -*-
import scrapy
from doubanspider.items import DoubanspiderItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/top250']


    def parse(self, response):
        movie_list = response.xpath("//ol[@class='grid_view']/li")
        for i_item in movie_list:
            douban_item = DoubanspiderItem()
            douban_item['movie_num'] = i_item.xpath(".//div[@class='item']//em/text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='hd']/a/span[1]/text()").extract_first()
            content_list = i_item.xpath(".//div[@class='info']/div[@class='bd']/p/text()").extract()
            for content_i in content_list :
                content_s = "".join(content_i.split())
                douban_item['movie_introduce'] = content_s
            douban_item['movie_star'] = i_item.xpath(".//div[@class='item']//span[@class='rating_num']/text()").extract_first()
            douban_item['movie_eval'] = i_item.xpath(".//div[@class='item']//div[@class='star']/span[4]/text()").extract_first()
            douban_item['movie_image_url'] = i_item.xpath(".//div[@class='pic']//img/@src").extract_first()

            yield douban_item
        next_link = response.xpath("//span[@class='next']/link/@href").extract()
        if next_link :
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)