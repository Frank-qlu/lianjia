import requests
from bs4 import BeautifulSoup
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

def GetUrlHtml(url):
    kv={"User-Agent": "Mozilla/5.0"}
    response=requests.get(url,headers=kv)
    try:
        response.raise_for_status()
        response.status_code=response.apparent_encoding
        return response.text
    except:
        return "URL异常了"
def HtmlParser(response):
     soup=BeautifulSoup(response,"lxml")
     #############提取房源名称
     resblock_name=soup.find_all("div",class_="resblock-name")
     # 使用查询结果再创建一个BeautifulSoup对象,对其继续进行解析
     for a in resblock_name:
         #获取楼盘名字
         name=a.text.split("\n")[1]
         loupan_name.append(name)
         #获取楼盘类型
         type=a.text.split("\n")[2]
         resblock_type.append(type)
         #获取楼盘状态
         status=a.text.split("\n")[3]
         sale_status.append(status)
     ################提取房源位置
     loupan_location=soup.find_all("div",class_="resblock-location")
     for a in  loupan_location:
        location1=a.text.split("\n")[1]
        location2 = a.text.split("\n")[3]
        location3 = a.text.split("\n")[5]
        location=location1+"/"+location2+"/"+location3
        #print(location)
        resblock_location.append(location)
     ###########获取房源均价
     loupan_price=soup.find_all("div",class_="main-price")
     for a in loupan_price:
         price1=a.text.split("\n")[1]
         price2=a.text.split("\n")[2]
         price=price1+price2
         #print(price)
         main_price.append(price1)

def plot(house):
    name=house["resblock_name"]
    price = house["main_price"]
    price = np.array(price)
    name=np.array(name)
    #添加横纵轴名称
    plt.rc('font', family='STXihei', size=11)
    plt.xlabel("楼盘名称")
    plt.ylabel("楼盘价格")
    #设置图例
    plt.legend(["价格"],loc="upper right")
    plt.plot(name,price)
    plt.show()
if __name__ == '__main__':
    url="https://jn.fang.lianjia.com/loupan/"
    loupan_name = []
    resblock_type = []
    sale_status = []
    resblock_location=[]
    main_price=[]

    for i in range(1,22):
        #将url转化为字符串
        i=str(i)
        url=url+"pg"+i+"/"
        #print(url)
        response = GetUrlHtml(url)
        HtmlParser(response)
    #str.strip()过滤
    house = pd.DataFrame({"resblock_name": loupan_name,"main_price":main_price,"resblock_location":resblock_location, " resblock_type": resblock_type, "sale_status": sale_status})
    #调整列的顺序
    house=house[["resblock_name","main_price","resblock_location"," resblock_type", "sale_status"]]
    print(house)
    if not os.path.exists("济南房价数据"):
        os.mkdir("济南房价数据")
    house.to_csv("济南房价数据/房价.csv",encoding = 'gbk', index = False)
    #plot(house)
    # 价格进行降序
    # 删除价格待定的行
    house = house[~house['main_price'].str.contains("价格待定")]
    house=house.sort_values(by="main_price",ascending=False)