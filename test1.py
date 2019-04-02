import sys
import os
# sys.path.append('D:\\MyTest\\mypython\\')
# sys.path.append('.')

# 搜索指定文件夹


def search_file(url, suffix=['.xls', '.xlsx']):
    for root, _, files in os.walk(url):
        for name in files:
            if os.path.splitext(name)[1] in suffix:
                yield os.path.join(root, name)

for i in search_file(r'C:\Users\wk\Desktop\食品检测数据'):
    print(i)
#go = os.walk(r'C:\Users\wk\Desktop\食品检测数据')

#for i in next(go):
    #print(i)