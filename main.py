import json

from box import Box
from spiders.spider import Spider


def main():
    with open("sites.json", "r") as file:
        sites = Box(json.load(file))

    for site in sites.rss_feeds:
        Spider(site.url)


if __name__ == "__main__":
    main()
