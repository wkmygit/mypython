import sys
import os
import xlrd
import xlwt
from Common import mssql_helper
mssql = mssql_helper.MSSQL()


# 查询食品类型ID
def get_foodtype(foodname):
    sql = "SELECT ID FROM dbo.Detection_FoodType WHERE ParentID<>0 AND FoodTypeName='%s'" % foodname
    row = mssql.exec_query(sql)
    if len(row) > 0:
        return row[0][0]
    else:
        return 0

# 保存数据到文件中
def data_insert(content):
    with open('f:/data.txt', 'a') as data:
        data.write(content)

# 导入Excel
def read_execl(url):
    row_count = [0, 0]
    # 打开Execl
    workbook = xlrd.open_workbook(url)
    # 根据sheet索引或者名称获取sheet内容
    sheet = workbook.sheet_by_index(0)
    row_count[0] = sheet.nrows
    data = []
    data_no = []
    for i in range(sheet.nrows):
        rows = sheet.row_values(i)
        food = rows[0].strip()
        foodtype = get_foodtype(food)  # 获取食品类型ID
        if foodtype > 0:
            rows[0] = foodtype
            data.append(tuple(rows))
        else:
            data_no.append(rows[0])
    try:
        # 没有匹配的数据写入txt文件
        for i in list(set(data_no)):
            data_insert(i+'\n')
        
        # 写入数据库
        sql = 'INSERT INTO dbo.Detection_FoodTypeOffer(FoodTypeID,DetectionItem,StandardMethod,Price) VALUES(%d,%s,%s,%s)'
        res = mssql.exec_batch_insert(sql, data)
        if res > 0:
            row_count[1] = len(data)
        return row_count
    except Exception as e:
        print(e)
        return row_count

#遍历所有Excel
def search_file(url, suffix=['.xls', '.xlsx']):
    for root, _, files in os.walk(url):
        for name in files:
            if os.path.splitext(name)[1] in suffix:
                yield os.path.join(root, name)


if __name__ == '__main__':
    url = input('请输入文件夹路径：')
    for i in search_file(url):
        row = read_execl(i)
        print(i)
        print('导入完成,共%d条数据,成功导入%d条' % (row[0], row[1]))
        print('------------------------------------------------')
    input()
