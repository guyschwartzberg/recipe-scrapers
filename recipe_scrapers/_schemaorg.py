import extruct
from ._utils import get_minutes, normalize_string, get_diet_from_tags

SCHEMA_ORG_HOST = "schema.org"
SCHEMA_NAMES = ["Recipe", "WebPage"]

SYNTAXES = ["microdata", "json-ld"]


class SchemaOrgException(Exception):
    def __init__(self, message):
        super().__init__(message)


class SchemaOrg:

    def __init__(self, page_data):
        self.format = None
        self.data = {}

        data = extruct.extract(
            page_data,
            syntaxes=SYNTAXES,
            uniform=True,
        )

        for syntax in SYNTAXES:
            for item in data.get(syntax, []):
                if (
                    SCHEMA_ORG_HOST in item.get("@context", "") and
                    item.get("@type", "").lower() in [schema.lower() for schema in SCHEMA_NAMES]
                ):
                    self.format = syntax
                    self.data = item
                    if item.get("@type").lower() == 'webpage':
                        self.data = self.data.get('mainEntity')
                    return

    def language(self):
        return self.data.get("inLanguage") or self.data.get("language")

    def title(self):
        return self.data.get("name")

    def total_time(self):
        total_time = get_minutes(self.data.get("totalTime"))
        if not total_time:
            return (
                get_minutes(self.data.get('prepTime')) +
                get_minutes(self.data.get('cookTime'))
            )
        return total_time

    def yields(self):
        recipe_yield = str(self.data.get("recipeYield"))
        if len(recipe_yield) <= 3:  # probably just a number. append "servings"
            return recipe_yield + " serving(s)"
        return recipe_yield

    def image(self):
        image = self.data.get('image')

        if image is None:
            raise SchemaOrgException("Image not found in SchemaOrg")

        if type(image) == dict:
            return image.get('url')
        elif type(image) == list:
            if type(image[0]) == dict:
                return image[0].get('url')
            return image[0]

        return image

    def ingredients(self):
        return [
            normalize_string(ingredient)
            for ingredient in self.data.get("recipeIngredient", [])
        ]

    def instructions(self):
        recipe_instructions = self.data.get('recipeInstructions')
        if type(recipe_instructions) == list:
            if type(recipe_instructions[0]) == str:
                return '\n'.join(
                    instruction
                    for instruction in recipe_instructions
                )
            else:
                return '\n'.join(
                    instruction.get('text')
                    for instruction in recipe_instructions
                )
        return recipe_instructions

    def suitable_for_diet(self):
        diet = self.data.get("suitableForDiet")
        tags = self.tags()
        if diet is None or not diet:
            if tags is None or not tags:
                return []
            return get_diet_from_tags(tags)
        if type(diet) == list:
            diet_info = [x.strip().replace('http://schema.org/', '').replace('Diet', '').lower() for x in diet]
            return list(set(diet_info).union(set(get_diet_from_tags(tags))))

    def ratings(self):
        ratings = self.data.get("aggregateRating", None)
        if ratings is None:
            return None

        if type(ratings) == dict:
            return round(float(ratings.get('ratingValue')), 2)
        return round(float(ratings), 2)

    def tags(self):
        tags = self.data.get("keywords")
        if tags is None:
            raise SchemaOrgException('No tag data in SchemaOrg.')
        if type(tags) == str:
            return [x.strip() for x in tags.split(',')]


