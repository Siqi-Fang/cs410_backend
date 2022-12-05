import csv
import sqlite3
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from app.db import get_db
from app.constants import FIELDS
from decouple import config
import eng_spacysentiment
nlp = eng_spacysentiment.load()

DB = config('DB')
CHROMEDRIVER_PATH = config('CHROMEDRIVER_PATH')
TABLE ='POSTS'
SPREADSHEET = config('SPREEDSHEET_PATH')




def single_write_to_db(post_date, content, author, platform, url, keyword):
    """Write a single row to database"""
    # sentiment analysis
    result = nlp(content).cats
    sentiment = 'positive' if result['positive'] > 0.5 else 'negative'
    score = result[sentiment] * 100

    conn = get_db()
    conn.execute('INSERT INTO POSTS (post_date, content, author, platform, url, keyword, sentiment, score) '
                 'VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                 (post_date, content, author, platform, url, keyword, sentiment, score))
    conn.commit()


def form_field_to_sql_command(platform: str, keywords: list, start_date: str, end_date: str) -> str:
    """
    Return the string sql command that query for the given kwargs.
    If dates are left blank then we don't filter for dates,
    """
    where_statements = []
    keywords = ["\'" + keyword + "\'" for keyword in keywords]
    where_statements.append('keyword in ({})'.format(",".join(keywords)))
    where_statements.append('platform = \'{}\''.format(platform))
    if start_date != '' and end_date == '':
        where_statements.append('post_date > datetime(\'{}\')'.format(start_date))
    elif start_date == '' and end_date != '':
        where_statements.append('post_date < datetime(\'{}\')'.format(end_date))
    elif start_date != '' and end_date != '':
        where_statements.append('post_date between datetime(\'{}\') and datetime(\'{}\')'.format(
                                                        start_date, end_date))

    return 'SELECT ' + ", ".join(FIELDS) + ' FROM ' + TABLE + ' WHERE ' + \
           " and ".join(where_statements) + 'ORDER BY sentiment, score  DESC'
           # sort by sentiment asc gives negative first


def update_csv_from_cmd(sql_cmd: str) -> int:
    """
    Update the static/result.csv file with the sql query result
    :param sql_cmd:
    :return: int: - 0 if NO DATA, -1 if ERROR, len(data) retrieved -> SUCCESS
    """
    conn = sqlite3.connect(DB)
    records = conn.execute(sql_cmd).fetchall()

    try:
        if len(records) == 0:  # no data retrieved
            return 0
        else:
            with open(SPREADSHEET, "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter=",")
                csv_writer.writerow(FIELDS)
                csv_writer.writerows(records)
            return len(records)
    except:
        return -1


def set_up_chrome_driver():
    """Returns a chrome driver that runs in headless mode(no window shows up)"""

    WINDOW_SIZE = "1920,1080"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % WINDOW_SIZE)

    driver = webdriver.Chrome(executable_path=CHROMEDRIVER_PATH,
                              options=chrome_options)

    return driver

