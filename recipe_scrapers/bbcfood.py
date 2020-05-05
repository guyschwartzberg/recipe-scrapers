from ._abstract import AbstractScraper
from ._utils import get_minutes, normalize_string, get_yields


class BBCFood(AbstractScraper):

    @classmethod
    def host(self, domain='com'):
        return 'bbc.{}'.format(domain)

