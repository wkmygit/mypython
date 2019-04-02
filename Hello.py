import urllib.request

def getHtml(url):
    page=urllib.request.urlopen(url)
    html=page.read()
    return html.decode()

def content(html):
    str='<div class="content">'
    content=html.partition(str)[2]
    #str1='<div class="article-social">'
    #content=content.partition(str1)[0]
    return content

def title(content,beg=0):
    try:
        title_list=[]
        while True:
            num1=content.index('】',beg)+3
            num2=content.index('</p>',num1)
            title_list.append(content[num1:num2])
            beg=num2
    except ValueError:
        return title_list

def get_img(content,beg=0):
    try:
        img_list=[]
        while True:
            src1=content.index('http',beg)
            src2=content.index('/></p>',src1)
            img_list.append(content[src1:src2])
            beg=src2
    except ValueError:
        return img_list

def many_img(data,beg=0):
    try:
        many_img_str=''
        while True:
            src1=data.index('http',beg)
            src2=data.index('/><br /><img src=',src1)
            many_img_str+=data[src1:src2]+'|'
            beg=src2
    except ValueError:
        return many_img_str

def data_out(title,img):
    with open('F:/data.txt','a+',encoding='utf-8') as fo:
        fo.write('\n')
        for size in range(0,len(title)):
            if len(img)>size:
                if len(img[size])>70:
                    img[size]=many_img(img[size])
                fo.write(title[size]+'&'+img[size]+'\n')
            else:
                fo.write(title[size]+'\n')

content=content(getHtml('http://bohaishibei.com/post/10475/'))
#print(getHtml('http://bohaishibei.com/post/10475/'))
title=title(content)
img=get_img(content)
data_out(title,img)
