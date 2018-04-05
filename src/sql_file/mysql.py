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
            self.close_db()
        self.db_connect = MySQLdb.connect(self.host, self.user, self.passwd, self.db, charset="utf8")

    # 创建单例连接
    def __new__(cls, *args, **kwargs):
        if not hasattr(OperateMysql, "_instance"):
            with OperateMysql._instance_lock:
                if not hasattr(OperateMysql, "_instance"):
                    OperateMysql._instance = object.__new__(cls)
        return OperateMysql._instance

    # 获取游标，才能执行sql语句
    def get_cursor(self):
        if self.db_connect is not None:
            return self.db_connect.cursor()
        else:
            self.db_connect = MySQLdb.connect(self.host, self.user, self.passwd, self.db, charset="utf8")
            return self.db_connect.cursor()

    # 关闭连接
    def close_db(self):
        if self.db_connect is not None:
            self.db_connect.close()

    # 创建表格
    def create_table(self, table_name='default', head_of_table=[]):
        cursor = self.get_cursor()

        if cursor is not None:
            cursor.execute("DROP TABLE IF EXISTS %s" % table_name)
            SQL = """CREATE TABLE %s ( 
                        id int(4) primary key not null auto_increment""" % table_name
            if len(head_of_table) is not 0:
                for num in range(0, len(head_of_table)):
                    for key, value in head_of_table[num].items():
                        SQL += """, 
                          %s %s""" % (key, value)
            SQL += """
                     )"""

            cursor.execute(SQL)
            print '%s 表格创建成功' % table_name

    # 插入数据
    def insert_table(self, table_name='default', content_data=[]):
        cursor = self.get_cursor()

        if cursor is not None:
            SQL = "insert into %s values( " % table_name
            if len(content_data) is not 0:
                SQL += 'null, '
                for num in range(0, len(content_data)):
                    if num is not len(content_data) - 1:
                        SQL += "'%s', " % content_data[num]
                    else:
                        SQL += "'%s' " % content_data[num]
                    print content_data[num]
            SQL += ")"

            try:
                # 执行sql语句
                cursor.execute(SQL)
                # 提交到数据库执行
                self.db_connect.commit()
                print 'insert 成功'
            except:
                # Rollback in case there is any error
                self.db_connect.rollback()
                print 'insert 失败'
            print 'insert 完成'

    # 删除数据
    def delete_table(self, table_name='default', delete_string_sql=''):
        cursor = self.get_cursor()
        print delete_string_sql
        if cursor is not None:
            SQL = "delete from %s" % table_name
            if delete_string_sql.strip() is not '':
                SQL += " %s" % delete_string_sql
                # for num in range(0, len(data)):
                #     if num is not len(data) - 1:
                #         SQL += "'%s', " % data[num]
                #     else:
                #         SQL += "'%s' " % data[num]
                #     print data[num]
            SQL += ""

            try:
                # 执行sql语句
                cursor.execute(SQL)
                # 提交到数据库执行
                self.db_connect.commit()
                print 'delete 成功'
            except:
                # Rollback in case there is any error
                self.db_connect.rollback()
                print 'delete 失败'
            print 'delete 完成'

    # 更新数据
    def update_table(self, table_name='default', update_string_sql=''):
        cursor = self.get_cursor()
        print update_string_sql
        if cursor is not None:
            SQL = "update %s set" % table_name
            if update_string_sql.strip() is not '':
                SQL += " %s" % update_string_sql
                # for num in range(0, len(data)):
                #     if num is not len(data) - 1:
                #         SQL += "'%s', " % data[num]
                #     else:
                #         SQL += "'%s' " % data[num]
                #     print data[num]
            SQL += ""
            try:
                # 执行sql语句
                cursor.execute(SQL)
                # 提交到数据库执行
                self.db_connect.commit()
                print 'update 成功'
            except:
                # Rollback in case there is any error
                self.db_connect.rollback()
                print 'update 失败'
            print 'update 完成'

    # 查询数据
    def query_table(self, table_name='default', query_string_sql=''):
        cursor = self.get_cursor()
        if cursor is not None:
            SQL = "select * from %s" % table_name
            if query_string_sql.strip() is not '':
                SQL += " %s" % query_string_sql
                # for num in range(0, len(data)):
                #     if num is not len(data) - 1:
                #         SQL += "'%s', " % data[num]
                #     else:
                #         SQL += "'%s' " % data[num]
                #     print data[num]
            SQL += ""
            cursor.execute(SQL)
            result = cursor.fetchall()

            if result is not None:
                result_list = []
                for num in range(1, len(result)):
                    result_list.append(result[num])
                print 'query 完成，查询结果： %s' % result_list
                return result_list
            else:
                print 'query 完成，查询结果不存在'
                return None

    # 获取表头
    def get_table_header(self, table_name='default'):
        cursor = self.get_cursor()
        if cursor is not None:
            SQL = "show columns from %s" % table_name
            cursor.execute(SQL)
            result = cursor.fetchall()

            if result is not None:
                result_list = []
                for num in range(1, len(result)):
                    result_list.append(result[num][0])
                print '获取表头 ：%s' % result_list
                return result_list

            else:
                print '获取表头，表头不存在'
                return None
