import re

TIME_REGEX = re.compile(
    r'(\D*(?P<hours>\d+)\s*(hours|hrs|hr|h|Hours|H|óra))?(\D*(?P<minutes>\d+)\s*(minutes|mins|min|m|Minutes|M|perc))?'
)

SERV_REGEX_NUMBER = re.compile(
    r'(\D*(?P<items>\d+)?\D*)'
)

SERV_REGEX_ITEMS = re.compile(
    r'\bsandwiches\b |\btacquitos\b | \bmakes\b', flags=re.I | re.X
)

SERV_REGEX_TO = re.compile(
    r'\d+(\s+to\s+|-)\d+', flags=re.I | re.X
)

DISH_TYPE = {"keto", "lowcarb", "eggfree", "peanutfree", "soyfree", "diabetic", "glutenfree", "halal", "kosher",
             "lowcalorie", "lowfat", "lowlactose", "lactosefree", "lowsalt", "vegan", "vegetarian", "highfiber",
             "dairyfree", "lowcholesterol", "lowsodium", "nutfree"}


def get_minutes(element):
    try:
        if isinstance(element, str):
            tstring = element
        else:
            tstring = element.get_text()
        if '-' in tstring:
            tstring = tstring.split('-')[1]  # sometimes formats are like this: '12-15 minutes'
        if 'h' in tstring:
            tstring = tstring.replace('h', 'hours') + 'minutes'
        matched = TIME_REGEX.search(tstring)

        minutes = int(matched.groupdict().get('minutes') or 0)
        minutes += 60 * int(matched.groupdict().get('hours') or 0)

        return minutes
    except AttributeError:  # if dom_element not found or no matched
        return 0


def get_yields(element):
    """
    Will return a string of servings or items, if the receipt is for number of items and not servings
    the method will return the string "x item(s)" where x is the quantity.
    :param element: Should be BeautifulSoup.TAG, in some cases not feasible and will then be text.
    :return: The number of servings or items.
    """
    try:

        if isinstance(element, str):
            tstring = element
        else:
            tstring = element.get_text()

        if SERV_REGEX_TO.search(tstring):
            tstring = tstring.split(SERV_REGEX_TO.split(tstring)[1])[1]

        matched = SERV_REGEX_NUMBER.search(tstring).groupdict().get('items') or 0
        servings = "{} serving(s)".format(matched)

        if SERV_REGEX_ITEMS.search(tstring) is not None:
            # This assumes if object(s), like sandwiches, it is 1 person.
            # Issue: "Makes one 9-inch pie, (realsimple-testcase, gives "9 items")
            servings = "{} item(s)".format(matched)

        return servings

    except AttributeError as e:  # if dom_element not found or no matched
        print("get_serving_numbers error {}".format(e))
        return ''


def normalize_string(string):
    return re.sub(
        r'\s+', ' ',
        string.replace(
            '\xa0', ' ').replace(  # &nbsp;
            '\n', ' ').replace(
            '\t', ' ').strip()
    )


def get_diet_from_tags(tags):
    if tags is None or type(tags) is not list:
        return None
    tags = [re.sub(r'\s+', '', x.replace("-", '')).lower() for x in tags]
    return list(set(tags).intersection(DISH_TYPE))


def parsely_id_extract(soup):
    recipe_id = soup.find(
        'meta',
        {'name': "parsely-post-id"}
    )
    return recipe_id['content']
