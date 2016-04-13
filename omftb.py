#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import click


BOT_API_URL = 'https://api.telegram.org/bot'


@click.command()
@click.argument('token')
def main(token):
    r = requests.post(BOT_API_URL + token + '/getUpdates', json={'timeout': 1})
    print r.json()


if __name__ == '__main__':
    main()
