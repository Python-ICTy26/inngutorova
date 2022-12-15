import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    news_list = []
    titles = parser.table.findAll("span", {"class": "titleline"})
    sublines = parser.findAll("td", {"class": "subtext"})

    for i in range(len(titles)):
        titleline = titles[i]
        subline = sublines[i]
        title = titleline.find("a").text
        author = subline.find("a", {"class": "hnuser"}).text
        url = titleline.find("a")["href"]
        if subline.findAll("a")[-1].text == "discuss":
            comments = 0
        else:
            line = subline.findAll("a")[-1].text
            comments = int(line.split()[0])
        points = subline.find("span", {"class": "score"}).text
        news_list.append(
            {
                "title": title,
                "author": author,
                "url": url,
                "comments": comments,
                "points": points,
            }
        )

    return news_list


def extract_next_page(parser):
    next_page = parser.find("a", {"class": "morelink"})["href"]
    print(next_page)
    return next_page


def get_news(url, n_pages=1):
    """Collect news from a given web page"""
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news
