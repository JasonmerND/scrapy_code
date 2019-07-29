# -*- coding: utf-8 -*-
import scrapy
# 对应的请求，POST 以及GET
from scrapy.http import FormRequest, Request
# 对应的Item
from ..items.hubei_item import CrwalHubeiItem, CrwalHubeiItemLoader


class defaultSpidersExample(scrapy.Spider):
    # 设置爬虫名
    name = 'spider_name'

    # 设置入口的url
    start_urls = 'http://59.175.169.110/web/corpCxxw/corpCxxwSearch.aspx?fl=1'

    # 设置POST请求中携带请求参数
    data = {
    }


    def start_requests(self):
        """
            爬虫程序的入口方法，作为一个生成器。
            如果需要使用自定义的下载中间件，那么请将
            标记通过meta进行传输，用以判断。

        --  return :
            返回应该用yield，或者返回一个包含请求对象的列表
        

        """
        yield Request(
            url=self.start_urls,
            callback=self.parse,
            dont_filter=True, # 是否url去重，True为不去重
        )

    def parse(self, response):
        """
            处理响应的方法，实现进行页面解析，以及发送下一页请求等
            通常返回类型都为yield形式, 
            
        """
        pass

        
    def detail_parse(self, response):
        """
        明细解析的具体方法
        返回类型也为yield
        """
        # 第一种，也是常用的一种
        Item_loader = CrwalHubeiItemLoader(
            item=CrwalHubeiItem(), response=response)
        Item = Item_loader.load_item()

        # 第二种，为直接生成Item对象，例如Item=CrwalHubeiItem()
        yield Item
