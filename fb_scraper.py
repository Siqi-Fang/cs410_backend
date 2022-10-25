# import
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains

from selenium.common.exceptions import ElementNotInteractableException

from bs4 import BeautifulSoup as bs

from decouple import config
USERNAME = config('USERNAME')
KEY = config('KEY')

import time


def openSeeMore(browser):
    readMore = browser.find_elements(By.XPATH, "//div[text()='See more']")
    if len(readMore) > 0:    
        count = 0
        for i in readMore:
            action=ActionChains(browser)
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
        print('redirected!!!')
        browser.back()
        print('got back!!!')


def archiveAtEnd(browser, reviewList):
    browser.execute_script("window.scrollTo(0, -document.body.scrollHeight);") # scroll back to the top
    time.sleep(10)
        
    for idx, l in enumerate(reviewList):
        if idx % 10 == 0:
            if idx < 15:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[0])
            else:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx-15])
            
            time.sleep(1)
            try:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx+15])
            except:
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[-1])

            time.sleep(1)
            browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx])
            
            for r in range(2):
                time.sleep(3)
                try:
                    browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx+5])
                    time.sleep(3)
                except:
                    browser.execute_script("arguments[0].scrollIntoView();", reviewList[-1])
                browser.execute_script("arguments[0].scrollIntoView();", reviewList[idx+r*3])
                time.sleep(3)
                with open(f'./PATH/{str(idx)}_{r}.html',"w", encoding="utf-8") as file:
                    source_data = browser.page_source
                    bs_data = bs(source_data, 'html.parser')
                    file.write(str(bs_data.prettify()))
                    print(f'written: {idx}_{r}')


def _login_to_truth(driver, my_username, my_password):
    username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='email']")))
    password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='pass']")))

    username.clear()
    username.send_keys(my_username)
    password.clear()
    password.send_keys(my_password)

    button = WebDriverWait(driver, 2).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

    # wait 5 seconds to allow your new page to load
    time.sleep(5)


def facebook_query(driver, keyword):
    k_word = keyword.split(" ")
    for word in k_word:
        word = word.lower()

    driver.get("http://www.facebook.com")
    try: #Fine
        search = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[aria-label='Search Facebook']")))
        search.send_keys(keyword)
        search.send_keys(Keys.RETURN)
    except ElementNotInteractableException:
        print('Not able to locate search Bar')
        driver.quit()
    try: #TODO
        driver.find_element(By.XPATH, '/html/body/div[1]/div[1]/div[1]/div/div[3]/div/div/div/div[1]/div[1]/div[1]/div/div[2]/div[1]/div[2]/div/div/div[2]/div/div[2]/div/a/div[1]/div[2]/div/div/div/div/span').click()
    except:
        print('locating posts field failed')
        driver.quit()
    driver.find_element(By.XPATH, '//div[@class="x1rg5ohu xw3qccf xsgj6o6"]').click()
    time.sleep(1)
    driver.find_element(By.XPATH, '//div[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou xe8uvvx x1hl2dhg xggy1nq x1o1ewxj x3x9cwd x1e5q0jg x13rtm0m x87ps6o x1lku1pv x1a2a7pz x6s0dn4 xjyslct x9f619 x1ypdohk x78zum5 x1q0g3np x2lah0s x1w4qvff x13mpval xdj266r xat24cr xz9dl7a x1sxyh0 xsag5q8 xurb0ha x1n2onr6 x16tdsg8 x1ja2u2z"][3]/div/div').click()

    now = driver.current_url
    print("now", now)

    mobile = now[:8] + "m." + now[12:]
    print("mobv", mobile)
    driver.get(mobile)

    count = 0
    switch = True
    old_numReviews = 0
    specifiedNumber = 8 # number of reviews to get
    url = []
    height = 0

    while switch:
        count += 1
        result = []
        dates = []

        dates = [el.text for el in driver.find_elements(By.XPATH, '//div[@class="_52jc _5qc4 _78cz _24u0 _36xo"]/a[@class="_26yo"]')]
        links_l = [el.get_attribute('href') for el in driver.find_elements(By.XPATH, '//div[@class="_52jc _5qc4 _78cz _24u0 _36xo"]/a[@class="_26yo"]')]
        texts = [el.text for el in driver.find_elements(By.XPATH, '//div[@class="_5rgr _5gh8 _3-hy async_like"]/div[@class="story_body_container"]/div/div/span/span[@data-sigil="more"]')]
        names = [el.text for el in driver.find_elements(By.XPATH, '//div[@class="_4g34"]/h3')]

        actualPosts = driver.find_elements(By.XPATH, '//div[@class="story_body_container"]/div[@class="_5rgt _5nk5 _5msi"]')
        texts = []
        if actualPosts:
            for posts in actualPosts:
                text = ""
                ActionChains(driver).move_to_element(posts).perform()
                paragraphs = posts.text
                text += paragraphs
                texts.append(text)

        # scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

        if height == driver.execute_script("return document.body.scrollHeight"):
            switch = False
        else:
            height = driver.execute_script("return document.body.scrollHeight")

    org = len(texts)
    for text in texts:
        pos = text
        pos1 = pos.lower()
        for j in range(len(k_word)-1):
            if k_word[j] not in pos1:
                i = texts.index(text)
                texts.pop(i)
                links_l.pop(i)
                names.pop(i)
                dates.pop(i)
                break
        if text in texts:
            i = texts.index(text)
            texts[i] = texts[i]
            print(texts[i][:30])

    platform = ["Facebook"] * len(dates)
    result = zip(platform, names, dates, texts, links_l)

    return result

    time.sleep(5)


def main():
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications": 2}
    chrome_options.add_experimental_option("prefs", prefs)

    keyword = 'illegal immigrant'
    driver = webdriver.Chrome('/Users/apple/Downloads/chromedriver', options=chrome_options)
    keywords = [keyword]
    driver.get("http://www.facebook.com")

    _login_to_truth(driver, USERNAME, KEY)
    for keyword in keywords:
        facebook_query(driver, keyword)


if __name__ == '__main__':
    main()