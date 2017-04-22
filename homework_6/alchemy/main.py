import asyncio
from aiohttp import ClientSession
from lxml import etree
import re
import psycopg2
from sqlalchemy.orm import sessionmaker
from alchemy.model import Base, Posts
from sqlalchemy import create_engine


# conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='2367'")
# cur = conn.cursor()


async def fetch(url, session):
    async with session.get(url) as response:
        return await response.text()


async def get_pages(r):
    tasks = []

    async with ClientSession() as session:
        for item in range(r):
            task = asyncio.ensure_future(fetch(url.format(item * 40), session))
            tasks.append(task)
        return await asyncio.gather(*tasks)


async def get_topics(pages):
    tasks = []
    async with ClientSession() as session:
        for item in pages:
            task = asyncio.ensure_future(fetch(item, session))
            tasks.append(task)
        return await asyncio.gather(*tasks)


def parse(responses):
    data = []
    for i in responses:
        root = etree.HTML(i)
        topics.extend(root.xpath('//div[@class="list-inner"]/a/text()'))
        data.extend(root.xpath('//a[@class="topictitle"]/@href'))
        authors.extend(root.xpath('//dd[@class="author"]/a/text()'))
    links = []
    for items in data:
        links.append('http://forum.overclockers.ua' + items[1:])

    return links


def find_money(articles):
    prices = []
    currency = []
    for article in articles:
        regexp = re.compile('(\d*)[ ]?(грн)')
        result = regexp.findall(str(article))
        if not result:
            prices.append(0)
            currency.append('грн')
        else:
            prices.append(result[0][0])
            currency.append(result[0][1])
    return prices, currency


if __name__ == '__main__':
    url = "http://forum.overclockers.ua/viewforum.php?f=26&start={}"

    loop = asyncio.get_event_loop()
    how_much = int(input('Pages: '))

    return_pages = loop.run_until_complete(get_pages(how_much))

    topics = []
    authors = []
    pages = parse(return_pages)

    return_topics = loop.run_until_complete(get_topics(pages))

    articles = []
    for item in return_topics:
        root = etree.HTML(item)
        text = root.xpath('//div[@class="content"]')[0].xpath('./descendant-or-self::text()')
        text = " ".join(text)
        articles.append(text)
    price, currency = find_money(articles)

    # cur.execute('''
    #     CREATE TABLE IF NOT EXISTS posts(
    #        id SERIAL PRIMARY KEY,
    #        author TEXT NOT NULL,
    #        url TEXT NOT NULL,
    #        topic TEXT NOT NULL,
    #        article_text TEXT NOT NULL,
    #        price TEXT NOT NULL,
    #        currency TEXT NOT NULL
    #     );
    #     ''')
    #
    # count = 0
    # for i in range(len(authors)):
    #     cur.execute("""INSERT INTO posts (author, url, topic, article_text, price, currency)
    #                        SELECT %s, %s, %s, %s, %s, %s
    #                        WHERE NOT EXISTS (SELECT * FROM posts where topic = %s and author = %s)""",
    #                 (authors[i], pages[i], topics[i], articles[i], price[i], currency[i], topics[i],
    #                  authors[i]))
    #     count += 1
    #
    # conn.commit()
    # conn.close()
    # print('found: {}'.format(count))
    engine = create_engine('postgresql://postgres:2367@localhost:5432/postgres')
    Base.metadata.create_all(engine)
    DBSession = sessionmaker(engine)
    session = DBSession()
    for i in range(len(topics)):
        new_post = Posts(author=authors[i],
                         url=pages[i],
                         topic=topics[i],
                         article_text=articles[i],
                         price=price[i],
                         currency=currency[i])
        session.add(new_post)

    session.commit()
