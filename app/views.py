from flask import Blueprint, request, render_template, url_for
from datetime import datetime
from app.utils import form_field_to_sql_command, update_csv_from_cmd
from app.truth_scraper import query_single_truth
from app.twitter_scraper import query_single_tweet
from app.constants import Platform, FIELDS

bp = Blueprint('app', __name__, template_folder='/templates', static_folder='/static')

@bp.route('/')
def home():
    return render_template('main.html')


@bp.route('/render_search/')
def render_search():
    return render_template('search.html')


@bp.route('/render_scrape/')
def render_scrape():
    return render_template('scrape.html')


@bp.route('/gen_scrape_request/', methods=['POST', 'GET'])
def gen_scrape_request():

    if request.method == 'POST':
        # all the fields needs to be required
        platform = request.form['social-media']  # will return the value field
        platform = Platform.from_str(platform)
        user_login = request.form['username']
        user_key = request.form['password']
        search_terms = request.form.getlist('terms')

        print(platform, user_login, user_key, search_terms)

        for term in search_terms:
            perform_new_query(platform, term)

        return render_template('scrape.html')


@bp.route('/retrieve_posts/', methods=['POST', 'GET'])
def retrieve_posts():

    if request.method == 'POST':
        # all the fields needs to be required
        platform = request.form['social-media']  # will return the value field
        search_terms = request.form.getlist('terms')
        start_date = request.form['start-search']
        end_date = request.form['end-search']
        sql_cmd = form_field_to_sql_command(platform=platform, keywords=search_terms,
                                            start_date=start_date, end_date=end_date)
        print(sql_cmd)
        update_status = update_csv_from_cmd(sql_cmd)
        if update_status > 0: # download ready
            link_to_download = '<a href = {} download> Click Here to download {} entries found </a>'.format(
                url_for('static', filename='result.csv'), update_status)
        elif update_status == 0:
        # TODO Message
            link_to_download = "No result matching your search exists in our database"
        else:
            link_to_download = 'Connection Failed, Please Retry'

        return render_template('search.html', link_to_download=link_to_download)


# def retrieve_post(post_id):
#     conn = get_db_connection()
#     post = conn.execute('SELECT * FROM posts WHERE id = ?',
#                         (post_id,)).fetchone()
#     conn.close()
#     if post is None:
#         FileNotFoundError("No Post Found")
#     return post


# @bp.route("/request_test", methods=['POST'])
# def save_post():
#     """Save Post to database from POST request"""
#     if request.method == 'POST':
#         post_date = request.form.get('post_date')
#         content = request.form.get('content')
#         author = request.form.get('author')
#         platform = request.form.get('platform')
#         url = request.form.get('url')
#         keyword = request.form.get('keyword')
#
#         single_write_to_db(post_date, content, author, platform, url, keyword)
#     return


def perform_new_query(platform, term):
    if platform == Platform.TRUTHSOCIAL:
        query_single_truth(term)
    elif platform == Platform.TWITTER:
        query_single_tweet(term)
    elif platform == Platform.FACEBOOK:
        raise NotImplementedError


# if __name__ == '__main__':
#     app.run()
