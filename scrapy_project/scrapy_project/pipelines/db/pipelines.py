# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi


class MysqlTwistedPipline(object):
    """
    数据入库
    """

    def __init__(self, dbpool):
        self.dbpool = dbpool
        self.error_log = os.path.join(
            os.path.dirname(__file__), 'error_log.txt')

    @classmethod
    def from_settings(cls, settings):
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)

        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        query = self.dbpool.runInteraction(self.do_insert, item)
        query.addErrback(self.handle_error, item, spider)  # 处理异常

    def handle_error(self, failure, item, spider):
        # 处理异步插入的异常
        with open(self.error_log, 'a', encoding='utf-8') as f:
            f.write(
                "------【{}】页面入库失败,错误信息:{}\n--------------\n".format(item['url'], failure))

    def do_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中
        # 先查重
        select_sql, params = item.get_select_sql()
        if cursor.execute(select_sql, params):
            return
        insert_sql, params = item.get_insert_sql()
        cursor.executemany(insert_sql, params)
