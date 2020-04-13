import requests
from bs4 import BeautifulSoup
import pprint

res = requests.get('https://news.ycombinator.com/news')
res2 = requests.get('https://news.ycombinator.com/news?p=2')
soup = BeautifulSoup(res.text, 'html.parser')
soup2 = BeautifulSoup(res2.text, 'html.parser')

links = soup.select('.storylink')
subtext = soup.select('.subtext')
links2 = soup2.select('.storylink')
subtext2 = soup2.select('.subtext')

top60_links = links + links2
top60_subtext = subtext + subtext2


def sort_stories_by_votes(hackerlist):
    return sorted(hackerlist, key=lambda k: k['votes'], reverse=True)


def create_custom_hacker_news_list(links, subtext):
    hacker_news_list = []

    # using enumerate as we need the index for [subtext] also and not only for [links]
    for index, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        vote = subtext[index].select('.score')
        if len(vote): # if vote exists
            points = int(vote[0].getText().replace(' points', ''))
            if points > 99:
                hacker_news_list.append({'title': title, 'link': href, 'votes': points})
    return sort_stories_by_votes(hacker_news_list)


pprint.pprint(create_custom_hacker_news_list(top60_links, top60_subtext))