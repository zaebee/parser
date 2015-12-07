# parser

## install

``` virtualenv .env
``` pip install grab

## run
Available 3 backends:
- `dep` - departures.com
- `tmout` - timeout.com
- `nyt` - nytimes.com (Not implemented)

Now is working timeout.com parser and departures.com parser. Example:

```./spider.py --engine='tmout' --url='/newyork/restaurants/the-100-best-dishes-in-new-york-city-2014-best-pizza'```

```./spider.py --engine='tmout' --url='/newyork/restaurants/battle-of-the-burgers-20-best-burgers'```

```./spider.py --engine='dep' --url='/10-new-york-cocktail-bars'```

```./spider.py --engine='dep' --url='/top-burgers-around-world'```
