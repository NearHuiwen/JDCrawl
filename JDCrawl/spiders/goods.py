import copy
from threading import Lock

import scrapy
from scrapy import Request

from JDCrawl.items import JdcrawlItem
from JDCrawl.utils.common import Common
from JDCrawl.utils.cookie_utils import Cookie_Utils
from JDCrawl.utils.db_controller_mysql import MySql_Utils


class GoodsSpider(scrapy.Spider):
    name = 'goods'

    def __init__(self):
        # 爬取总数
        self.totalCount = 0
        self.mutex = Lock()  # 线程锁保证线程安全

        # 动态cookie
        self.cookie_utils = Cookie_Utils()
        # 伪造请求头
        self.headers = {
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'sec-ch-ua': '"\\Not;A\"Brand";v="99", "Google Chrome";v="85", "Chromium";v="85"',
            'sec-ch-ua-mobile': '?0',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'https://search.jd.com/Search?keyword=%E7%9C%BC%E9%95%9C&enc=utf-8&wq=%E7%9C%BC%E9%95%9C&pvid=6dedd21c53594c608ad969e0264c5bac',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
        }
        self.mysql_utils = MySql_Utils()

        self.search_word_list = ["面霜","眼镜"]

    def start_requests(self):
        '''准备开始爬取首页数据
        :return:
        '''
        for index in range(len(self.search_word_list)):
            keyword = self.search_word_list[index]
            page = 1  # 第几页，每页30条信息
            # 根据销量排行爬取
            req_url = f"https://search.jd.com/Search?keyword={keyword}&wq={keyword}&psort=3&click=0"
            meta = {"keyword": keyword, "page": page}
            req_headers = copy.deepcopy(self.headers)
            req_headers["Referer"] = req_url
            req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
            print(f"准备爬取[{keyword}]第[1]页req_url=[{req_url}]的列表信息\n")
            yield Request(url=req_url, method='GET', headers=req_headers, callback=self.pagination_parse, meta=meta,
                          dont_filter=True)

    def pagination_parse(self, response):
        keyword = response.meta.get('keyword')
        page = response.meta.get('page')
        li_list=response.xpath('//*[@id="J_goodsList"]/ul/li')
        if(1==page):
            totalPage=int(response.xpath('//*[@id="J_topPage"]/span/i/text()').extract_first().strip())
        else:
            totalPage = response.meta.get('totalPage')
        for li_index in range(len(li_list)):
            li_item=li_list[li_index]
            item = JdcrawlItem()
            item["detail_url"]="https:"+li_item.xpath('./div/div[@class="p-name p-name-type-2"]/a/@href').extract_first().strip()
            item["pic_url"]="https:"+li_item.xpath('./div/div[@class="p-img"]/a/img/@data-lazy-img').extract_first().strip()
            item["title"]=Common.spider_data_by_xpath(li_item,'./div/div[@class="p-name p-name-type-2"]/a/em')
            item["view_price"]=float(li_item.xpath('./div/div[@class="p-price"]/strong/i/text()').extract_first().strip())
            nick =li_item.xpath('./div/div["p-shop"]/span/a/text()')
            if(nick):
                item["nick"]=nick.extract_first().strip()
            else:
                item["nick"]=""
            item["search_word"] = keyword
            self.add_totalCount(1)
            print(f'爬取[{item["detail_url"]}]的信息成功，目前已爬取共[{self.totalCount}]条数据\n')
            yield item
        if (page < totalPage and page < 10):
            page += 1
            s=(page-1)*30+1
            req_url = f"https://search.jd.com/s_new.php?keyword={keyword}C&psort=3&wq={keyword}&psort=3&page={page}&s={s}&click=0"
            meta = {"keyword": keyword, "page": page,"totalPage":totalPage}
            req_headers = copy.deepcopy(self.headers)
            req_headers["Referer"] = req_url
            req_headers["Cookie"] = self.cookie_utils.getCookieByPoll()
            print(f"准备爬取[{keyword}]第[{page}]页req_url=[{req_url}]的列表信息\n")
            yield Request(url=req_url, method='GET', headers=req_headers, callback=self.pagination_parse, meta=meta,
                          dont_filter=True)

    # 统计总数
    def add_totalCount(self, count):
        self.mutex.acquire()
        self.totalCount += count
        self.mutex.release()

