# -*- coding: utf-8 -*-
# @Author : 李惠文
# @Email : 2689022897@qq.com
# @Time : 2020/8/5 13:55
import hashlib
import time


# 计算方法用时的装饰器（单位：秒）
def count_time(func):
    def fun_time(*args):
        t1 = time.time()
        func(*args)
        t2 = time.time()
        print("运行时间为", t2 - t1, "秒")

    return fun_time
# 生成MD5
def genearteMD5(str):
    # 创建md5对象
    hl = hashlib.md5()
    # Tips
    # 此处必须声明encode
    # 否则报错为：hl.update(str)    Unicode-objects must be encoded before hashing
    hl.update(str.encode(encoding='utf-8'))
    return hl.hexdigest()
class Common:
    # JS unicode编码转为Python unicode中文
    @staticmethod
    def jsUnicode2Python(text):
        text=text.replace("%", "\\")
        return text.encode("utf-8").decode("unicode_escape")

    # xpath爬取（包含换行符）
    @staticmethod
    def spider_data_by_xpath(response, path):
        list = response.xpath(path).xpath('.//text()').extract()
        if (len(list) > 0):
            for index in range(len(list)):
                list[index] = list[index].strip()
            data = "".join(list)
            return data
        else:
            return ""


    # lxml xpath爬取（包含换行符）
    @staticmethod
    def lxml_data_by_xpath(response, path):
        list = response.xpath(path)
        if (len(list) > 0):
            for index in range(len(list)):
                list[index] = list[index].strip()
            data = "".join(list)
            return data
        else:
            return ""

