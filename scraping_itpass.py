import requests
from bs4 import BeautifulSoup
import io
import csv

baseUrl = "https://www.itpassportsiken.com"

exam_year = list(range(5, 0, -1))+list(range(31, 20, -1))


exam_all = []
for year in exam_year:
    if year in [5, 4, 3, 31]:
        exam_all.append(str(year).zfill(2)+'_haru')
    elif year in [1, 2]:
        exam_all.append(str(year).zfill(2)+'_aki')
    elif year == 23:
        exam_all.append(str(year).zfill(2)+'_aki')
        exam_all.append(str(year).zfill(2)+'_toku')
    else:
        exam_all.append(str(year).zfill(2)+'_aki')
        exam_all.append(str(year).zfill(2)+'_haru')

hira_index = {
    "ア": 1,
    "イ": 2,
    "ウ": 3,
    "エ": 4
}

alp = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
maru = ['⓪', '①', "②", "③",  "④", "⑤", "⑥", "⑦", "⑧", "⑨"]

dataLength = 100

# exam_all = ["24_haru"]
csv_data = io.StringIO()
writer = csv.writer(csv_data)
writer.writerow(['url', 'data', 'subject1', 'subject2', 'category', 'question',
                'option1', 'option2', 'option3', 'option4', 'answer', 'explanation', 'imgs'])

for exam in exam_all:
    for questionNum in range(1,  dataLength+1):
        url = baseUrl+"/kakomon/" + str(exam)+"/q"+str(questionNum)+".html"
        req = requests.get(url)
        soup = BeautifulSoup(req.content, "html5lib")

        brs = soup.select("br")
        for br in brs:
            br.replace_with("\n")
        soup.select("h3")[0].clear()
        questionData = soup.select("h2")[0].text
        subjectData1 = soup.select("p")[0].text.split("»")[0].replace(
            " ", "") if len(soup.select("p")[0].text.split("»")) > 0 else ""
        subjectData2 = soup.select("p")[0].text.split("»")[1].replace(
            " ", "") if len(soup.select("p")[0].text.split("»")) > 1 else ""
        categoryData = soup.select("p a")[0].text if len(
            soup.select("p a")) > 0 else ""
        # .replace('\n','',1)[::-1].replace('\n','',1)[::-1]
        question = soup.select(("#mondai"))[0]

        if len(soup.select(".selectList>li>img")) > 0:
            selectImg = soup.select(".selectList>li>img")[0]
            question.append(selectImg)

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

        bb = soup.select("#mondai>.bb")
        for index, li in enumerate(bb):
            soup.select("#mondai>.bb")[
                index].insert(0, '[')
            soup.select("#mondai>.bb")[
                index].append(']')

        for n in range(10):
            aa = soup.select(f".maru{n}")
            for index, li in enumerate(aa):
                li.replace_with(
                    f'\n{maru[n]} {li.text}')

            cc = soup.select(f".li{n}")
            for index, li in enumerate(cc):
                li.replace_with(
                    f'\n({n}) {li.text}')

        uuu = soup.select("u")
        for index, u in enumerate(uuu):
            u.replace_with(f"<u>{u.text}</u>")

        bbb = soup.select("#mondai>ul>li")
        for index, li in enumerate(bbb):
            li.insert(0, f'\n・')
        aaa = soup.select("#mondai>ol>li")
        for index, li in enumerate(aaa):
            li.insert(0, f'\n{alp[index]}. ')

        # if len(question.select("li")) == 3:
        #     question.select("li")[0].insert(0, '\na. ')
        #     question.select("li")[1].insert(0, '\nb. ')
        #     question.select("li")[2].insert(0, '\nc. ')
        # elif len(question.select("li")) == 2:
        #     question.select("li")[0].insert(0, '\n(1) ')
        #     question.select("li")[1].insert(0, '\n(2) ')

        question = question.text
        if (len(soup.select(".img_margin>.showQText")) > 0):
            href = soup.select(".img_margin>.showQText")[0].get("href")
            req2 = requests.get(baseUrl+"/kakomon/" + str(exam)+"/"+href)
            soup2 = BeautifulSoup(req2.content, "html5lib")
            images = soup2.select("img")
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
            for n in range(10):
                aa = soup2.select(f".maru{n}")
                for index, li in enumerate(aa):
                    li.replace_with(
                        f'\n{maru[n]} {li.text}')

                cc = soup2.select(f".li{n}")
                for index, li in enumerate(cc):
                    li.replace_with(
                        f'\n({n}) {li.text}')

            q_2 = soup2.select("#QTextWrap")[0].text
            question = q_2 + "\n" + question

        option1 = soup.select(("#select_a"))[0].text if len(
            soup.select(("#select_a"))) > 0 else ""
        option2 = soup.select(("#select_i"))[0].text if len(
            soup.select(("#select_i"))) > 0 else ""
        option3 = soup.select(("#select_u"))[0].text if len(
            soup.select(("#select_u"))) > 0 else ""
        option4 = soup.select(("#select_e"))[0].text if len(
            soup.select(("#select_e"))) > 0 else ""

        if option1 == "":
            option1 = "ア"
        if option2 == "":
            option2 = "イ"
        if option3 == "":
            option3 = "ウ"
        if option4 == "":
            option4 = "エ"

        answer_hira = soup.select(("#answerChar"))[0].text
        answer = hira_index[answer_hira]
        answerText = soup.select(("#kaisetsu"))[0]
        if answerText.select(".lia"):
            answerText.select(".lia")[0].insert(0, '\n1\n')
            answerText.select(".lii")[0].insert(0, '\n2\n')
            answerText.select(".liu")[0].insert(0, '\n3\n')
            answerText.select(".lie")[0].insert(0, '\n4\n')

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

        # .replace('\n','',1)[::-1].replace('\n','',1)[::-1]
        answerText = answerText.text.replace("「ア」", "「1」").replace(
            "「イ」", "「2」").replace("「ウ」", "「3」").replace("「エ」", "「4」")
        # difficulty=soup.select(".content.answerBox div div i")[0].get("class")[0].replace("level","")
        data = [url, questionData, subjectData1, subjectData2, categoryData,
                question, option1, option2, option3, option4, answer, answerText, imgs]
        writer.writerow(data)

    print(str(exam) + " done")

csv_data.seek(0)

file_name = "itpass_kakomon.csv"

with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    file.write(csv_data.getvalue())

print("出力完了しました。")
