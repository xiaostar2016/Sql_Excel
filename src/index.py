#!/usr/bin/env python
# coding:utf-8

from excel_file import OperateExcel

from sql_file import OperateMysql
import warnings

warnings.filterwarnings('ignore')

LOAD_FILE_URL = u"../111.xlsx"
EXPORT_FILE_URL = u"../222.xlsx"
head_of_table = [{'name': 'CHAR(20)'}, {'age': 'int'}, {'sex': 'CHAR(5)'}, {'income': 'FLOAT'}]
content_data = ['小明', '16', '男', '6000']
delete_string_sql = "where id = '20'"
update_string_sql = "age = age + 1 where id = '21'"
query_string_sql = "where id = '21'"
# 从mysql中读取数据


# operateExcel = OperateExcel(LOAD_FILE_URL, EXPORT_FILE_URL)
#
# content_json = operateExcel.load_excel()
# operateExcel.export_excel(content_json)

operateMysql = OperateMysql('localhost', 'root', '123', 'test')
# operateMysql.create_table(table_name="love", head_of_table=head_of_table)
operateMysql.insert_table(table_name='love', content_data=content_data)
# operateMysql.delete_table(table_name='love', delete_string_sql=delete_string_sql)
# operateMysql.update_table(table_name='love', update_string_sql=update_string_sql)
result_list = operateMysql.query_table(table_name='love', query_string_sql=query_string_sql)
for num in range(0, len(result_list)):
    print 'index %s' % result_list[num]
