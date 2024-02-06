import requests
from bs4 import BeautifulSoup
import io
import csv

baseUrl = "https://takken-siken.com"

exam_year = list(range(2023, 1999, -1))

exam_all = []


for year in exam_year:
    if year in [2021, 2020]:
        exam_all.append(str(year)+'-2')
        exam_all.append(str(year)+'-1')
    else:
        exam_all.append(str(year))

kana = ['ア', 'イ', 'ウ', 'エ', 'オ']


dataLength = 50

# exam_all = ["2018"]
csv_data = io.StringIO()
writer = csv.writer(csv_data)
writer.writerow(['url', 'data', 'subject', 'category', 'question',
                'option1', 'option2', 'option3', 'option4', 'answer', 'explanation', 'difficulty', 'similar', 'imgs'])

for exam in exam_all:
    for questionNum in range(1, dataLength+1):
            # questionNum=6
        try:
            url = baseUrl+"/kakomon/" + \
                str(exam)+"/"+str(questionNum).zfill(2)+".html"
            req = requests.get(url)
            soup = BeautifulSoup(req.content, "html5lib")

            brs = soup.select("br")
            for br in brs:
                br.replace_with("\n")
            soup.select("h3")[0].clear()
            imgs = ""
            q_type = 0

            questionData = soup.select("h2")[0].text
            subjectData1 = soup.select(".bunyalinks>a")[0].text
            categoryData = soup.select(".bunyalinks>a")[1].text
            question = soup.select((".mondai"))[0]
            if len(soup.select(".mondai>.kanaList>li")) > 0:
                q_type = 1

            images = question.select("img")
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
                txt=laws[index].text
                if "２　" in txt:
                    txt='１　'+txt
                soup.select(".lawNo")[0].replace_with(f"<blockquote>{txt0}\n{txt}</blockquote>")
            for item in laws:
                item.clear()
            ans_lis = answerText.select(".kaisetsuList>li")
            if q_type == 0:
                for index, li in enumerate(ans_lis):
                    ans_lis[index].insert(0, f'\n{index+1}\n')
            elif q_type == 1:
                for index, li in enumerate(ans_lis):
                    ans_lis[index].insert(0, f'\n{kana[index]}\n')
                    soup.select(".mondai>.kanaList>li")[
                        index].insert(0, f'\n{kana[index]}\n')

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
            images = answerText.select("img")
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

            answerText = answerText.text.replace("解説\n", "", 1).replace("（<blockquote>","\n<blockquote>").replace("</blockquote>）。","</blockquote>\n")
            difficulty = soup.select(".content.answerBox div div i")[
                0].get("class")[0].replace("level", "")

            data = [url, questionData, subjectData1, categoryData,
                    question, option1, option2, option3, option4, answer, answerText, difficulty, similar, imgs]
            writer.writerow(data)
        except Exception as e:
            print(str(exam) + " " + str(questionNum) + " failed")
            print(e)

    print(str(exam) + " done")

csv_data.seek(0)

file_name = "takken_kakomon.csv"

with open(file_name, mode="w", newline="", encoding="utf-8") as file:
    file.write(csv_data.getvalue())

print("出力完了しました。")
