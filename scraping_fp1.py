import requests
from bs4 import BeautifulSoup
import io
import csv


from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from save_image import save_image

driver = webdriver.Chrome()
driver.implicitly_wait(2)


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


def screenShot(url: str):
    # try:
    print(url)
    driver.get(url)
    scrs = driver.find_element(By.CLASS_NAME, "explan").screenshot_as_base64
    res = save_image({"image": scrs, "image_name": f"{exam}_{questionNum}.png"})
    return f"<img>https://remody-quiz-images.s3.ap-northeast-1.amazonaws.com/selenium_screenshot/{exam}_{questionNum}.png</img>"

    # except Exception as e:
    #     print(e)
    #     return None


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
        print(exam)
    return a


dataLength = 50

# exam_all = ["2021_9"]
csv_data = io.StringIO()
writer = csv.writer(csv_data)
writer.writerow(['url', 'data', 'subject', 'category', 'question',
                'option1', 'option2', 'option3', 'option4', 'answer', 'explanation', 'difficulty', 'similar', 'imgs'])

all = [['2023_9', 41], ['2023_1', 12], ['2022_9', 12], ['2021_9', 40], ['2021_5', 11], ['2021_5', 12], ['2021_5', 29], ['2021_1', 12], ['2020_9', 12], ['2020_9', 41], ['2020_1', 7], ['2020_1', 12], ['2019_9', 30], [
    '2019_1', 12], ['2019_1', 33], ['2019_1', 41], ['2018_1', 12], ['2017_9', 12], ['2017_1', 11], ['2016_9', 11], ['2016_9', 29], ['2016_9', 41], ['2016_1', 12], ['2015_9', 27], ['2015_1', 12], ['2014_9', 12]]


for exam1 in all:
    # for questionNum in range(1, dataLength+1):
    # questionNum=39
    # try:
    exam = exam1[0]
    questionNum = exam1[1]
    url = baseUrl+"/kakomon/" + \
        str(exam)+"/"+str(questionNum).zfill(2)+".html"
    req = requests.get(url)
    soup = BeautifulSoup(req.content, "html5lib")

    brs = soup.select("br")
    for br in brs:
        br.replace_with("\n")
    soup.select("h3")[0].clear()
    q_type = 0

    questionData = soup.select("h2")[0].text
    subjectData1 = soup.select(".bunyalinks>a")[0].text
    categoryData = soup.select(".bunyalinks>a")[1].text
    question = soup.select((".mondai"))[0]
    # if len(soup.select(".mondai>ol>li")) > 0:
    #     q_type = 1

    bbb = soup.select(".mondai>ul>li")
    for index, li in enumerate(bbb):
        soup.select(".mondai>ul>li")[
            index].insert(0, f'\n・')
    aaa = soup.select(".mondai>ol>li")
    for index, li in enumerate(aaa):
        soup.select(".mondai>ol>li")[
            index].insert(0, f'\n{alp[index]}\n')

    print(f"num:{len(soup.select('.explan'))}")
    explan = soup.select(".explan")[0]
    res = screenShot(url)
    if res:
        print(res)
        explan.replace_with(res)

    imgs = ""
    images = soup.select("img")
    for image in images:
        pas = image.get("src")
        if pas[:1] == "/":
            text = " <img>"+baseUrl + pas + "</img> "
            imgs += baseUrl + pas + "\n"
        else:
            text = " <img>"+baseUrl+"/kakomon/" + \
                str(exam)+"/" + pas + "</img> "
            imgs += baseUrl+"/kakomon/" + \
                str(exam)+"/" + pas + "\n"
        image.replace_with(text)

    option1 = soup.select((".selectList>li"))[0].text
    option2 = soup.select((".selectList>li"))[1].text
    option3 = soup.select((".selectList>li"))[2].text
    option4 = soup.select((".selectList>li"))[3].text
    answer = soup.select(".answerChar")[0].text
    answerText = soup.select((".kaisetsu"))[0]
    similars = soup.select(".similar_list_wrap")
    similar = ""
    for item in similars:
        div = item.select(".similar_list>div")
        for num in div:
            link = (num.select("a")[0].get("href") + "\n")
            aa = link.split("/")
            similar += aa[2] + "/" + aa[3].split(".")[0] + "\n"
        item.clear()
    lawNos = soup.select(".lawNo")
    laws = soup.select(".lawBody")
    for index, law in enumerate(lawNos):
        txt0 = law.text
        law.clear()
        txt = laws[index].text
        if "２　" in txt:
            txt = '１　'+txt
        soup.select(".lawNo")[0].replace_with(
            f"<blockquote>{txt0}\n{txt}</blockquote>")
    for item in laws:
        item.clear()
    ans_lis_a = answerText.select(".kaisetsuList>li")
    for index, li in enumerate(ans_lis_a):
        ans_lis_a[index].insert(0, f'\n{index+1}\n')
    ans_lis_b = answerText.select(".kaisetsu>div>ol[type=a]>li")
    for index, li in enumerate(ans_lis_b):
        ans_lis_b[index].insert(0, f'\n{alp[index]}\n')

    question = question.text.replace("\n", "", 1)

    lis = answerText.select("li")
    for li in lis:
        li.insert_after('\n')
    uls = answerText.select("ul")
    for ul in uls:
        ul.insert_after('\n')
    dts = answerText.select("dt")
    for dt in dts:
        dt.insert_after('\n')
    dls = answerText.select("dl")
    for dl in dls:
        dl.insert_after('\n')
    dds = answerText.select("dd")
    for dd in dds:
        dd.insert_after('\n')

    answerText = answerText.text.replace("解説\n", "", 1).replace(
        "（<blockquote>", "\n<blockquote>").replace("</blockquote>）。", "</blockquote>\n")
    difficulty = soup.select(".content.answerBox div div i")[
        0].get("class")[0].replace("level", "")

    data = [url, questionData, subjectData1, categoryData,
            question, option1, option2, option3, option4, answer, answerText, difficulty, similar, imgs]
    writer.writerow(data)
    # except Exception as e:
    #     print(str(exam) + " " + str(questionNum) + " failed")
    #     print(e)

    # print(str(exam) + " done")

csv_data.seek(0)

file_name = "fp1_kakomon.csv"

with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    file.write(csv_data.getvalue())

print("出力完了しました。")
