# -*- coding: utf-8 -*-
import datetime
from JDCrawl.utils.db_manager_mysql import DbManager
"""
MySQL数据库控制工具
"""
class MySql_Utils:
    def __init__(self):
        self.dbManager = DbManager()

    #添加/替换商品信息
    def replace_good(self,item):
        create_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        params = [item['search_word'],item['title'], item['pic_url'],
                  item['detail_url'],item['view_price'],item['nick'], create_time]
        sql = "REPLACE INTO t_goods(search_word,title,pic_url,detail_url,view_price,nick,create_time) VALUES (%s,%s,%s,%s,%s,%s,%s)"
        return self.dbManager.edit(sql, params)

# if __name__ == '__main__':


#     replace_detail('sss', 'sss', 'saaa')

