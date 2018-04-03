import requests
import json

def publics():
    string = []
    pubdic = {}
    pub = [71114104, 132176157, 72340177, 88350989, 122162987, 139069603,
    68232062, 29606875, 81671374, 91624558, 147286578]
    for gid in pub:
        token='6bca1415abf87ea3b901fa146a010209449123cf9020df5d9ced8569f61ee5ff920647e59fef2361fba6f'
        pd = {'url': 'https://api.vk.com/method/groups.getById?',
        'data': {'access_token': token, 'v': 3, 'group_id':gid}}
        resp = posting(pd['url'], pd['data'])['response']
        a = pubdic[gid] = resp[0]['name']
        print (a)
        input()


def posting(url, data):
    response = requests.post(url, data)
    return json.loads(response.text)

publics()
