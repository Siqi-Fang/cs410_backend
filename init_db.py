import sqlite3
from sqlite3 import IntegrityError

connection = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor() # cursor object allows creating rows

# try:
#     cur.execute("INSERT INTO TEST (post_date, created_date, content, author, platform, url, keyword) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                 ('1-1-1111', '1-2-1111', 'Content Placeholder', 'Author', 'Facebook', 'www.notreal.com', 'bo')
#                 )
#
#     cur.execute("INSERT INTO TEST (post_date, created_date, content, author, platform, url, keyword) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                 ('1-1-1111', '1-3-1111', 'Content Placeholder', 'Author', 'Facebook', 'www.notreal.com', 'bo')
#                 )
#     cur.execute("INSERT INTO TEST (post_date, created_date, content, author, platform, url, keyword) VALUES (?, ?, ?, ?, ?, ?, ?)",
#                 ('1-1-1111', '1-4-1111', 'Content Placeholder', 'Author', 'Facebook', 'www.notreal.com', 'bo')
#                 )
# except IntegrityError:
#     print('bye')
connection.commit()
connection.close()