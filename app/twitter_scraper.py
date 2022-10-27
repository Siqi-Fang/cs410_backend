import snscrape.modules.twitter as sntwitter
from app.utils import single_write_to_db
from sqlite3 import IntegrityError



def query_single_tweet(slur):
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
    pass


if __name__ == '__main__':
    main()