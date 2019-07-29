# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

import time
import scrapy
import json
from lxml import etree
from scrapy import signals
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class SeleniumMiddleware(object):
    
    def __init__(self):

        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # 使用无头谷歌浏览器模式
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')

    def process_request(self, request, spider):

        return None
        
    def process_response(self, request, response, spider ):

        return response

