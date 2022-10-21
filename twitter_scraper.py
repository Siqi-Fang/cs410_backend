import snscrape.modules.twitter as sntwitter
from utils import single_write_to_db
from sqlite3 import IntegrityError
"""
(post_date, content, author, platform, url, term)
"""


def get_tweets_with_slur(slur):
    query = slur + " since:2020-10-16"
    items = sntwitter.TwitterSearchScraper(query).get_items()
    for tweet in items:
        for word in slur:
            if word.lower() not in tweet.content.lower():
                continue
        tweet_url = "https://twitter.com/" + tweet.user.username + "/status/" + str(tweet.id)
        try:
            single_write_to_db(tweet.date, tweet.content, tweet.user.username, 'Twitter', tweet_url, slur)
        except IntegrityError:
            print("Reached visited post, search stopped")
            break

def main():
    #slurs = ["Illegal alien Latino", "Illegal immigrant Latino", "Latino Wetback", "Latino Spic", "Latino Undocumented", "Latino Beaner", "Latino Rapists", "Latino Drug dealers", "Latino Invasion"]
    term = 'Latino Invasion'
    get_tweets_with_slur(term)
    print('==========Query for {} finished============'.format(term))


if __name__ == '__main__':
    main()