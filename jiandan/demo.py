import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import re
import os

browser = webdriver.Chrome()
# 设置网站等待时间
wait = WebDriverWait(browser, 10)

def get_html(url):
    '''
        利用 webdriver 来请求对应的网站
        :param url: 最后一页的网址
        :return: html
    '''
    print('正在爬取...')
    try:
        browser.get(url)
        html = browser.page_source
        if html:
            return html
    except EOFError:
        return None

def download(html):
    '''
    解析网站, 写图片进文件夹内，并获取下一页链接以及下一页的页码
    :param html:
    :return: 下一页链接
    '''
    soup = BeautifulSoup(html, 'lxml')
    imgs = soup.select('img')         #返回值为list
    url = soup.select('#body #comments .comments .cp-pagenavi a')[-1]   #获取到的列表最后一个为下一页（标号变小）
    href = re.findall('href="(.*?)"', str(url))    #使用正则表达式提取其中的网址
    next_page = int(re.findall('\d+', str(url))[0])  # 下一页的页码（列表）
    current_page = next_page+1
    next_url = 'https:' + href[0]

    count = 1
    for img in imgs:
        img_url = re.findall('src="(.*?)"', str(img))      # 图片链接
        if img_url[0][-3:] == 'jpg' and img_url[0][:4] == 'http':
            print('正在下载：%s 第 %s 张' % (img_url[0], count))
            write_fo_file(img_url[0], "第{}页".format(current_page) , count)
            count += 1
    return next_url,next_page

def write_fo_file(url, num, count):
    '''
    把抓取到的图片保存到本地文件
    :param url: 图片链接
    :param num: 页数（根据页数创建文件夹）
    :param count: 第几张（图片编号）
    :return: None
    '''
    dirName = u'{}/{}'.format('煎蛋网', num)
    if not os.path.exists(dirName):
        os.makedirs(dirName)

    filename = '%s/%s/%s.jpg' % (os.path.abspath('.'), dirName, count)   #绝对路径 / 煎蛋网+页码 / 第几张
    print(filename)
    pic = requests.get(url).content
    with open(filename, 'wb+') as jpg:                     #以二进制写    自动关闭文件
        jpg.write(pic)

def main():
    '''
    执行的主函数
    :return:
    '''
    url = 'http://jandan.net/ooxx'
    next_page_num = 2
    while next_page_num > 1:
        html = get_html(url)          #输出“正在下载”并返回网页HTML信息
        next_page = pares_one(html)   #下载图片，返回下一页的网址和页码
        url = next_page[0]
        next_page_num = next_page[1]
    print("下载完成")


if __name__ == '__main__':
    main()
