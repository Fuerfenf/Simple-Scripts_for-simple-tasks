class SeveralElementsFound(Exception):

    def __init__(self, css):
        super().__init__('several elements found by CSS %s' % css)


class NoElementFound(Exception):

    def __init__(self, css):
        super().__init__('no elements found by CSS %s' % css)
