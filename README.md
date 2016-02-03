# Instagram hashtag parser

## install

``` virtualenv .env```

``` source .env/bin/activate```

``` pip install grab```

We need `python-instagram` lib but official repo has a bug https://github.com/Instagram/python-instagram/issues/214, so I install fork:
```pip install -e "git+https://github.com/skywritergr/python-instagram.git#egg=instagram"```

## run

Examples:

```./spider.py --hashtag='наширукинедляскуки'```

```./spider.py  -t 'trendever'```


## SIC!
You need set Instagram `API_ACCESS_TOKEN`. I hardcoded my token into Spider `prepare` method.

Alse you need install system packages `sudo apt-get install libcurl4-openssl-dev libxslt1-dev libxml2-dev`
