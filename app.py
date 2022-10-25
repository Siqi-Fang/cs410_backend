from flask import Flask, request
from datetime import datetime
from utils import single_write_to_db, get_db_connection
from truth_scraper import query_single_truth
from twitter_scraper import query_single_tweet
from constants import Platform, FILEDS

app = Flask(__name__)


def retrieve_post(post_id):
    conn = get_db_connection()
    post = conn.execute('SELECT * FROM posts WHERE id = ?',
                        (post_id,)).fetchone()
    conn.close()
    if post is None:
        FileNotFoundError("No Post Found")
    return post


@app.route("/request_test", methods=['POST'])
def save_post():
    """Save Post to database from POST request"""
    if request.method == 'POST':
        post_date = request.form.get('post_date')
        content = request.form.get('content')
        author = request.form.get('author')
        platform = request.form.get('platform')
        url = request.form.get('url')
        keyword = request.form.get('keyword')

        single_write_to_db(post_date, content, author, platform, url, keyword)
    return


def perform_new_query(platform, term):
    if platform == Platform.TRUTHSOCIAL:
        query_single_truth(term)
    elif platform == Platform.TWITTER:
        query_single_tweet(term)
    elif platform == Platform.FACEBOOK:
        raise NotImplementedError


if __name__ == '__main__':
    app.run()
