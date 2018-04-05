#!/usr/bin/env python
# coding:utf-8

from excel_file import OperateExcel

from sql_file import OperateMysql
import warnings
import json

warnings.filterwarnings('ignore')

LOAD_FILE_URL = u"../load_excel.xlsx"
EXPORT_FILE_URL = u"../store_excel.xlsx"

table_name = 'mytest'
head_of_table = [{'name': 'CHAR(20)'}, {'age': 'int'}, {'sex': 'CHAR(5)'}, {'income': 'FLOAT'}]
content_data = ['小明', '16', '男', '6000']
delete_string_sql = "where id = '20'"
update_string_sql = "age = age + 1 where id = '21'"
query_string_sql = "where id = '6'"
query_string_sql = ""


def excel_store_mysql(content):
    if content is not None:
        content = json.loads(content, encoding="UTF-8")
        print content
        row_list = {}
        for row in content.iterkeys():
            row_list[int(row)] = row

        print row_list

        head_of_table = content[row_list[1]]
        print 'head : %s' % head_of_table

        content_type = []
        content_type_table = content[row_list[2]]
        for num in range(0, len(content_type_table)):
            if type(content_type_table[num]) is int:
                content_type.append('int')
            elif type(content_type_table[num]) is unicode:
                content_type.append('char(20)')
            elif type(content_type_table[num]) is long:
                content_type.append('bigint')
            elif type(content_type_table[num]) is float:
                content_type.append('float')

        temp = {}
        head_table = []
        for num in range(0, len(head_of_table)):
            print head_of_table[num]
            print content_type_table[num]
            temp[head_of_table[num]] = content_type[num]
            head_table.append(temp)
            temp = {}

        print "head_table ： %s" % head_table
        operateMysql.create_table(table_name=table_name, head_of_table=head_table)

        for row in range(2, len(row_list) + 1):
            print u'second_content[row_list[row]] : %s' % content[row_list[row]]
            operateMysql.insert_table(table_name=table_name, content_data=content[row_list[row]])


def mysql_export_excel(string_sql):
    result_list = operateMysql.query_table(table_name=table_name, query_string_sql=string_sql)
    if result_list is not None:

        table_header = operateMysql.get_table_header(table_name=table_name)
        print """
-----------------------------------------------------------------------------------------------------------------------"""
        print table_header
        content_dict = {0: table_header}

        for num in range(0, len(result_list)):
            print result_list[num]
            temp = []
            for result in range(1, len(result_list[num])):
                temp.append(result_list[num][result])
            content_dict[num + 1] = temp
        print """------------------------------------------------------------------------------------------------------------------------
        """
        data_json = json.dumps(content_dict, encoding="UTF-8", ensure_ascii=False)
        operateExcel.export_excel(data_json)
    else:
        print '查询不到结果'


# 创建数据库的表
# operateMysql.create_table(table_name=table_name, head_of_table=head_table)

# 将数据库的表中插入数据
# operateMysql.insert_table(table_name=table_name, content_data=content_data)

# 将数据库的表中进行数据删除
# operateMysql.delete_table(table_name=table_name, delete_string_sql=delete_string_sql)

# 将数据库的表中数据进行更新
# operateMysql.update_table(table_name=table_name, update_string_sql=update_string_sql)

# 将创建数据库的表中数据进行查询
# result_list = operateMysql.query_table(table_name=table_name, query_string_sql=query_string_sql)
# for num in range(0, len(result_list)):
#     print 'index %s' % result_list[num]


operateExcel = OperateExcel(LOAD_FILE_URL, EXPORT_FILE_URL)
operateMysql = OperateMysql('localhost', 'root', '123', 'test')

# 将excel数据获取出来，并返回一个json类型的信息
# content_json = operateExcel.load_excel()

# 将excel数据存储到mysql中
# excel_store_mysql(content_json)

# 将mysql中的数据存储到excel中
mysql_export_excel(query_string_sql)
