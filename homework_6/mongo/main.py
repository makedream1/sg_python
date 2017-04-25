import asyncio
from aiohttp import ClientSession
from lxml import etree
import re
from pymongo import MongoClient


async def fetch(url, session):
    async with session.get(url) as response:
        assert response.status == 200
        return await response.text()


async def get(pages):
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
    how_much = input('Pages (Default 1): ')
    how_much = 1 if not how_much else how_much
    pages = []

    for item in range(int(how_much)):
        item = 1 if item == 0 else item
        pages.append(url.format(item * 40))

    loop = asyncio.get_event_loop()

    return_pages = loop.run_until_complete(get(pages))

    topics = []
    authors = []
    pages = parse(return_pages)

    return_topics = loop.run_until_complete(get(pages))

    articles = []
    for item in return_topics:
        root = etree.HTML(item)
        text = root.xpath('//div[@class="content"]')[0].xpath('./descendant-or-self::text()')
        text = " ".join(text)
        articles.append(text)
    price, currency = find_money(articles)

    count = 0
    client = MongoClient()
    db = client['test-database']
    posts = db['scraper_posts']
    all_results = []
    for i in range(len(topics)):
        link = pages[i].split('&sid')[0]

        duplicate = posts.find({"url": link}).count()
        if not duplicate:
            post = {"author": authors[i],
                    "url": link,
                    "topic": topics[i],
                    "price": price[i],
                    "currency": currency[i],
                    "text": articles[i],
                    }
            all_results.append(post)
            count += 1
    try:
        posts.insert_many(all_results).inserted_ids
    except:
        print("Not found new posts")
    print('Found:', count)
    print('Total:', posts.find().count())
