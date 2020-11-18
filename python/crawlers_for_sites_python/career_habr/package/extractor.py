from package.custom_exeptions import SeveralElementsFound, NoElementFound


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


class Attribute(CSSExtractor):

    def convert(self, element_list):
        return element_list[0].attrib['title']


class Href(CSSExtractor):

    def convert(self, element_list):
        return element_list[0].attrib['href']

