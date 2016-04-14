#!/usr/bin/env python
# -*- coding: utf-8 -*-


import requests
import click
import random


BOT_API_URL = 'https://api.telegram.org/bot'
secret_number = 42


def process_message(text):
    global secret_number
    if text == '/start':
        secret_number = random.randint(1, 100)
        return 'Я загадал число от 1 до 100, попробуй угадать!'
    try:
        v = int(text)
    except ValueError:
        return 'Нужно ввести число'
    if v > secret_number:
        return 'Слишком много!'
    if v < secret_number:
        return 'Слишком мало!'
    secret_number = random.randint(1, 100)
    return 'Точно! Давай попробуем другое число.'


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
        req = {'timeout': 5}
        if update_id is not None:
            req['offset'] = update_id
        response = requests.post(BOT_API_URL + token + '/getUpdates', json=req).json()
        result_array = response['result']
        for result in result_array:
            process_updates(token, result)
            update_id = result['update_id'] + 1


if __name__ == '__main__':
    main()
