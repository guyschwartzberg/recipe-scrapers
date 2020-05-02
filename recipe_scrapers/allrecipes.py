from ._abstract import AbstractScraper


class AllRecipes(AbstractScraper):

    @classmethod
    def host(self):
        return 'allrecipes.com'

    def tags(self):
        try:
            s = self.soup.find("div", {"class":"keyvals"})['data-content_cms_tags']
        except TypeError:
            return None
        return s.split("|")


