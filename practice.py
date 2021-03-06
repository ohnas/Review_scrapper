import time
import datetime
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
# 크롬 브라우저를 띄우지 않고 실행
options.headless = True
options.add_argument("window-size=1920x1080")
# user-agent 값을 보내기
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
)
browser = webdriver.Chrome(options=options)
url = "https://smartstore.naver.com/the_3/products/6142640270"
browser.get(url)
# 로딩이 완전히 될때까지 4초 대기
time.sleep(4)
# 브라우저 맨 아래까지 스크롤 하기
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

soup = BeautifulSoup(browser.page_source, "lxml")
pages = soup.find("div", {"class": "_1HJarNZHiI"})
hidden_next_page = pages.find("a", {"class": "_2Ar8-aEUTq"})["aria-hidden"]

reviews_list = []
#'다음 ' 페이지의 속성이 "true" 일 경우(리뷰페이지가 10개 이하일때)
if hidden_next_page == "true":
    for page_number in range(2, len(pages)):
        time.sleep(0.7)
        # 클릭해야하는 페이지 element 찾기
        page = browser.find_element(
            By.XPATH,
            f"//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[{page_number}]",
        )

        # 클릭에서 오류가 발생해서 구글링 해보니 아래 코드를 적으라고함(스택오버플로어에서 찾음), 답변을 보니 이유는 다들 모르지만 아래코드로 하면 실행은 가능
        browser.execute_script("arguments[0].click()", page)
        review_soup = BeautifulSoup(browser.page_source, "lxml")
        reviews = review_soup.find_all("div", {"class": "_1YShY6EQ56"})
        for review in reviews:
            content = review.find("div", {"class": "YEtwtZFLDz"}).find(
                "span", {"class": "_3QDEeS6NLn"}
            )
            content = content.text.split("\n")
            if len(content) > 1:
                content = "".join(content)
            else:
                content = str(content[0])

            rate = review.find("div", {"class": "_2V6vMO_iLm"}).find(
                "em", {"class": "_15NU42F3kT"}
            )
            rate = int(rate.text)

            created = review.find("div", {"class": "_2FmJXrTVEX"}).find(
                "span", {"class": "_3QDEeS6NLn"}
            )
            created = created.text.replace(".", "")
            created = "20" + created
            created = created[0:6]
            # created = datetime.datetime.strptime(created, "%Y%m").date()

            review_item = {
                "content": content,
                "rate": rate,
                "created": created,
            }
            reviews_list.append(review_item)

#'다음 ' 페이지의 속성이 "false" 일 경우(리뷰페이지가 10개 이상일때)
elif hidden_next_page == "false":
    while True:
        try:
            for page_number in range(2, 13):
                time.sleep(0.7)
                page = browser.find_element(
                    By.XPATH,
                    f"//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[{page_number}]",
                )
                browser.execute_script("arguments[0].click()", page)
                review_soup = BeautifulSoup(browser.page_source, "lxml")
                reviews = review_soup.find_all("div", {"class": "_1YShY6EQ56"})
                for review in reviews:
                    content = review.find("div", {"class": "YEtwtZFLDz"}).find(
                        "span", {"class": "_3QDEeS6NLn"}
                    )
                    content = content.text.split("\n")
                    if len(content) > 1:
                        content = "".join(content)
                    else:
                        content = str(content[0])

                    rate = review.find("div", {"class": "_2V6vMO_iLm"}).find(
                        "em", {"class": "_15NU42F3kT"}
                    )
                    rate = int(rate.text)

                    created = review.find("div", {"class": "_2FmJXrTVEX"}).find(
                        "span", {"class": "_3QDEeS6NLn"}
                    )
                    created = created.text.replace(".", "")
                    created = "20" + created
                    created = created[0:6]
                    # created = datetime.datetime.strptime(created, "%Y%m").date()

                    review_item = {
                        "content": content,
                        "rate": rate,
                        "created": created,
                    }
                    reviews_list.append(review_item)
        except:
            break

# 크롬드라이브 종료
browser.quit()


df = pd.DataFrame(reviews_list)
df = df.drop_duplicates(keep="first", subset=["content", "rate", "created"])
df = df.groupby("rate").count()
df = df.reset_index()
print(df)
