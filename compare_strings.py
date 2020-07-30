import json
import requests, time
from googletrans import Translator

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
        arr = []
        for i in response:
            arr.append(response[i]['sim']['score'])
        if arr == []:
            arr.append(0)
        print(string1, string2, max(arr))
        return max(arr)

    else:
        return 'Error:', result['msg']

def getSimAlt(string1, string2):
    # data = 'body=[{"term":"Yes"},{"text": "Yes I know"}]'
    # headers = {"content-type": "application/json"}
    # params = (('priority', 'normal'))
    # url = "http://api.cortical.io:80/rest/compare?retina_name=en_associative"
    # r = requests.post(url, headers=headers, data=data)
    # print(r)
    trans = Translator()
    str1 = trans.translate(string1, src="ru", dest="en").text
    str2 = trans.translate(string2, src="ru", dest="en").text
    if str1.lower() == str2.lower():
        print(str1, str2, 1)
        return 1
    else:
        try:
            url = 'http://api.cortical.io:80/rest/compare?retina_name=en_associative'
            print(str1, str2)
            params = {
            "retina_name":"en_associative",
            "start_index":0,
            "max_results":1,
            "sparsity":1.0,
            "get_fingerprint":False
            }
            data = [{"term":str1}, {"text":str2}]
            while True:
                r = requests.post(url, json=data)
                time.sleep(1)
                if r.status_code != 429:
                    break
            print(r.status_code, str1, str2)
            res = r.json()["cosineSimilarity"]
            if __name__ == "__main__":
                print(res)
            print(str1, str2, res)
            return res
        except:
            return 0

if __name__ == "__main__":
    getSimAlt("back", "Come to the back door")








