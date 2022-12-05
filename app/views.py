from flask import Blueprint, request, render_template, url_for
from app.utils import form_field_to_sql_command, update_csv_from_cmd
from app.constants import Platform, FIELDS

from app.truth_scraper import query_single_truth
from app.gateway import query_single_post
from app.twitter_scraper import query_single_tweet




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
            perform_new_query(platform, term, user_login, user_key)

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
            link_to_download = "No result matching your search exists in our database"
        else:
            link_to_download = 'Connection Failed, Please Retry'

        return render_template('search.html', link_to_download=link_to_download)


def perform_new_query(platform, term, user_login, user_key):
    if platform == Platform.TRUTHSOCIAL:
        query_single_truth(term, user_key, user_login)
    elif platform == Platform.TWITTER:
        query_single_tweet(term)
    elif platform == Platform.GATEWAYPUNDIT:
        query_single_post(term)
    elif platform == Platform.FACEBOOK:
        raise NotImplementedError



