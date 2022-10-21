from time import sleep
from decouple import config
from datetime import datetime

from selenium.webdriver.common.keys import Keys
from selenium.common import exceptions
from selenium import webdriver

from sqlite3 import IntegrityError

from app import single_write_to_db


USERNAME = config('USERNAME')
KEY = config('KEY')


def get_truth_data(card):
    """
    Extract the field (user_id, user, postdate, post_text, link) from a html post element
    NOTE:
        StaleElement can happen if there is a new post being made b/w when you retrive the collection of posts
        and when you run this function, solution is to re-retrieve the posts i think
        :param card:Object
        :return: post_date, content, author, 'Truth Social', url
    """
    try:  # many ways to grab this
        user_id = card.find_element("xpath", 'div/div/div[1]/div/div/div[1]/div/div/div/p').text
    except exceptions.NoSuchElementException:
        user_id = ""
    except exceptions.StaleElementReferenceException:
        return
    try:
        author = card.find_element('xpath', 'div/div/div[1]/div/div/div[1]/div/span/a/div/p').text
    except exceptions.NoSuchElementException:
        author = ""
    except exceptions.StaleElementReferenceException:
        return

    try:
        post_date = card.find_element('xpath', './/time').get_attribute('title')
        post_date = datetime.strptime(post_date, '%b %d, %Y, %H:%M')
    except exceptions.NoSuchElementException:
        return
    except ValueError: # truth social has weird time sometimes
        print('Invalid Timestamp detected')
        return

    try:
        body = card.find_element('xpath', './/div[@class="status__content-wrapper"]')
        content = body.find_element('tag name', 'p').text
    except exceptions.NoSuchElementException:
        content = ""

    try:
        post_id = card.find_element('xpath', "div/div").get_attribute('data-id')
        url = "https://truthsocial.com/{username}/posts/{id}".format(username=user_id, id=post_id)
    except exceptions.NoSuchElementException:
        url = 'N/A'

    data = (post_date, content, author, 'Truth Social', url)

    return data


def collect_from_current_view(driver, lookback_limit=25):
    """
    The page is continuously loaded, so as you scroll down the number of tweets returned by this function will
     continue to grow. To limit the risk of 're-processing' the same tweet over and over again, you can set the
     `lookback_limit` to only process the last `x` number of tweets extracted from the page in each iteration.
     You may need to play around with this number to get something that works for you. I've set the default
     based on my computer settings and internet speed, etc...
     """
    page_cards = driver.find_elements('xpath', '//div[@data-testid="status"]')
    if len(page_cards) <= lookback_limit:
        return page_cards
    else:
        return page_cards[-lookback_limit:]


def scroll_down_page(driver, last_position, num_seconds_to_load=2, scroll_attempt=0, max_attempts=5):
    """
    The function will try to scroll down the page and will check the current
    and last positions as an indicator. If the current and last positions are the same after `max_attempts`
    the assumption is that the end of the scroll region has been reached and the `end_of_scroll_region`
    flag will be returned as `True`
    """
    end_of_scroll_region = False
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(num_seconds_to_load)
    curr_position = driver.execute_script("return window.pageYOffset;")
    if curr_position == last_position:
        if scroll_attempt < max_attempts:
            end_of_scroll_region = True
        else:
            scroll_down_page(last_position, curr_position, scroll_attempt + 1)
    last_position = curr_position
    return last_position, end_of_scroll_region


def driver_clear(element):
    """Clear the text field of input element"""
    while element.get_attribute('value') != '':
        element.send_keys(Keys.BACKSPACE)


def truth_search(driver, term, query):
    """
    Go to search bar and get you to the page to begin scrapping

    :param driver: chrome driver object
    :param term: search keyword
    :type term: str
    :param query: 'USER' or 'KEYWORD'
    :type query: str
    """
    # maybe use enum for query param
    search_term = term
    search_input = driver.find_element("xpath", '//input[@id="search"]')
    driver_clear(search_input)
    search_input.send_keys(search_term)
    search_input.send_keys(Keys.RETURN)
    sleep(1)

    if query == 'USER':
        driver.find_element("xpath", '//a[@title="' + term + '"]').click()  # opens the person's profile page
    elif query == "KEYWORD":  # get to post page
        tab = driver.find_element("xpath", '//div[@role="tablist"]')
        element = tab.find_element("xpath", '//button[2]/div')
        driver.execute_script("arguments[0].click();", element)

    else:
        raise ValueError("Invalid query type for truth social, must be by Username or by Keyword")
    driver.execute_script("document.body.style.zoom='50%'")


def _login_to_truth(driver, my_username, my_password):
    # fills the login page with credentials u provided
    username = driver.find_element("xpath", '//input[@name="username"]')
    username.clear()
    username.send_keys(my_username)
    username.send_keys(Keys.RETURN)
    sleep(0.5)

    password = driver.find_element("xpath", '//input[@name="password"]')
    password.clear()
    password.send_keys(my_password)
    password.send_keys(Keys.RETURN)
    sleep(0.5)


def query_single(term, query="KEYWORD"):
    #options = webdriver.ChromeOptions()
    #options.add_argument("headless") # hides the window
    driver = webdriver.Chrome('/Users/apple/Downloads/chromedriver')
    driver.get('https://truthsocial.com/login')
    driver.maximize_window()
    sleep(2)

    _login_to_truth(driver, USERNAME, KEY)
    sleep(2)

    truth_search(driver, term, query)

    last_position = None
    end_of_scroll_region = False

    while not end_of_scroll_region:
        cards = collect_from_current_view(driver)
        for card in cards:
            try:
                post = get_truth_data(card)
            except exceptions.StaleElementReferenceException:
                continue
            if not post:
                continue
            post_date, content, author, platform, url = get_truth_data(card)
            try:
                single_write_to_db(post_date, content, author, platform, url, term)
            except IntegrityError:
                print("Reached visited post, search stopped")
                break
        last_position, end_of_scroll_region = scroll_down_page(driver, last_position)

    driver.quit()


def main():
    my_terms = ["Illegal alien Latino", "Illegal immigrant Latino", "Latino Wetback", "Latino Spic",
                "Latino Undocumented", "Latino Beaner", "Latino Rapists", "Latino Drug dealers", "Latino Invasion"]

    for term in my_terms:
        query_single(term)


if __name__ == '__main__':
    main()
