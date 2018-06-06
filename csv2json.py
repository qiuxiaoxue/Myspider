import sys, getopt
import csv
import json
import pandas as pd

def list2json():
    ipTable = ['158.59.194.213', '18.9.14.13', '58.59.14.21']
    fileObject = open('sampleList.txt', 'w')
    for ip in ipTable:
        fileObject.write(ip)
        fileObject.write('\n')
    fileObject.close()

def dict2json():
    dictObj = {
        'andy': {
            'age': 23,
            'city': 'shanghai',
            'skill': 'python'
        },
        'william': {
            'age': 33,
            'city': 'hangzhou',
            'skill': 'js'
        }
    }
    jsObj = json.dumps(dictObj)
    fileObject = open('jsonFile.json', 'w')
    fileObject.write(jsObj)
    fileObject.close()

def savef(datalist, filename):
    data = datalist
    df = pd.DataFrame()
    for i in range(len(data)):
        df.insert(i, str(i), pd.Series(data[i]))
    df = df.T
    df.to_csv(filename+'.csv',encoding = "utf-8")

def csvfile2json(filename):
    with open(filename ,encoding= "utf-8") as csvfile:
        reader = csv.reader(csvfile)
        reader = list(reader)
        jsonfile = []
        for i in range(len(reader)):
            diolage = []
            diolage.append("[" + str(reader[i][1])+ "]")#.replace(r'\\n"','\\n')
            diolage.append("[" + str(reader[i][2]) + "]")
            print(diolage)
            jsonfile.append(diolage)

        jsObj = json.dumps(jsonfile)
        fileObject = open('jsondata.json', 'w',encoding= "utf-8")
        fileObject.write(jsObj)
        fileObject.close()


csvfile2json("jsonTeutf-8.csv")

# list2json()
# dict2json()