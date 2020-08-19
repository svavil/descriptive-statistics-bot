# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import numpy as np
from time import sleep
import os

def get_updates_json(request):  
    response = requests.get(request + 'getUpdates')
    return response.json()

def get_numbered_update(json, message_id):
    if (message_id >= len(json['result'])):
        return np.NaN
    message_text = json['result'][message_id]['message']['text']
    if message_text == '/start':
        return np.NaN
    return float(message_text)

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
        number = get_numbered_update(json, next_message_number)
        if ~np.isnan(number):
            chat_id = json["result"][next_message_number]["message"]["chat"]["id"]
            if chat_id in statistics.keys():
                statistics[chat_id] = statistics[chat_id] + [number]
            else:
                statistics[chat_id] = [number]
            reply_text = describe(statistics[chat_id])
            params = {'chat_id': chat_id, 'text': reply_text}
            response = requests.post(url + 'sendMessage', data = params)
            print(response)
            next_message_number += 1
        sleep(1)
