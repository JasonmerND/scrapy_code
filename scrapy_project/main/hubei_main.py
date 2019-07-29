import os
import sys
from scrapy.cmdline import execute

DIR  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(DIR)
execute(['scrapy', 'crawl', 'hubei'])

