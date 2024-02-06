import requests
from bs4 import BeautifulSoup
import io
import csv

baseUrl = "https://www.itpassportsiken.com/kakomon"

exam_year = list(range(5, 0, -1))+list(range(31, 20, -1))


exam_all = []
for year in exam_year:
    if year in [5, 4, 3, 31]:
        exam_all.append(str(year).zfill(2)+'_haru')
    elif year in [1, 2]:
        exam_all.append(str(year).zfill(2)+'_aki')
    elif year == 23:
        exam_all.append(str(year).zfill(2)+'_toku')
    else:
        exam_all.append(str(year).zfill(2)+'_aki')
        exam_all.append(str(year).zfill(2)+'_haru')

index = {
    "ア": 1,
    "イ": 2,
    "ウ": 3,
    "エ": 4
}

dataLength = 100

#exam_all = ["05_haru"]
csv_data = io.StringIO()
writer = csv.writer(csv_data)
writer.writerow(['url', 'data', 'subject1', 'subject2', 'category', 'question',
                'option1', 'option2', 'option3', 'option4', 'answer', 'explanation', 'img_q', 'img_a'])

for exam in exam_all:
    for questionNum in range(1, dataLength+1):
        print(questionNum)
        url = baseUrl+"/"+str(exam)+"/q"+str(questionNum)+".html"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html5lib")

        brs = soup.select("br")
        for br in brs:
            br.replace_with("\n")
        soup.select("h3")[0].clear()
        imgs1 = ""

        questionData = soup.select("h2")[0].text
        subjectData1 = soup.select("p")[0].text.split("»")[0].replace(" ", "") if len(soup.select("p")[0].text.split("»"))>0 else ""
        subjectData2 = soup.select("p")[0].text.split("»")[1].replace(" ", "") if len(soup.select("p")[0].text.split("»"))>1 else ""
        categoryData = soup.select("p a")[0].text if len(soup.select("p a"))>0 else ""
        # .replace('\n','',1)[::-1].replace('\n','',1)[::-1]
        question = soup.select(("#mondai"))[0]
        images = question.select("img")
        image_url = []
        for image in images:
            text = " <img>"+"</img> "
            image.replace_with(text)
            imgs1+=(baseUrl+"/"+str(exam)+"/"+image.get("src")+"\n")
            
        
        if len(question.select("li"))==3:
            question.select("li")[0].insert(0, '\na. ')
            question.select("li")[1].insert(0, '\nb. ')
            question.select("li")[2].insert(0, '\nc. ')
        elif len(question.select("li"))==2:
            question.select("li")[0].insert(0, '\n(1) ')
            question.select("li")[1].insert(0, '\n(2) ')
        question=question.text

        option1 = soup.select(("#select_a"))[0].text if len(soup.select(("#select_a")))>0 else ""
        option2 = soup.select(("#select_i"))[0].text if len(soup.select(("#select_i")))>0 else ""
        option3 = soup.select(("#select_u"))[0].text if len(soup.select(("#select_u")))>0 else ""
        option4 = soup.select(("#select_e"))[0].text if len(soup.select(("#select_e")))>0 else ""
        answer_hira = soup.select(("#answerChar"))[0].text
        answer = index[answer_hira]
        answerText = soup.select(("#kaisetsu"))[0]
        if answerText.select(".lia"):
         answerText.select(".lia")[0].insert(0, '\n1\n')
         answerText.select(".lii")[0].insert(0, '\n2\n')
         answerText.select(".liu")[0].insert(0, '\n3\n')
         answerText.select(".lie")[0].insert(0, '\n4\n')
        if len(answerText.select("li"))==3:
            answerText.select("li")[0].insert(0, '\na\n')
            answerText.select("li")[1].insert(0, '\nb\n')
            answerText.select("li")[2].insert(0, '\nc\n')

        # answerText.select("h3")[0].decompose()
        # lis=answerText.select(".kaisetsuList > li")
        # index=1
        # for li in lis:
        #     li.insert_before(str(index)+"\n")
        #     li.insert_after('\n')
        #     index+=1
        # lis=answerText.select("li")
        # for li in lis:
        #     li.insert_after('\n')
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
        # answerTextNoImage=answerText.text.replace('\n','',1)[::-1].replace('\n','',1)[::-1]
        images = answerText.select("img")
        image_url = []
        imgs2=""
        for image in images:
            text = " <img>"+"</img> "
            image.replace_with(text)
            imgs2+=(baseUrl+"/"+str(exam)+"/"+image.get("src")+"\n")

        # .replace('\n','',1)[::-1].replace('\n','',1)[::-1]
        answerText = answerText.text.replace("「ア」","「1」").replace("「イ」","「2」").replace("「ウ」","「3」").replace("「エ」","「4」")
        # difficulty=soup.select(".content.answerBox div div i")[0].get("class")[0].replace("level","")
        imgs1=imgs1[::-1].replace('\n','',1)[::-1]
        imgs2=imgs2[::-1].replace('\n','',1)[::-1]
        data = [url, questionData, subjectData1, subjectData2, categoryData,
                question, option1, option2, option3, option4, answer, answerText, imgs1, imgs2]
        writer.writerow(data)

    print(str(exam) + " done")

csv_data.seek(0)

file_name = "ippass_kakomon.csv"

with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    file.write(csv_data.getvalue())

print("出力完了しました。")
