# -*- coding:UTF-8 -*-

from bs4 import BeautifulSoup
import requests
import sys

class Download(object):
    '''
    类说明：下载笔趣看网站小说《斗罗大陆》
    '''
    def __init__(self):
        self.server = 'http://www.biqukan.com'
        self.target = "http://www.biqukan.com/3_3026/"
        self.names = []      #存放章节名
        self.urls = []     #存放章节连接
        self.nums = 0        #章节数

    def get_download_url(self):
        '''
        函数说明：获取下载链接
        :return:
        '''
        req = requests.get(url=self.target)
        html = req.text
        div_bf = BeautifulSoup(html,"lxml")
        div = div_bf.find_all("div",class_ = "listmain")
        a_bf = BeautifulSoup(str(div[0]),'lxml')
        a = a_bf.find_all("a")
        self.nums = len(a[15:])         #剔除开头的最新章节以及外传，从第15行开始
        for each in a[15:]:
            self.names.append(each.string)
            self.urls.append(self.server + each.get("href"))

    def get_contents(self,target):
        '''
        获取章节内容
        :param self:
        :param target:章节链接
        :return:
        '''
        req = requests.get(url = target)
        html = req.text
        bf = BeautifulSoup(html,"lxml")
        texts = bf.find_all('div',class_ = 'showtxt')
        texts = texts[0].text.replace("\xa0"*8,"\n\n")
        return texts

    def writer(self,name,path,text):
        '''
        将爬取的文章内容写入文件
        :param self:
        :param name:章节名
        :param path:当前路径下，小说保存名称（string）
        :param text:章节内容
        :return:None
        '''
        writer_flag = True
        with open(path,"a",encoding="utf-8") as f:
            f.write(name + '\n')
            f.write(text)
            f.write('\n\n')

if __name__ == "__main__":
    dl = Download()
    dl.get_download_url()
    print("《斗罗大陆》开始下载：")
    for i in range(dl.nums):
        dl.writer(dl.names[i],'斗罗大陆.txt',dl.get_contents(dl.urls[i]))
        sys.stdout.write("已下载：%.3f%%" % float(i/dl.nums) + '\r')
        sys.stdout.flush()          # %.3f是指小数点后三位
    print("《斗罗大陆》下载完成")
