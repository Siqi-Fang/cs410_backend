"""
Lucy Zhang
Senior Seminar Project
Twitter Scraping
"""
import sys
import time
from bs4 import BeautifulSoup
import requests
import re
from datetime import datetime
from app.utils import single_write_to_db


def main():
    query_single_post('latino rapists')


def query_single_post(slur):
    # https://www.thegatewaypundit.com/?s=hispanic+immigrants
    slur = slur.lower()
    pattern = re.compile('https:\/\/www\.thegatewaypundit\.com\/\d+\/\d+\/.*')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.0 Safari/537.36'
    }

    all_links = []
    slur_str = "+".join(slur.split(' '))
    url = "https://www.thegatewaypundit.com/page/1/?s=" + slur_str

    try:
        page = requests.get(url, headers=headers)
    except Exception as e:
        print("error type:", sys.exc_info()[0])

    time.sleep(2)
    soup = BeautifulSoup(page.content, 'html.parser')
    pages = soup.find_all("div", {"class": "next-page-num nav-style"})
    num_pages = 0

    for page in pages:
        if (page.find("a")) is not None:
            num_pages = max(num_pages, int((page.find("a")).text))

    for n in range(1, num_pages):
        url = "https://www.thegatewaypundit.com/page/" + str(n) + "/?s=" + slur_str
        try:
            page = requests.get(url, headers=headers)
        except Exception as e:
            print("error type:", sys.exc_info()[0])
        time.sleep(2)
        soup = BeautifulSoup(page.content, 'html.parser')
        for link in soup.find_all('a'):
            all_links.append(link.get('href'))

        for link in set(all_links):
            if pattern.match(str(link)) and "#disqus_thread" not in str(link):
                page = requests.get(link, headers=headers)
                time.sleep(2)
                soup = BeautifulSoup(page.text, 'html.parser')
                paragraph_text = ""
                entry_info = str(soup.findAll('div', attrs={'class': 'entry-meta-text'})[0])
                author = soup.findAll('div', attrs={'class': 'entry-meta-text'})[0].find("a").text
                idx = entry_info.find("Published")
                date_raw = " ".join(entry_info[idx:].split(" ")[1:4])
                date = datetime.strptime(date_raw, '%B %d, %Y')

                for paragraph in soup.find_all('p'):
                    paragraph_text += paragraph.get_text().lower()

                slurs_used = True
                for s in slur.split(" "):
                    if s.lower() not in paragraph_text:
                        slurs_used = False
                if not slurs_used:
                    continue
                single_write_to_db(date, "", author, "gateway-pundit", link, slur)


if __name__ == "__main__":
    main()
