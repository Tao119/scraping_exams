import requests
from bs4 import BeautifulSoup
import io
import csv

baseUrl = "https://fp1-siken.com"

exam_year = list(range(2023, 2013, -1))

exam_all = []


for year in exam_year:
    if year in [2023, 2022, 2021, 2019]:
        exam_all.append(str(year)+'_9')
        exam_all.append(str(year)+'_5')
        exam_all.append(str(year)+'_1')
    else:
        exam_all.append(str(year)+'_9')
        exam_all.append(str(year)+'_1')

kana = ['ア', 'イ', 'ウ', 'エ', 'オ']
alp = ['a', 'b', 'c', 'd', 'e']


dataLength = 50

# exam_all = ["2021_9"]


def countShot():
    a = []
    for exam in exam_all:
        for questionNum in range(1, dataLength+1):
                url = baseUrl+"/kakomon/" + \
                    str(exam)+"/"+str(questionNum).zfill(2)+".html"
                req = requests.get(url)
                soup = BeautifulSoup(req.content, "html5lib")
                if len(soup.select(".explan")) > 0:
                    a.append([exam, questionNum])
    return a