#!/usr/bin/env python
# coding:utf-8

import os
import MySQLdb
import threading


class OperateMysql:
    _instance_lock = threading.Lock()
    db_connect = None

    def __init__(self, host=None, user=None, passwd=None, db=None):
        str = ''
        if host is None:
            str += 'host'

        if user is None:
            str += ', ' + 'user'

        if passwd is None:
            str += ', ' + 'password'

        if db is None:
            str += ', ' + 'database'

        if str.strip() != '':
            print '%s 未定义，程序退出' % str
            os._exit(0)

        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db

        if self.db_connect is not None:
            self.db_connect.close()
        self.db_connect = MySQLdb.connect(self.host, self.user, self.passwd, self.db, charset="utf8")

    def __new__(cls, *args, **kwargs):
        if not hasattr(OperateMysql, "_instance"):
            with OperateMysql._instance_lock:
                if not hasattr(OperateMysql, "_instance"):
                    OperateMysql._instance = object.__new__(cls)
        return OperateMysql._instance

    # 将读取到的数据从到mysql中
    def save_mysql(self):

        cursor = self.db_connect.cursor()
        cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")
        sql = """CREATE TABLE EMPLOYEE (
                    FIRST_NAME  CHAR(20) NOT NULL,
                    LAST_NAME  CHAR(20),
                    AGE INT,  
                    SEX CHAR(1),
                    INCOME FLOAT )"""

        cursor.execute(sql)
        return
