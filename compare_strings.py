
import json
import requests

# 1. Get your authentication token
# by posting username and password to the server

r = requests.post('http://paraphraser.ru/token/',
                  data={'login': 'user', 'password': '12345678'})
token = r.json().get('token', '')

# 2. Make a request using the obtained token

payload = {'c': 'syns',
           'query': 'кот ест рыбку',
           'top': 3,
           'scores': 0,
           'forms': 0,
           'format': 'json',
           'lang': 'ru',
           'token': token}

r = requests.post('http://paraphraser.ru/api/',
                  data=payload)
result = r.json()


if result['code'] == 0:
    response = result['response']

    for item in response:
        for value in response[item]['syns']:
            print(value)

else:
    print('Error:', result['msg'])