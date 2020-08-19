# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import requests
import numpy as np
from time import sleep
import bot_token

def get_updates_json(request):  
    response = requests.get(request + 'getUpdates')
    return response.json()

def get_numbered_update(request, message_id):
    json = get_updates_json(request)
    if (message_id >= len(json['result'])):
        return np.NaN
    message_text = json['result'][message_id]['message']['text']
    if message_text == '/start':
        return np.NaN
    return float(message_text)

if '__main__' == __name__:
    json = get_updates_json(url)
    next_message_number = len(json['result'])
    while(True):
        number = get_numbered_update(url, next_message_number)
        if ~np.isnan(number):
            json = get_updates_json(url)
            reply_text = 'Accepted'
            params = {'chat_id': json['result'][next_message_number]['message']['chat']['id'], 'text': reply_text}
            response = requests.post(url + 'sendMessage', data = params)
            print(response)
            next_message_number += 1
        sleep(1)
    
def describe(number_list):
    import numpy as np
    count = len(number_list)
    if (0 == count):
        return("No numbers in list")
    mean = np.mean(number_list)
    std = np.std(number_list)
    return "A list of " + str(count) + " samples with mean " + str(round(mean, 2)) + " and deviation " + str(round(std, 2))

def describe_no_dependencies(number_list):
    count = len(number_list)
    if (0 == count):
        return("No numbers in list")
    sum = 0
    for i in range(0, len(number_list)):
        sum = sum + number_list[i]
    mean = sum / count
    sum_sq = 0
    for i in range(0, len(number_list)):
        sum_sq = sum_sq + (number_list[i] - mean)**2
    std = (sum_sq / (count - 1))**0.5
    return "A list of " + str(count) + " samples with mean " + str(round(mean, 2)) + " and deviation " + str(round(std, 2))