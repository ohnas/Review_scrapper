import time
from bs4 import BeautifulSoup
from selenium import webdriver

options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")
options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
)

browser = webdriver.Chrome(options=options)

url = "https://smartstore.naver.com/the_3/products/5020498264"
browser.get(url)

time.sleep(4)
browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

soup = BeautifulSoup(browser.page_source, "lxml")
reviews = soup.find_all("div", {"class": "YEtwtZFLDz"})
reviews_list = []
for item in reviews:
    p = item.find("span", {"class": "_3QDEeS6NLn"})
    review = {
        "p": p.text,
    }
    reviews_list.append(review)
print(reviews_list)
