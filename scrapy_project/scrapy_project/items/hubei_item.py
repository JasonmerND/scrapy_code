# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import re
import json
import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, Join, Compose,TakeFirst

class SetNone(object):

    def __call__(self, values):
        if not values:
            return ["NULL"]
        else:
            return values


class CrwalHubeiItemLoader(ItemLoader):
    default_output_processor = TakeFirst()
    default_input_processor = SetNone()


class CrwalHubeiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    url = scrapy.Field()
    # company: 企业名称
    company = scrapy.Field()
    # corp_code: 企业唯一代码
    corp_code = scrapy.Field()

    # cert_type_num: 证书类型
    cert_type_num = scrapy.Field()

    # project_name: 项目名称
    project_name = scrapy.Field()

    # project_num: 项目编码
    project_num = scrapy.Field()

    # address: 项目地址
    address = scrapy.Field()

    # build_corp_name: 建设单位
    build_corp_name = scrapy.Field()

    # build_corp_code: 唯一代码
    build_corp_code = scrapy.Field()

    # province: 发生所在省
    province = scrapy.Field()

    # city: 发生所在市
    city = scrapy.Field()

    # jianjie: 奖励简介
    jianjie = scrapy.Field()

    # wenhao: 奖励决定文号
    wenhao = scrapy.Field()
    # date: 奖励日期(发生日期)
    date = scrapy.Field()
    # content: 奖励决定内容
    content = scrapy.Field()

    # jiangli_department: 奖励部门
    jiangli_department = scrapy.Field()
    # jiangli_level: 奖励级别
    jiangli_level = scrapy.Field()
    # dengji_department: 登记部门
    dengji_department = scrapy.Field()
    # telephone: 登记部门联系电话
    telephone = scrapy.Field()

    def get_insert_sql(self):
        """
        数据入库
        """
        insert_sql = """
            insert into hubei(
                url,
                company,
                corp_code,
                cert_type_num,
                project_name,
                project_num,
                address,
                build_corp_name,
                build_corp_code,
                province,
                city,
                jianjie,
                wenhao,
                date,
                content,
                jiangli_department,
                jiangli_level,
                dengji_department,
                telephone
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        params = [(
                self['url'],
                self['company'],
                self['corp_code'],
                self['cert_type_num'],
                self['project_name'],
                self['project_num'],
                self['address'],
                self['build_corp_name'],
                self['build_corp_code'],
                self['province'],
                self['city'],
                self['jianjie'],
                self['wenhao'],
                self['date'],
                self['content'],
                self['jiangli_department'],
                self['jiangli_level'],
                self['dengji_department'],
                self['telephone']
        )]
        return insert_sql, params

    def get_select_sql(self):
        """
        去重
        """
        select_sql = """
            select * from hubei
            where url = %s
        """
        params = (self['url'], )
        return select_sql, params
