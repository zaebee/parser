# parser

## install

``` virtualenv .env
``` pip install grab

## run
Available 3 backends:
- `nyt` - nytimes.com
- `dep` - departures.com
- `tmout` - timeout.com

Now is wirking only timeout.com parser. Example:

```./spider.py --engine='tmout' --url='/newyork/restaurants/the-100-best-dishes-in-new-york-city-2014-best-pizza'```
