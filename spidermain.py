#!/usr/bin/python
#-*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import pandas as pd
import requests
from util import get_HTMLText

import sys
import importlib
import time
import random
importlib.reload(sys)


def scrapy_chatdata(baseurl):
    department_lists = getdepartment(baseurl) #获取科室类型List
    # print(department_lists)
    m = 0
    for onepartmentUrl in department_lists: #遍历所有科室
        m = m + 1
        if m <11 :
            continue
        questionListUrl = scrapy_question(onepartmentUrl,baseurl) #当前科室所有的问题URL
        time.sleep(random.randint(3, 5))
        getchat(questionListUrl)#当前科室所有问题的chatdata
        time.sleep(random.randint(3,5))

def getdepartment(baseUrl):
    url_end = '/pc/qalist/'
    tempbaseUrl = baseUrl + url_end #导航标签首页
    departmentHtml,statue_code = get_HTMLText(tempbaseUrl)
    print(statue_code)
    departmentHtml = str(departmentHtml)
    departmentHtml = BeautifulSoup(departmentHtml,"lxml")
    items = departmentHtml.find_all('ul',class_="tab-type-one first-clinic j-tab-wrap") # 获取科室类型
    items = str(items)
    items = BeautifulSoup(items,"lxml")
    departments = []
    for item in items.find_all('li'):#获取科室类型
        department_item = item.a['href']
        NewUrl = baseUrl + department_item
        departments.append(NewUrl)
    time.sleep(random.randint(5, 10))
    return departments

def scrapy_question(questionUrl,baseurl):
    questionUrlList = []
    for i in range(1,31,1):
        questionHtml, statue_code = get_HTMLText(questionUrl + "?page=" + str(i) + "#hotqa")
        try:
            if statue_code == 200:
                questionHtml = str(questionHtml)
                questionHtml = BeautifulSoup(questionHtml,"lxml")
                chats = questionHtml.find_all("div",class_ = "hot-qa-item")
                for chat in chats:
                    chaturl = baseurl + chat.a['href']
                    questionUrlList.append(chaturl)
                print("问题chat抓取中")
            else:
                break
        except:
            print("获取questionHtml问题结束，共有 "+str(i)+"页。")
        time.sleep(random.randint(3, 5))
        #抓取这个问题的chatdata
    return questionUrlList

def getchat(questionUrlList):
    title = questionUrlList[0].split("/")[-2]
    print("title"+title)
    chatdata = []
    for questionUrl in questionUrlList:
        chatline = scrapy_question_chat(questionUrl)
        chatdata.append(chatline)
        time.sleep(random.randint(5, 10))

    savef(chatdata, str(title))
    #查看是否存在下一页questionHtml
    # nextQuestionPage = ""
    # try:
    #     nextQuestionPage = questionHtml.find_all("a",class_ ="next")
    #     nextQuestionPage = nextQuestionPage[0]['href']
    # except:
    #     print("获取下一页问答错误。。。")
    # if nextQuestionPage != "":
    #     scrapy_question(str(baseurl+nextQuestionPage),baseurl,m+1,title)

def scrapy_question_chat(chaturl):
    chatHtml,statue_code = get_HTMLText(chaturl)
    chatHtml = str(chatHtml)
    chatHtml = BeautifulSoup(chatHtml,"lxml")
    chatHtml = chatHtml.find_all("div",class_ = "block-line")
    chatlines = []
    for chatline in chatHtml:
        name = chatline.h6.text.strip()
        linetxt = chatline.p.text.strip()
        chatlines.append(name + ":" + linetxt)
        # chatlines.append(linetxt)
    chatlines.append("#######")
    return chatlines

def savef(datalist, filename):
    data = datalist
    df = pd.DataFrame()
    tmp = len(data[0])
    index = 0
    for i in range(len(data)):
        if tmp < len(data[i]):
            tmp = len(data[i])
            index = i
    data[0], data[index] = data[index], data[0]
    for i in range(len(data)):
        df.insert(i, str(i), pd.Series(data[i]))

    df.to_csv(filename+'.csv')

def main():
    #春雨经典问答模块
    baseurl='https://www.chunyuyisheng.com'
    scrapy_chatdata(baseurl)

# main()