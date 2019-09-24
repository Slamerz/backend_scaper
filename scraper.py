#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module docstring: One line description of what your program does.

There should be a blank line in between description above, and this
more detailed description. In this section you should put any caveats, 
environment variable expectations, gotchas, and other notes about running
the program.  Author tag (below) helps instructors keep track of who 
wrote what, when grading.
"""

__author__ = "Jacob Walker"

# Imports go at the top of your file, after the module docstring.
# One module per import line. These are for example only.
from HTMLParser import HTMLParser
import argparse
import re
import requests
import sys


class MyHTMLParser(HTMLParser):
    """Get a list of all relative urls in an a, or image tag"""
    url_list = []

    def handle_starttag(self, tag, attrs):
        if (tag == 'a' or tag == 'img') and attrs:
            self.url_list.append(attrs[0][1])


def scrape_url(url):
    """ Takes a url from command line arg and retrieves the text of the
    webpage, parsing out any URLs, email addresses, or phone numbers included
    in the HTML
    """
    r = requests.get(url)
    url_list = get_urls(r.text)
    email_list = get_email_addresses(r.text)
    phone_list = get_phone_numbers(r.text)

    print_list('Urls', url_list)
    print_list('Emails', email_list)
    print_list('Phone Numbers', phone_list)


def print_list(title, data):
    """Print data from collected lists to console"""
    message = '{} Found' \
              '-----------------------------------------------------' \
              '\n'.format(title)
    if data:
        for entry in data:
            message += entry + '\n'
    else:
        message += "none"
    print message + '\n\n'


def get_phone_numbers(r):
    """Get a list of all phone numbers in a string"""
    phone_match = re.findall(r'\d\d\d-\d\d\d-\d\d\d\d', r)
    phone_list = []
    if phone_match:
        for match in phone_match:
            if match not in phone_list:
                phone_list.append(match)
    phone_list = set(phone_list)
    return phone_list


def get_email_addresses(r):
    """Get a list of al email addresses from a string"""
    email_match = re.findall(r'[\w.-]+@[\w.-]+.\w+', r)
    email_list = []
    if email_match:
        for match in email_match:
            if match not in email_list:
                email_list.append(match)
    email_list = set(email_list)
    return email_list


def get_urls(r):
    """Get a list of all urls found in a string"""
    url_list = find_urls(r)
    url_list += find_tag_urls(r)
    return set(url_list)


def find_tag_urls(r):
    """Parse Html data to locate relative urls in img and A tags"""
    parser = MyHTMLParser()
    parser.feed(r)
    return parser.url_list


def find_urls(r):
    """Gets a list of all urls with https from a string"""
    http_match = re.findall(r'https:\/\/[\w\/?=.-]+', r)
    url_list = []
    if http_match:
        for match in http_match:
            if match not in url_list:
                url_list.append(match)
    return url_list


def create_parser():
    """Creates an argument parser object"""
    parser = argparse.ArgumentParser()
    parser.add_argument('url', help='url to scrape')
    return parser


def main(args):
    """Finds all urls, phone numbers, and email addresses from a given web page and returns them to the console"""
    parser = create_parser()

    if not args:
        parser.print_usage()
        sys.exit(1)

    parsed_args = parser.parse_args(args)
    scrape_url(parsed_args.url)


if __name__ == '__main__':
    main(sys.argv[1:])
