# -*- coding: cp949 -*-
from bs4 import BeautifulSoup
import urllib.request as req
import urllib.parse


def LoadXMLFromFile():
    Data = None
    url = "http://apis.data.go.kr/B552657/ErmctInfoInqireService/getEgytListInfoInqire?serviceKey=uiHZLqJ3xI1D%2B6DAcB5SF3mJL5rcFqCqo628wClXgoesJSMUUVqGPZJqgMiIzvErTq6%2BwQRFcr27%2BuVERdvuIQ%3D%3D&pageNo=1&startPage=1&numOfRows=408&pageSize=408"
    savename = 'data.xml'

    data = urllib.request.urlopen(url).read()
    text = data.decode('utf-8')

    req.urlretrieve(url, savename)

    xml = open(savename, "r", encoding="utf-8").read()
    Data = BeautifulSoup(xml, "html.parser")
    return Data

def LoadAPIFromIP():
    IPData = None
    url = "http://ip-api.com/xml"
    savename = 'myipinfo.xml'

    data = urllib.request.urlopen(url).read()
    text = data.decode('utf-8')

    req.urlretrieve(url, savename)

    xml = open(savename, "r", encoding="utf-8").read()
    IPData = BeautifulSoup(xml, "html.parser")
    return IPData