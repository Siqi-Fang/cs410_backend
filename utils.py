import pandas as pd
from os import listdir
from os.path import isfile, join
import sqlite3


def get_db_connection(db='database.db'):
    """Return Database row factory object use it with execute()
    Optional parameter: database name
    """
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    return conn


def single_write_to_db(post_date, content, author, platform, url, keyword):
    """Write a single row to database"""
    post_date = post_date
    content = content
    author = author
    platform = platform
    url = url
    keyword = keyword

    conn = get_db_connection()
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

if __name__ == '__main__':
    test_db_setup()