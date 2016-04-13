#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests


def main():
    r = requests.get('https://api.github.com/events')
    print r.text


if __name__ == '__main__':
    main()
