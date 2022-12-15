from urllib.parse import parse_qs

from bayes import NaiveBayesClassifier
from bottle import redirect, request, route, run, template
from db import News, session
from scraputils import get_news


@route("/")
def root():
    redirect("/news")


@route("/news")
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template("news_template", rows=rows)


@route("/add_label/")
def add_label():
    args = parse_qs(request.query_string)
    s = session()
    s.query(News).filter(News.id == int(args["id"][0])).update({"label": str(args["label"][0])}
    )
    s.commit()
    redirect("/news")


@route("/update")
def update_news():
    s = session()
    news = get_news("https://news.ycombinator.com/newest")
    for new in news:
        isin = len(
            s.query(News).filter(News.author == new["author"], News.title == new["title"]).all())
        if not isin:
            s.add(
                News(
                    title=new["title"],
                    author=new["author"],
                    points=new["points"],
                    comments=new["comments"],
                    url=new["url"],
                )
            )
    s.commit()
    redirect("/news")


@route("/classify")
def classify_news():
    redirect("/recommendations")


@route("/recommendations")
def recommendations():
    s = session()
    labeled = s.query(News).filter(News.label != None).all()
    titles_known = []
    labels_known = []
    for new in labeled:
        titles_known.append(new.title)
        labels_known.append(new.label)
    model = NaiveBayesClassifier(1)
    model.fit(titles_known, labels_known)

    not_labeled = s.query(News).filter(News.label == None).all()
    titles = []
    for new in not_labeled:
        titles.append(new.title)
    labels = model.predict(titles)

    classified_news = []
    for label in ("good", "maybe", "never"):
        ind = 0
        for title_label in labels:
            if title_label == label:
                classified_news.append(not_labeled[ind])
            ind += 1
    return template("news_template", rows=classified_news)


if __name__ == "__main__":
    run(host="localhost", port=8080)
