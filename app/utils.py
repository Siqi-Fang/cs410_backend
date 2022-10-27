import pandas as pd
import csv
from os import listdir
from os.path import isfile, join
import sqlite3
from decouple import config
from app.db import get_db
from flask import g, url_for, current_app
from app.constants import FIELDS

DB = config('DB')
TABLE = 'TEST'

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
    conn.close()


def create_table_from_files(folder):
    """For demo purpose only"""
    filenames = [f for f in listdir(folder) if isfile(join(folder, f))]
    header = ['keyword', 'author', 'post_date', 'content', 'url']
    df = pd.DataFrame(columns=header)
    for filename in filenames:
        if filename[0] != '.':
            temp = pd.read_excel(folder+'/'+filename, engine='openpyxl', names=header, header=None, index_col=None)
            temp.drop(axis=0, index=[0], inplace=True)
            df = pd.concat([df, temp])
    print(df.shape)
    df['platform'] = 'facebook'

    return df


def df_to_db(data, db, tablename='POSTS'):
    connection = sqlite3.connect(db)
    try:
        data.to_sql(name=tablename, con=connection, if_exists='append')
    except Exception as e:
        print('Error Reading df')
        print(e.message)


def test_db_setup():
    df = pd.read_csv('data/test_data.csv')
    df['platform'] = 'facebook'
    print(df.shape)

    connection = sqlite3.connect('data/test.db')
    df.to_sql(name="TEST", con=connection, if_exists='append')


def form_field_to_sql_command(platform: str, keywords: str) -> str:
    """
    Return the string sql command that query for the given kwargs.
        Support Platform and Keywords currently
    """
    where_statements = []

    keywords = ["\'" + keyword + "\'" for keyword in keywords]
    where_statements.append('keyword in ({})'.format(",".join(keywords)))
    where_statements.append('platform == \'{}\''.format(platform))

    return 'SELECT ' + ", ".join(FIELDS) + ' FROM ' + TABLE + ' WHERE ' + \
           " and ".join(where_statements)


def update_csv_from_cmd(sql_cmd: str) -> int:
    """
    Update the static/result.csv file with the sql query result
    :param sql_cmd:
    :return: int: - 0 if NO DATA, -1 if ERROR, len(data) retrieved -> SUCCESS
    """
    conn = sqlite3.connect(DB)
    # try:
    records = conn.execute(sql_cmd).fetchall()

    try:
        if len(records) == 0: # no data retrieved
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