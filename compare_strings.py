import json
import requests

# 1. Get your authentication token
# by posting username and password to the server
def getSim(string1, string2, lang='ru', login='arslan2233', password='qwer2004'):
    r = requests.post('http://paraphraser.ru/token/',
                      data={'login': login, 'password': password})
    token = r.json().get('token', '')

    # 2. Make a request using the obtained token

    payload = {'c': 'sim',
               'query': string1+';'+string2,
               'type': 'vector',
               'format': 'json',
               'lang': lang,
               'token': token}

    r = requests.post('http://paraphraser.ru/api/',
                      data=payload)
    result = r.json()


    if result['code'] == 0:
        response = result['response']

        return response['1']['sim']['score']

    else:
        return 'Error:', result['msg']