from ._abstract import AbstractScraper
from ._utils import normalize_string, get_diet_from_tags


class AllRecipes(AbstractScraper):

    @classmethod
    def host(self):
        return 'allrecipes.com'

    def tags(self):
        try:
            s = normalize_string(self.soup.find("div", {"class":"keyvals"})['data-content_cms_tags'])
        except TypeError:
            return None
        return s.split("|")

    def suitable_for_diet(self):
        return get_diet_from_tags(self.tags())

