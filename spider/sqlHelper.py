# -*- coding: utf-8 -*-

import logging
import pymysql
from spider.settings import DATABASE_CONFIG
from datetime import datetime


class SqlHelper(object):
    def __init__(self):
        self.conn = pymysql.connect(**DATABASE_CONFIG)
        self.table_name = datetime.now().strftime("detail_%Y_%m_%d_%H_%M_%S")
        try:
            self.conn.select_db('3158_spider')
            self.init()
        except BaseException:
            self.create_database('3158_spider')
            self.conn.select_db('3158_spider')
            self.init()

    def init(self):
        # 创建抓取记录表
        command = (
            "CREATE TABLE IF NOT EXISTS {} ("
            "`id` BIGINT (15) NOT NULL PRIMARY KEY AUTO_INCREMENT,"
            "`name` CHAR(200) DEFAULT NULL,"
            "`url` VARCHAR(255) DEFAULT NULL,"
            "`desc` TEXT DEFAULT NULL,"
            "`market` TEXT DEFAULT NULL,"
            "`images_path` TEXT DEFAULT NULL"
            ") ENGINE=InnoDB".format(self.table_name))
        self.create_table(command)

    def create_database(self, database_name):
        try:
            command = 'CREATE DATABASE IF NOT EXISTS %s DEFAULT CHARACTER SET \'utf8\' ' % database_name
            with self.conn.cursor() as cur:
                cur.execute(command)
        except Exception as e:
            logging.warning('sql helper create_database exception:%s' % str(e))

    def create_table(self, command):
        try:
            with self.conn.cursor() as cur:
                cur.execute(command)
            self.conn.commit()
        except Exception as e:
            logging.warning('sql helper create_table exception:%s' % str(e))

    def insert(self, data):
        try:
            sql = "INSERT INTO "+self.table_name+"(`name`, `url`, `desc`, `market`, `images_path`)" \
                  " VALUES(%s, %s, %s, %s, %s)"
            with self.conn.cursor() as cur:
                cur.execute(sql, data)
            self.conn.commit()
        except Exception as e:
            logging.warning('sql helper insert exception msg:%s' % e)
