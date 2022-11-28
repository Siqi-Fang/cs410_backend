from facebook_scraper import get_posts

for post in get_posts('Illegal alien Latino', pages=1):
    print(post['text'][:50])