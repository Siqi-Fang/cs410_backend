import pandas as pd
import csv
from os import listdir
from os.path import isfile, join
import sqlite3
from app.db import get_db
from app.constants import FIELDS

DB = 'data/database.db'
TABLE = 'POSTS'


def single_write_to_db(post_date, content, author, platform, url, keyword):
    """Write a single row to database"""
    post_date = post_date
    content = content
    author = author
    platform = platform
    url = url
    keyword = keyword

    conn = get_db()
    conn.execute('INSERT INTO posts (post_date, content, author, platform, url, keyword) VALUES (?,?, ?, ?, ?, ?)',
                 (post_date, content, author, platform, url, keyword))
    conn.commit()


def test_db_setup():
    df = pd.read_csv('data/test_data.csv')
    df['platform'] = 'facebook'
    print(df.shape)

    connection = sqlite3.connect('data/test.db')
    df.to_sql(name="TEST", con=connection, if_exists='append')


def form_field_to_sql_command(platform: str, keywords: str, start_date: str, end_date: str) -> str:
    """
    Return the string sql command that query for the given kwargs.
    If dates are left blank then we don't filter for dates,
    """
    where_statements = []

    keywords = ["\'" + keyword + "\'" for keyword in keywords]
    where_statements.append('keyword in ({})'.format(",".join(keywords)))
    where_statements.append('platform == \'{}\''.format(platform))
    if start_date != '' and end_date == '':
        where_statements.append('post_date > datetime(\'{}\')'.format(start_date))
    elif start_date == '' and end_date != '':
        where_statements.append('post_date < datetime(\'{}\')'.format(end_date))
    elif start_date != '' and end_date != '':
        where_statements.append('post_date between datetime(\'{}\') and datetime(\'{}\')'.format(
                                                        start_date, end_date))

    return 'SELECT ' + ", ".join(FIELDS) + ' FROM ' + TABLE + ' WHERE ' + \
           " and ".join(where_statements)


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
            with open("app/static/result.csv", "w") as csv_file:
                csv_writer = csv.writer(csv_file, delimiter="\t")
                csv_writer.writerow(FIELDS)
                csv_writer.writerows(records)
            return len(records)
    except:
        return -1


if __name__ == '__main__':
    update_csv_from_cmd("SELECT POST_DATE, AUTHOR, CONTENT, PLATFORM, URL, KEYWORD FROM TEST WHERE keyword in (\'Illegal alien Latino\') and platform == \'facebook\'")