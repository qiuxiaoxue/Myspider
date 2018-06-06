抓取春雨医生经典问答十四个科室的医患对话数据

环境：BeautifulSoup 、requests、pandas、csv
数据爬虫结构：spidermain.py util.py
 
 
1.抓取数据格式：
按照科室循环，每个科室各300对话，每个对话数据按列存储。
 
 
2.数据处理后格式：dataProc.py
除去数据中的无关文字字符并将数据存储为一纵列方便后面的情感标签判断。
 

2.情感分析：na?ve bayes
依赖库 numpy 、 jieba

给数据打标签chatdata_lable()
 
 
 
3.数据量10M , 21000行，简单的合并医患问答对话

最后打好标签的对话数据。
 
