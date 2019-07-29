#!/usr/bin/env python3
from bs4 import BeautifulSoup as bsoup
import requests as req
import argparse

from SubReddit import Entry
from Constants import RSS_SUFFIX, STATUS_OK, URL_TMPLT, U_AGENT_STR


def sanitize_rss_url(url):
    if not url.endswith(RSS_SUFFIX):
        url += '/' if not url[-1] == '/' else ''
        url += RSS_SUFFIX
    return url


def fetch_feed(url):
    res = req.get(url, headers=U_AGENT_STR, params={'sort': 'new'})
    if not res.status_code == STATUS_OK:
        print(f"GET[{url}] failed. Response code: {res.status_code}")
        return
    return bsoup(res.content, 'lxml')


def parse_entries(rss):
    entries = [Entry.create_entry(ent) for ent in rss.findAll("entry")]
    for i, ent in enumerate(entries):
        print(f"{ent._update.ctime()} Title: {ent._title}")


def main(subreddit):
    url = URL_TMPLT.format(subreddit)
    rss = fetch_feed(sanitize_rss_url(url))
    parse_entries(rss)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Console reddit client")
    parser.add_argument("-r", "--subreddit",
                        help="Subreddit to fetch e.g: news, python",
                        type=str, default="all")
    args = parser.parse_args()

    main(subreddit=args.subreddit)
