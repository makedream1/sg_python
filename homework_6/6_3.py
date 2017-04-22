import asyncio
from aiohttp import ClientSession
from lxml import etree
import re


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
    for item in responses:
        root = etree.HTML(item)
        topics.extend(root.xpath('//div[@class="list-inner"]/a/text()'))
        data.extend(root.xpath('//a[@class="topictitle"]/@href'))
        authors.extend(root.xpath('//dd[@class="author"]/a/text()'))
    links = []
    for items in data:
        links.append('http://forum.overclockers.ua' + items)

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


def check_if_exists(cursor, author, topic_title):
    cursor.execute('''SELECT author FROM posts WHERE topics = (%s) AND author = (%s)''',
                   (topic_title, author))
    result = cursor.fetchone()

    if result:
        return True
    return False


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


    with open('text.txt', 'w', encoding='utf-8') as file:
        count = 0
        for i in range(len(authors)):
            dic = {'title': topics[i], 'url': pages[i], 'author': authors[i], 'text': articles[i], 'price': price[i],
                   'currency': currency[i]}
            file.write(str(dic) + '\n')
            count += 1
    print('inserted: {}'.format(count))
