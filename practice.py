import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()

options.add_argument("window-size=1920x1080")

options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36"
)

browser = webdriver.Chrome(options=options)

url = "https://smartstore.naver.com/the_3/products/5754869046"
browser.get(url)

time.sleep(4)

browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")


soup = BeautifulSoup(browser.page_source, "lxml")
pages = soup.find("div", {"class": "_1HJarNZHiI"})
hidden_next_page = pages.find("a", {"class": "_2Ar8-aEUTq"})["aria-hidden"]

if hidden_next_page == "true":
    for page_number in range(2, len(pages)):
        time.sleep(0.5)
        page = browser.find_element(
            By.XPATH,
            f"//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[{page_number}]",
        )
        browser.execute_script("arguments[0].click()", page)
elif hidden_next_page == "false":
    while True:
        try:
            for page_number in range(2, 13):
                time.sleep(0.5)
                page = browser.find_element(
                    By.XPATH,
                    f"//*[@id='REVIEW']/div/div[3]/div/div[2]/div/div/a[{page_number}]",
                )
                browser.execute_script("arguments[0].click()", page)
        except:
            break
