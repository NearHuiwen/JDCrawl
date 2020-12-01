# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdcrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    search_word= scrapy.Field()#搜索词
    title = scrapy.Field()#商品标题
    pic_url = scrapy.Field()#简介图片
    detail_url = scrapy.Field()#商品详情网站地址
    view_price = scrapy.Field()#商品价格（最低价）
    nick = scrapy.Field()#商家名称

