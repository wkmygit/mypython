import re
import requests
from lxml import html
from bs4 import BeautifulSoup

#根据URL获取网页HTML
def getHtml(url):
    res = requests.get(url)
    html = BeautifulSoup(res.text,'lxml')
    return html

#清除过滤emoji表情
def filter_emoji(desstr,restr=''):
    try:
        co = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        co = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    return co.sub(restr,desstr)

#保存数据到文件中
def data_insert(content):
    with open('f:/data.txt','a+') as data:
        data.write(content)

#获取百度贴吧数据
def get_teiba():
    url_1 = 'http://tieba.baidu.com'
    num = 0
    while num < 200:
        url = 'https://tieba.baidu.com/f?kw=%E6%9D%8E%E6%AF%85&ie=utf-8&pn=50' + str(num)
        soup = getHtml(url)
        res = soup.find_all('div',class_='t_con cleafix')
        for i in res:
            hf = int(i.span.get_text())
            if hf > 10:
                data_1 = filter_emoji(i.a.get_text())
                data_2 = '回复数量：%s' % i.span.get_text()
                data_3 = '地址：%s' % (url_1 + i.a.attrs['href'])
                data_4 = '%s\n%s\n%s\n\n' % (data_1,data_2,data_3)
                data_insert(data_4)
        num += 50
    print('导出成功')
    
if __name__ == '__main__':
    get_teiba()
