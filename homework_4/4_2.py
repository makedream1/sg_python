import threading
import requests
from lxml import html
from queue import Queue
import logging


class Scraper:
    def __init__(self, query, page_from, page_to, limit=2):
        self.query = query
        self.page_from = page_from
        self.page_to = page_to + 1
        self.limit = limit

    def __prepare(self):
        HEADERS = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/web p, * / *;q = 0.8',
            'Accept-Encoding': 'gzip, deflate, lzma, sdch',
            'Accept-Language': 'ru-RU,ru;q=0.8,enUS;q=0.6,en;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Host': 'www.olx.ua',
            'Referer': 'https://www.olx.ua/',
            'Save-Data': 'on',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit / 537.36(KHTML, like Gecko) '
                          'Chrome / 54.0.2840.99 Safari / 537.36 OPR / 41.0.2353.69'}
        self.session = requests.Session()
        self.session.headers.update(HEADERS)

    def start(self):
        self.__prepare()
        queue = Queue()
        threads = []
        for i in range(self.page_from, self.page_to):
            thread = threading.Thread(target=self.target_func, args=(self.get_link(i), self.notify, queue))
            thread.start()
            threads.append(thread)

        for th in threads:
            th.join()

        data = []
        while not queue.empty():
            data.extend(queue.get())
            queue.task_done()
        return data

    def notify(self, url):
        logging.basicConfig(filename='logs.log', level=logging.INFO)
        logging.info('Task done: %s' % url)

    def get_link(self, page):
        link = 'https://www.olx.ua/chernovtsy/q-{0}/?page={1}'.format(self.query, page)
        return link

    def crawl(self, url):
        resp = self.session.get(url)
        if resp.status_code == 200:
            page = resp.text
            root = html.fromstring(page)
            items = []
            offers = root.xpath('//td[@class="offer "]')
            for offer in offers:
                try:
                    title = offer.xpath('.//div[@class="space rel"]/h3/a/strong/text()')[0]
                    price = offer.xpath('.//td[@class="wwnormal tright td-price"]//p/strong/text()')[0]
                    items.append((title, price))
                except:
                    pass
            return items

    def target_func(self, url, logs, que):
        logs(url)
        que.put(self.crawl(url))


scrapper = Scraper('iphone', 1, 5, limit=2)
results = scrapper.start()
for result in results:
    offer, price = result
    print(offer, price)
