# Mar 31th, 10:39 PM, 2018 @ dorm 602
# 爬取起点中文小说前100页的信息, 并用 Excel 表格储存
# 爬取的信息有：小说名，作者ID，小说类型，完成情况，摘要，字数
# URL
# https://www.qidian.com/all?page=1
# https://www.qidian.com/all?page=2
# https://www.qidian.com/all?page=3
# ...
# https://www.qidian.com/all?page=100

import time
import xlwt
import requests
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'}
allbook_info = []

def get_info(url):
    res = requests.get(url, headers=headers)
    selector = etree.HTML(res.text)
    # 选取大节点
    infos = selector.xpath('/html/body/div[2]/div[5]/div[2]/div[2]/div/ul/li')
    for info in infos:
        title = info.xpath('div[2]/h4/a/text()')[0]
        author = info.xpath('div[2]/p[1]/a[1]/text()')[0]
        style = info.xpath('div[2]/p[1]/a[2]/text()')[0]
        state = info.xpath('div[2]/p[1]/span/text()')[0]
        introduction = info.xpath('div[2]/p[2]/text()')[0].strip()
        words = info.xpath('div[2]/p[3]/span/span/text()')
        book_info = list([title,author,style,state,introduction,words]) # 字数是乱码方块？
        allbook_info.append(book_info)

def main():
    urls = ['https://www.qidian.com/all?page={page}'.format(page=page) for page in range(1,101)]
    for url in urls:
        get_info(url)
        time.sleep(1)
    head = ['title','author','style','state','introduction','words']
    workbook = xlwt.Workbook(encoding='utf-8')
    sheet = workbook.add_sheet('Book')
    for i, item in enumerate(head):
        sheet.write(0,i,head[i])
    for i in range(len(allbook_info)):
        for j, item in enumerate(allbook_info[i]):
            sheet.write(i+1,j,item)
        i += 1
    workbook.save('E:\AllPrj\PyCharmPrj\py-crawler\Excel 存储\小说统计.xls')
if __name__ == '__main__':
    main()
