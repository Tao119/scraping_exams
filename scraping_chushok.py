from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome import service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import io
import csv
import time


driver = webdriver.Chrome()
driver.implicitly_wait(2)


baseUrl = "https://kakomonn.com/chushoks/questions"

exam_all = {}

nums = [66858, 57505, 54896, 48280, 45037, 44809, 44586, 44359]
qnums = [225,226,227,227,227,228,223,227]

j = 0

for i in range(2022, 2014, -1):
    exam_all[i] = [nums[j],qnums[j]]
    j += 1
exam_all={
 2016:[44636,1],
}

# csv_data = io.StringIO()
# writer = csv.writer(csv_data)
# writer.writerow(['url', 'data', 'subject', 'question', 'option1',
#                 'option2', 'option3', 'option4', 'option5', 'answer', 'answer text'])
#with open("chushok.csv", mode="w", newline="", encoding="utf-8") as file1:
#    file1.write('url, data, subject, question, option1, option2, option3, option4, option5, answer, answer text\n')

for exam in exam_all:
    a = None
    #a=44541 if exam == 2015 else None
    for questionNum in range(a or exam_all[exam][0], exam_all[exam][0] + exam_all[exam][1]):
        try:
            url = baseUrl+"/"+str(questionNum)
            driver.get(url)
            wait = WebDriverWait(driver,10)
            wait.until(expected_conditions.element_to_be_clickable(
                (By.NAME, "intAnswerData")))
            driver.execute_script("window.scrollTo(0,{});".format(str(driver.find_element(By.NAME, 'submit').location['y'])))
            driver.find_element(By.NAME, "intAnswerData").click()
            driver.find_element(By.NAME, "submit").click()
            wait.until(expected_conditions.presence_of_element_located(
                (By.CLASS_NAME, "ctr_box_09")))

            # req = requests.get(url)
            soup = BeautifulSoup(driver.page_source, "html5lib")
            imgs = soup.select("img")
            for img in imgs:
                src = img.get("src")
                img.replace_with("\n<img>{}</img>\n".format(src))

            brs = soup.select("br")
            for br in brs:
                br.replace_with("\n")
            
            questionData = soup.select(".ctr_h1")[0].text.replace(" 中小企業診断士の過去問 ","")

            subjectData = soup.select(".ctr_h1")[0].text.split(" ")[3]
            # subjectData=soup.select(".content.bunyalinks a")[0].text
            # categoryData=soup.select(".content.bunyalinks a")[1].text

            question = soup.select((".centerbody01_02"))[0].text.replace('"','""').replace('”','""')
            option1 = soup.select((".centerbody01_26"))[0].text.replace('"','""').replace('”','""')
            option2 = soup.select((".centerbody01_26"))[1].text.replace('"','""').replace('”','""')
            option3 = soup.select((".centerbody01_26"))[2].text.replace('"','""').replace('”','""')
            option4 = soup.select((".centerbody01_26"))[3].text.replace('"','""').replace('”','""')
            option5 = soup.select((".centerbody01_26"))[4].text.replace('"','""').replace('”','""') if len(
                soup.select((".centerbody01_26"))) >= 5 else ""
            answer = soup.select((".ctr_box_09"))[0].text
            for p in soup.select("p"):
                p.append("\n")
            answerText = soup.select((".centerbody01_74"))[0].text.replace("\n選択肢","\n\n選択肢").replace('"','""').replace('”','""')

            data = [url, questionData, subjectData, question, option1,
                    option2, option3, option4, option5, answer, answerText]
        except Exception as e:
            print("error in " + str(exam) + " " + str(questionNum))
            print(e)
            data = ["", "", "", "", "", "", "", "", "", "", ""]
        with open("chushok.csv", mode="a", newline="", encoding="utf-8") as file1:
            file1.write('"')
            file1.write('","'.join(data))
            file1.write('"\n')

    # csv_data.seek(0)
    # file_name = "chushoks_kakomon{}.csv".format(str(exam))
    # with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    #     file.write(csv_data.getvalue())
    # csv_data = io.StringIO()
    # writer = csv.writer(csv_data)
    # writer.writerow(['url', 'data', 'subject', 'question', 'option1',
    #             'option2', 'option3', 'option4', 'option5', 'answer', 'answer text'])

    print(str(exam) + " done")

# csv_data.seek(0)

# file_name="chushoks_kakomon.csv"

# with open(file_name, mode="w", newline="", encoding="utf-8") as file:
#     file.write(csv_data.getvalue())

print("出力完了しました。")
