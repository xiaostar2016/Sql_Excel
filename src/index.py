#!/usr/bin/env python
# coding:utf-8

from excel_file import OperateExcel

from sql_file import OperateMysql
import warnings

warnings.filterwarnings('ignore')

LOAD_FILE_URL = u"../111.xlsx"
EXPORT_FILE_URL = u"../222.xlsx"

# 从mysql中读取数据


# operateExcel = OperateExcel(LOAD_FILE_URL, EXPORT_FILE_URL)
#
# content_json = operateExcel.load_excel()
# operateExcel.export_excel(content_json)

operateMysql = OperateMysql('localhost', 'root', '123', 'test')
operateMysql.save_mysql()
