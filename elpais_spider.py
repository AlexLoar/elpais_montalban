# Pasatiempo de un viaje en bus

import json

import requests
from bs4 import BeautifulSoup

URL = 'https://elpais.com/autor/manuel_vazquez_montalban/a/'


def process_page(url):
    response = requests.get(url)
    page = BeautifulSoup(response.text, "html.parser")

    next_page = get_next_page(page)
    articles_links = get_articles(page)

    return articles_links, next_page


def get_next_page(page):
    try:
        next_page = page.find('li', {'class': 'paginacion-siguiente'}).a['href']
    except AttributeError:
        # Last page
        return None
    return next_page


def get_articles(page):
    articles = page.find_all('div', {'class': 'articulo__interior'})
    articles_links = list()
    for article in articles:
        link = 'https:{}'.format(article.h2.a['href'])
        articles_links.append(link)

    return articles_links


def get_article_info(article_link):
    article_page = requests.get(article_link)
    article = BeautifulSoup(article_page.text, "html.parser")

    title = article.find(id='articulo-titulo').text
    date = article.find('time', {'class': 'articulo-actualizado'})['datetime']
    content = article.find(id='cuerpo_noticia').text
    tags = [tag.text for tag in article.find_all('li', {'itemprop': 'keywords'})]

    return {'link': article_link, 'title': title, 'date': date, 'content': content, 'tags': tags}


def order_articles_by_reverse_date(articles):
    return articles.sort(key=lambda article: article['date'])


if __name__ == "__main__":
    next_page = URL

    article_list = list()
    while next_page:
        art_links, next_page = process_page(next_page)
        for article_link in art_links:
            article_list.append(get_article_info(article_link))

    ordered_articles = order_articles_by_reverse_date(article_list)

    with open("elpais_mvm.json", "w") as file:
        json.dump(ordered_articles, file)
