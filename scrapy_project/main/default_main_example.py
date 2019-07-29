import os
import sys
from scrapy.cmdline import execute


# 将执行目录切换到 与scrapy.cfg 文件同级
DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(DIR)


# 执行爬虫文件的命令
execute(['scrapy', 'crawl', 'spider_name'])

