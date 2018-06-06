# -*- coding: utf-8 -*-
import csv
import os
import pandas as pd
from xmnlp import XmNLP


def dataprocessing():
    namelist = get_filename(".\scrapydata")
    for filename in namelist:
        with open(r"scrapydata\\" + filename, encoding="gb18030") as csvfile:
            reader = csv.reader(csvfile)
            reader = list(reader)
            columnsdata = []
            for i in range(1,301):
                rows = [row[i] for row in reader]
                print(rows)
                for j in range(1,len(rows)):
                    if str(rows).strip() != "":
                        columnsdata.append(rows[j])
            savef(columnsdata, filename+"_translated")

def savef(datalist, filename):
    data = datalist
    df = pd.DataFrame()
    for i in range(len(data)):
        df.insert(i, str(i), pd.Series(data[i]))
    df = df.T
    df.to_csv(filename+'.csv')

def trans_col(filename):
    df = pd.DataFrame(pd.read_csv(filename,encoding = "gb18030"))
    new_col = df[0]
    for i in range(1, len(df)):
        b = new_col.append(df[i])
        new_col = b
    new_col = new_col.dropna()
    new_col = new_col.reset_index(drop=True)
    new_col.to_csv("test.csv",encoding = "utf-8")

def del_blankrow(filename):
    df = pd.DataFrame(pd.read_csv(filename,encoding = "gb18030"))
    df = df.dropna().reset_index(drop =True)
    df.to_csv("del_v"+filename ,index = False)

def get_filename(file_dir):
    for root, dirs, files in os.walk(file_dir):
        pass
    return files #获取文件夹上的所有文件名

def get_sentiment(testtxt):
    # 情感分析 example 1
    xm = XmNLP(testtxt)
    if xm.sentiment() < 0.2:
        return 0
    elif xm.sentiment() < 0.4:
        return 1
    elif xm.sentiment() < 0.6:
        return 2
    elif xm.sentiment() < 0.8:
        return 3
    else:
        return 4

def sentiment_lable(filename):
    with open(filename ,encoding= "utf-8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        columnsdata = []
        rows = [row[1] for row in reader]
        for j in range(1, len(rows)):
            chattxt = str(rows[j]).strip().replace('\n','')
            if chattxt == "#######":
                columnsdata.append(chattxt)
            else:
                if "患者:" in chattxt:
                    columnsdata.append(chattxt)
                else:
                    if "医生:" in rows[j-1]:
                        continue
                    else:
                        for n in range(1,10):
                            if j+n >= len(rows):
                                break
                            patientSeries = str(rows[j+n]).strip().replace('\n','')
                            if "患者:" in patientSeries:
                                break
                            elif patientSeries == "#######":
                                break
                            else:
                                chattxt = chattxt + ":" +patientSeries
                    columnsdata.append(chattxt)
        savef(columnsdata, filename + "_comdoc")

def chatdata_lable(filename):
    with open(filename ,encoding= "gb18030") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        columnsdata = []
        rows = [row[1] for row in reader]
        for j in range(1, len(rows)):
            chattxt = str(rows[j]).strip().replace('\n','')
            if chattxt == "#######":
                continue
            else:
                if "患者:" in chattxt:
                    sent_lab1 = get_sentiment(chattxt)
                    chattxt = '"'+ chattxt + '" ,'+ ' '+str(sent_lab1)
                    firstdoc = False
                    for n in range(1, 8):
                        diolage = []
                        if j + n >= len(rows):
                            break
                        patientSeries = str(rows[j + n]).strip().replace('\n', '')
                        if "医生:" in patientSeries:
                            firstdoc = True
                            sent_lab2 = get_sentiment(patientSeries)
                            patientSeries = '"' + patientSeries + '" ,' + ' ' + str(sent_lab2)
                            diolage.append(chattxt)
                            diolage.append(patientSeries)
                            columnsdata.append(diolage)
                        elif patientSeries == "#######":
                            break
                        else:
                            if firstdoc:
                                break
                            else:
                                continue
                else:
                    sent_lab2 = get_sentiment(chattxt)
                    docSeries = '"' + chattxt + '" ,' + ' ' + str(sent_lab2)
                    for n in range(1, 8):
                        diolage = []
                        if j + n >= len(rows):
                            break
                        patientSeries = str(rows[j + n]).strip().replace('\n', '')
                        if "患者:" in patientSeries:
                            sent_lab1 = get_sentiment(patientSeries)
                            patientSeries = '"' + patientSeries + '" ,' + ' ' + str(sent_lab1)
                            diolage.append(docSeries)
                            diolage.append(patientSeries)
                            columnsdata.append(diolage)
                        elif patientSeries == "#######":
                            break
                        else:
                            break
        savef(columnsdata, filename + "_labeled")



# chatdata_lable("del_combinedata_comdoc.csv")


