# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request

from ..items.hubei_item import CrwalHubeiItem, CrwalHubeiItemLoader


class HubeiSpider(scrapy.Spider):
    name = 'hubei'

    start_urls = 'http://59.175.169.110/web/corpCxxw/corpCxxwSearch.aspx?fl=1'

    data = {
        # 跳页方式 lbtnNext 下一页  lbtnGo 跳页
        '__EVENTTARGET': 'lbtnGo',
        # //input[@type='hidden' and @id='__EVENTARGUMENT']/@value
        '__EVENTARGUMENT': '',
        # //input[@type='hidden' and @id='__VIEWSTATE']/@value
        '__VIEWSTATE': '',
        # //input[@type='hidden' and @id='__EVENTVALIDATION']/@value
        '__EVENTVALIDATION': '',
        'txtXm': '',
        'ddlType': '1',
        # 需要跳转的页码
        'txtPageIndex': '',
        'hUrltype': '',
        'hfFl': '1',
    }

    def start_requests(self):

        yield Request(
            url=self.start_urls,
            callback=self.parse,
            dont_filter=True,
        )

    def parse(self, response):
        """
        爬取剩余页数以及明细列表页面
        """

        if 'index_flag' not in response.meta:
            # 获取总页数
            end_page = int(response.xpath(
                "//span[@id='labPageCount']/text()").extract_first())

            # 配置请求参数
            EVENTARGUMENT = response.xpath(
                "//input[@type='hidden' and @id='__EVENTARGUMENT']/@value").extract_first()
            VIEWSTATE = response.xpath(
                "//input[@type='hidden' and @id='__VIEWSTATE']/@value").extract_first()
            EVENTVALIDATION = response.xpath(
                "//input[@type='hidden' and @id='__EVENTVALIDATION']/@value").extract_first()
            self.data['__EVENTARGUMENT'] = EVENTARGUMENT
            self.data['__VIEWSTATE'] = VIEWSTATE
            self.data['__EVENTVALIDATION'] = EVENTVALIDATION

            # 请求后续列表页
            for i in range(1, end_page+1):
                self.data['txtPageIndex'] = str(i)
                yield FormRequest(
                    self.start_urls,
                    formdata=self.data,
                    callback=self.parse,
                    dont_filter=True,
                    meta={
                        "index_flag": True,
                    }
                )

        # 遍历当前的列表，进入解析页面
        detail_list = response.xpath(
            "//*[@id='tableList']/tr/td[2]/a/@href").extract()
        for a in detail_list:
            yield Request(
                url=response.urljoin(a),
                callback=self.detail_parse,
            )

    def detail_parse(self, response):
        """
        明细解析
        """
        Item_loader = CrwalHubeiItemLoader(
            item=CrwalHubeiItem(), response=response)
        # url: response.url
        Item_loader.add_value('url', response.url)
        # company: //td[@id='corpName']/text()
        Item_loader.add_xpath('company', "//td[@id='corpName']/text()")

        # corp_code: 企业唯一代码: //td[@id='CorpCode']/text()
        Item_loader.add_xpath('corp_code', "//td[@id='CorpCode']/text()")

        # cert_type_num: 证书类型: //td[@id='CertTypeNum']/text()
        Item_loader.add_xpath(
            'cert_type_num', "//td[@id='CertTypeNum']/text()")

        # project_name: 项目名称: //td[@id='prjName']/text()
        Item_loader.add_xpath('project_name', "//td[@id='prjName']/text()")

        # project_num: 项目编码: //td[@id='PrjNum']/text()
        Item_loader.add_xpath('project_num', "//td[@id='PrjNum']/text()")

        # address: 项目地址: //td[@id='Address']/text()
        Item_loader.add_xpath('address', "//td[@id='Address']/text()")

        # build_corp_name: 建设单位: //td[@id='BuildCorpName']/text()
        Item_loader.add_xpath(
            'build_corp_name', "//td[@id='BuildCorpName']/text()")

        # build_corp_code: 唯一代码: //td[@id='BuildCorpCode']/text()
        Item_loader.add_xpath(
            'build_corp_code', "//td[@id='BuildCorpCode']/text()")

        # province: 发生所在省: //td[@id='DSZ']/text()
        Item_loader.add_xpath('province', "//td[@id='DSZ']/text()")

        # city: 发生所在市: //td[@id='QX']/text()
        Item_loader.add_xpath('city', "//td[@id='QX']/text()")

        # jianjie: 奖励简介: //td[@id='txtJljj']/text()
        Item_loader.add_xpath('jianjie', "//td[@id='txtJljj']/text()")

        # wenhao: 奖励决定文号: //td[@id='AWARDNUMBER']/text()
        Item_loader.add_xpath('wenhao', "//td[@id='AWARDNUMBER']/text()")

        # date: 奖励日期(发生日期): //td[@id='AwardDate']/text()
        Item_loader.add_xpath('date', "//td[@id='AwardDate']/text()")

        # content: 奖励决定内容: //td[@id='awardcontent']/text()
        Item_loader.add_xpath('content', "//td[@id='awardcontent']/text()")

        # jiangli_department: 奖励部门: //td[@id='AWARDDEPARTNAME']/text()
        Item_loader.add_xpath('jiangli_department',
                              "//td[@id='AWARDDEPARTNAME']/text()")

        # jiangli_level: 奖励级别: //td[@id='AwardDepartType']/text()
        Item_loader.add_xpath(
            'jiangli_level', "//td[@id='AwardDepartType']/text()")

        # dengji_department: 登记部门: //td[@id='txtDjbm']/text()
        Item_loader.add_xpath('dengji_department',
                              "//td[@id='txtDjbm']/text()")

        # telephone: 登记部门联系电话: //td[@id='txtDjbmLxdh']/text()
        Item_loader.add_xpath('telephone', "//td[@id='txtDjbmLxdh']/text()")

        Item = Item_loader.load_item()
        yield Item
