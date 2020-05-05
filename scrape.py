import requests
from bs4 import BeautifulSoup

res = requests.get('https://news.ycombinator.com/')
soup = BeautifulSoup(res.text, 'html.parser')
links = soup.select('.storylink')
subtext = soup.select('.subtext')

all_links = []
all_subtext = []

for i in range(1, 4):
    url = 'https://news.ycombinator.com/?p=' + str(i)
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    links = soup.select('.storylink')
    subtext = soup.select('.subtext')
    all_links += links
    all_subtext += subtext


def sort_by_votes(stories):
    return sorted(stories, key=lambda k: k['votes'], reverse=True)


def top_hn(links, subtext):
    news = []
    for idx, item in enumerate(links):
        title = item.getText()
        href = item.get('href', None)
        votes = subtext[idx].select('.score')

        if (len(votes)):
            points = int(votes[0].getText().replace(' points', ''))
            if points > 99:
                news.append({
                    'title': title,
                    'link': href,
                    'votes': points
                })
    return sort_by_votes(news)


total_news = top_hn(all_links, all_subtext)
print(total_news)
print('Total news =', len(total_news))
