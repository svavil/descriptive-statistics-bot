# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
from time import sleep
import os

CODE_PASS = 0
CODE_START = 1
CODE_CLEAR = 2
CODE_MESSAGE = 3

def get_updates_json(request):  
    response = requests.get(request + 'getUpdates')
    return response.json()

def get_numbered_update(json, message_id):
    if (message_id >= len(json['result'])):
        return -1, CODE_PASS, -1
    chat_id = json["result"][message_id]["message"]["chat"]["id"]
    message_text = json['result'][message_id]['message']['text']
    if message_text == '/start':
        return chat_id, CODE_START, 0
    if message_text == "/clear":
        return chat_id, CODE_CLEAR, 0
    return chat_id, CODE_MESSAGE, float(message_text)

def describe(number_list):
    import numpy as np
    count = len(number_list)
    if (0 == count):
        return("No numbers in list")
    mean = np.mean(number_list)
    std = np.std(number_list)
    return "A list of " + str(count) + " samples with mean " + str(round(mean, 2)) + " and deviation " + str(round(std, 2))

if '__main__' == __name__:
    TOKEN = os.environ["BOT_TOKEN"]
    url = "https://api.telegram.org/bot" + TOKEN + "/"
    json = get_updates_json(url)
    next_message_number = len(json['result'])
    statistics = {}
    while(True):
        json = get_updates_json(url)
        chat_id, message_code, message_content = get_numbered_update(json, next_message_number)
        if message_code == CODE_PASS:
            sleep(1)
            continue
        if message_code == CODE_MESSAGE:
            if chat_id in statistics.keys():
                statistics[chat_id] = statistics[chat_id] + [message_content]
            else:
                statistics[chat_id] = [message_content]
            reply_text = describe(statistics[chat_id])
        if message_code == CODE_CLEAR:
            statistics[chat_id] = []
            reply_text = "Array cleared"
        if message_code == CODE_START:
            reply_text = "Enter one number at a time to accumulate statistics"
        params = {'chat_id': chat_id, 'text': reply_text}
        print(f"Sending message: {reply_text} to chat_id: {chat_id}")
        response = requests.post(url + 'sendMessage', data = params)
        print(response)
        next_message_number += 1
