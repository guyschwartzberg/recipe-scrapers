.. image:: https://img.shields.io/pypi/v/recipe-scrapers.svg?
    :target: https://pypi.org/project/recipe-scrapers/
    :alt: Version
.. image:: https://travis-ci.org/hhursev/recipe-scrapers.svg?branch=master
    :target: https://travis-ci.org/hhursev/recipe-scrapers
    :alt: Travis
.. image:: https://coveralls.io/repos/hhursev/recipe-scraper/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/hhursev/recipe-scraper?branch=master
    :alt: Coveralls
.. image:: https://img.shields.io/github/license/hhursev/recipe-scrapers?
    :target: https://github.com/hhursev/recipe-scrapers/blob/master/LICENSE
    :alt: License
.. image:: https://img.shields.io/github/stars/hhursev/recipe-scrapers?style=social
    :target: https://github.com/hhursev/recipe-scrapers/
    :alt: Github


------


A simple web scraping tool for recipe sites.

then:

.. code:: python

    from recipe_scrapers import scrape_me

    # give the url as a string, it can be url from any site listed below
    scraper = scrape_me('http://allrecipes.com/Recipe/Apple-Cake-Iv/Detail.aspx')

    scraper.title()
    scraper.total_time()
    scraper.yields()
    scraper.ingredients()
    scraper.instructions()
    scraper.image()
    scraper.links()

Note: ``scraper.links()`` returns a dictionary object containing all of the <a> tag attributes. The attribute names are the dictionary keys.
Note : The functions will return 0 or None if certain information isn't available on the website.

Scrapers available for:
-----------------------

- `http://allrecipes.com/ <http://allrecipes.com/>`_
- `http://bbc.com/ <http://bbc.com/food/recipes>`_
- `http://bbc.co.uk/ <http://bbc.co.uk/food/recipes>`_
- `http://bbcgoodfood.com/ <http://bbcgoodfood.com>`_
- `http://bettycrocker.com/ <http://bettycrocker.com>`_
- `http://bonappetit.com/ <http://bonappetit.com>`_
- `https://www.budgetbytes.com/ <https://www.budgetbytes.com>`_
- `http://closetcooking.com/ <http://closetcooking.com>`_
- `http://cookstr.com/ <http://cookstr.com>`_
- `http://copykat.com/ <http://copykat.com>`_
- `http://delish.com/ <http://delish.com>`_
- `http://epicurious.com/ <http://epicurious.com>`_
- `https://food.com/ <https://www.food.com>`_
- `http://foodnetwork.com/ <http://www.foodnetwork.com>`_
- `http://foodrepublic.com/ <http://foodrepublic.com>`_
- `http://tasty.co// <http://tasty.co>`_


