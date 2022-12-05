from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from bs4 import BeautifulSoup as bs
from decouple import config
from app.constants import FB_RECENT_TOGGLE
from app.utils import set_up_chrome_driver, single_write_to_db

import time

USERNAME = config('USERNAME')
KEY = config('KEY')


def openSeeMore(browser):
    readMore = browser.find_elements(By.XPATH, "//div[text()='See more']")
    if len(readMore) > 0:
        count = 0
        for i in readMore:
            action = ActionChains(browser)
            try:
                action.move_to_element(i).click().perform()
                count += 1
            except:
                try:
                    browser.execute_script("arguments[0].click();", i)
                    count += 1
                except:
                    continue
        if len(readMore) - count > 0:
            print('readMore issue:', len(readMore) - count)
        time.sleep(1)
    else:
        pass


def getBack(browser):
    if not browser.current_url.endswith('reviews'):
        browser.back()


def archiveAtEnd(browser, reviewList):
    browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);")  # scroll back to the top
    time.sleep(10)

    for idx, l in enumerate(reviewList):
        if idx % 10 == 0:
            if idx < 15:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[0])
            else:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx - 15])

            time.sleep(1)
            try:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx + 15])
            except:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[-1])

            time.sleep(1)
            browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx])

            for r in range(2):
                time.sleep(3)
                try:
                    browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx + 5])
                    time.sleep(3)
                except:
                    browser.execute_script("arguments[0].scrollIntoView();", reviewList[-1])
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx + r * 3])
                time.sleep(3)
                with open(f'./PATH/{str(idx)}_{r}.html', "w", encoding="utf-8") as file:
                    source_data = browser.page_source
                    bs_data = bs(source_data, 'html.parser')
                    file.write(str(bs_data.prettify()))
                    print(f'written: {idx}_{r}')


def _login_facebook(driver):
    driver.get("http://www.facebook.com")

    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))


    username.clear()
    username.send_keys(USERNAME)
    password.clear()
    password.send_keys(KEY)

    # log in
    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # wait 5 seconds to allow your new page to load
    time.sleep(5)


def single_keyword_search(driver, keyword):
    driver = set_up_chrome_driver()
    keyword = keyword.lower().replace(" ", '%20')

    driver.get("http://www.facebook.com/search/posts?q={}{}".format(keyword, FB_RECENT_TOGGLE))
    time.sleep(2)

    now = driver.current_url

    mobile = now[:8] + "m." + now[12:]
    driver.get(mobile)

    count = 0
    switch = True
    height = 0

    while switch:
        count += 1

        openSeeMore(driver)

        dates = [el.text for el in
                 driver.find_elements(By.XPATH, '//div[@class="_52jc _5qc4 _78cz _24u0 _36xo"]/a[@class="_26yo"]')]
        links_l = [el.get_attribute('href') for el in
                   driver.find_elements(By.XPATH, '//div[@class="_52jc _5qc4 _78cz _24u0 _36xo"]/a[@class="_26yo"]')]
        # texts = [el.text for el in driver.find_elements(By.XPATH,
        #                                                 '//div[@class="_5rgr _5gh8 _3-hy async_like"]/div[@class="story_body_container"]/div/div/span/span[@data-sigil="more"]')]
        names = [el.text for el in driver.find_elements(By.XPATH, '//div[@class="_4g34"]/h3')]

        actualPosts = driver.find_elements(By.XPATH,
                                           '//div[@class="story_body_container"]/div[@class="_5rgt _5nk5 _5msi"]')
        texts = []
        if actualPosts:
            for posts in actualPosts:
                text = ""
                ActionChains(driver).move_to_element(posts).perform()
                paragraphs = posts.text
                text += paragraphs
                texts.append(text)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        if height == driver.execute_script("return document.body.scrollHeight"):
            switch = False
        else:
            height = driver.execute_script("return document.body.scrollHeight")

    for i in range(len(names)):
        # make prediction here predicted = ''
        single_write_to_db(dates[i], text[i], names[i], 'facebook', links_l[i])


def main():
    pass

if __name__ == '__main__':
    main()
