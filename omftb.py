#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import click


BOT_API_URL = 'https://api.telegram.org/bot'


def process_message(text):
    return 'what is "' + text + '"?'


def send_message(token, chat_id, text):
    req = {'chat_id': chat_id, 'text': text}
    requests.post(BOT_API_URL + token + '/sendMessage', json=req)


def process_updates(token, updates):
    if 'message' not in updates:
        return
    message = updates['message']
    if 'text' not in message:
        return
    text = message['text']
    chat = message['chat']
    chat_id = chat['id']
    send_message(token, chat_id, process_message(text))


@click.command()
@click.argument('token')
def main(token):
    update_id = None
    while True:
        req = {'timeout': 5, 'limit': 1}
        if update_id is not None:
            req['offset'] = update_id
        response = requests.post(BOT_API_URL + token + '/getUpdates', json=req).json()
        result_array = response['result']
        if not result_array:
            continue
        result = result_array[0]
        process_updates(token, result)
        update_id = result['update_id'] + 1


if __name__ == '__main__':
    main()
