"""
1. Написать скрипт, собрающий информацию о велосипедах с сайта trial-sport.
В параметрах командной строки завать количество велосипедов
Собрать следующие поля: название, описание, цена
Данные сохранить в файл
2. Написать скрипт, выводящий данные в терминал
"""

import requests
from time import sleep
import random
from lxml import etree
from urllib.parse import urljoin
from storage import Storage


storage_api = Storage()


class SeveralElementsFound(Exception):

    def __init__(self, css):
        super().__init__('several elements found by CSS %s' % css)


class NoElementFound(Exception):

    def __init__(self, css):
        super().__init__('no elements found by CSS %s' % css)



class CSSExtractor:

    def __init__(self, css):
        self.css = css

    def __get__(self, descriptor, descriptor_cls):
        element_list = self.extract(descriptor)
        return self.convert(element_list)

    def extract(self, descriptor):
        return descriptor.container.cssselect(self.css)

    def convert(self, element_list):
        raise NotImplementedError


class Text(CSSExtractor):

    def convert(self, element_list):
        if len(element_list) == 1:
            return element_list[0].text.strip()
        elif len(element_list) > 1:
            raise SeveralElementsFound(self.css)
        else:
            raise NoElementFound(self.css)


class Available(CSSExtractor):

    def convert(self, element_list):
        return not bool(element_list)


class Href(CSSExtractor):

    def convert(self, element_list):
        return element_list[0].attrib['href']


class PositiveInt(CSSExtractor):

    def convert(self, element_list):
        price_split = element_list[0].text.split()
        result = int(''.join(price_split))
        assert result > 0
        return result


class TrialSportDescriptor:
    url = 'https://trial-sport.ru'

    def get_pagination(self, q):
        return self.Pagination(
            urljoin(self.url, 'gds.php?q=%s' % q)
        )

    class Pagination:

        def __init__(self, url):
            self.url = url

        @property
        def pages(self):
            yield self.Page(self.url)
            page = 2
            while True:
                yield self.Page(self.url + '&pg=%s' % page)
                page += 1

        class Page:
            item_css = '.objects > .object'

            def __init__(self, url):
                self.url = url
                self.page = None

            def parse(self, source_code):
                self.page = etree.HTML(source_code)
                for item_container in self.page.cssselect(self.item_css):
                    yield self.Item(self, item_container)

            class Item:

                def __init__(self, parent, container):
                    self.parent = parent
                    self.container = container

                title = Text('.title')
                href = Href('.title')

                @property
                def url(self):
                    return urljoin(self.parent.url, self.href)

                description = Text('.description')
                available = Available('.not-avail')
                price = PositivInt('.price .value')


def wait(min_wait, max_wait):
    seconds_to_wait = round(
        random.uniform(min_wait, max_wait),
        3
    )
    print('sleeping %s seconds' % seconds_to_wait)
    sleep(seconds_to_wait)


# def crawl(q, limit):
#     bike_data = storage_api.read()
#
#     gen = generate_urls(q)
#     for url in gen:
#         source_code = requests.get(url).text
#         page = etree.HTML(source_code)
#
#         for bike_item in page.cssselect('.objects > .object'):
#             if len(bike_data) == limit:
#                 return bike_data
#
#             title = bike_item.cssselect('.title')[0]
#             href = title.attrib['href']
#             url = urljoin('https://trial-sport.ru', href)
#
#             if url in bike_data:
#                 continue
#
#             description = bike_item.cssselect('.description')[0].text
#             price_split = ''.join(bike_item.cssselect('.price .value')[0].xpath('.//text()')).split()
#             price = int(''.join(price_split))
#             avail = not bool(bike_item.cssselect('.not-avail'))
#
#             bike_data[url] = {
#                 'title': title,
#                 'description': description,
#                 'price': price,
#                 'available': avail
#             }
#
#         wait(1, 5)


def save_data(bike_data):
    storage_api = Storage()
    storage_api.write(bike_data)


if __name__ == '__main__':
    bikes_cnt = 10

    trial_sport = TrialSportDescriptor()
    pagination = trial_sport.get_pagination(q="велосипеды")
    for page in pagination.pages:
        page_text = requests.get(page.url).text
        items = page.parse(page_text)
        for item in items:
            print(item.title)
            print(item.title)
            print(item.href)
            print(item.url)
            print(item.description)
            print(item.available)
            print(item.price)
            print()
            if bikes_cnt == 0:
                exit()

            bikes_cnt -= 1
