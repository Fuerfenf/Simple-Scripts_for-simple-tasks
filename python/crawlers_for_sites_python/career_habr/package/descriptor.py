from urllib.parse import urljoin
from lxml import etree
from package.extractor import *


class HabrDescriptor:
    base_url = "https://career.habr.com"

    def get_pagination(self, query_vac, max_pages):
        return self.Pagination(
            urljoin(self.base_url, '/vacancies?currency=rur&page={}&q={}'.format(None, query_vac)), max_pages
        )

    class Pagination:

        def __init__(self, url, max_pages):
            self.url = url
            self.max_pages = max_pages

        @property
        def pages(self):
            yield self.Page(self.url)
            page = 1
            while page < self.max_pages:
                yield self.Page(self.url.replace("None", str(page)))
                page += 1

        class Page:
            item_css = '.job'

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

                href = Href('.job_icon')

                @property
                def url(self):
                    return urljoin(self.parent.url, self.href)

                vacancy_name = Attribute('.title')
                company_name = Text('.company_name a')




