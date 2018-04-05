import requests
import json
import time

long = [71114104, 132176157, 72340177, 88350989, 122162987, 139069603,
68232062, 29606875, 81671374, 91624558, 147286578] #22751485,  двач, слишком много постов беру  93082454, 114437208 мемзавод трудности с
short = [71114104, 132176157, 72340177]
memes = long
anime = [93566453, 100867898, 111230293, 125372241, 100389805, 100892059, 126167642,
104003829, 139383329, 135741815, 58110597, 21044057] #127473798 & 130717387 стали закрытой группой
bn = [43901086, 72188644, 64888663, 129754667, 141803118, 39186540, 72340177, 88350989, 46521427] # 95509314 паршивые одинаковые мемы и большой индекс
early = ['00:07', '01:07', '02:07', '03:07', '04:07']
schedule = ['08:07', '09:07', '10:07', '11:07', '12:07', '13:07',
'14:07', '15:07', '16:07', '17:07', '18:07', '19:07', '20:07', '21:07',
'22:07', '23:07']
post_list = {}
etholone = []
token='6bca1415abf87ea3b901fa146a010209449123cf9020df5d9ced8569f61ee5ff920647e59fef2361fba6f'
my_gid = 124367984
my_uid = 78767814
gids = memes
sort_type = 'reposts'

def now():
    return time.time()

def post(url, data):
    response = requests.post(url, data)
    return json.loads(response.text)

def sec_to_str(seconds, flag):
    if flag == 'a': #Wed May 31 11:39:24 2017
        return time.strftime("%a %b %d %H:%M:%S %Y", time.localtime(seconds))
    elif flag == 'b': #151 11:40:04 2017
        return time.strftime("%j %H:%M:%S %Y", time.localtime(seconds))
    elif flag == 'c': #21:18:07 03 Jun 2017
        return time.strftime("%H:%M:%S %d %b %Y", time.localtime(seconds))

def str_to_sec(string, flag):
    if flag == 'a':
        return time.mktime(time.strptime(string, "%a %b %d %H:%M:%S %Y"))
    elif flag == 'b':
        return time.mktime(time.strptime(string, "%j %H:%M:%S %Y"))
    elif flag == 'c':
        return time.mktime(time.strptime(string, "%H:%M:%S %d %b %Y"))

def write(text):
    file = open('post_log.txt', 'a')
    file.write('\n' + text)
    file.close()

def sort(dic, sort_type):
    indic = 1
    while indic > 0:
        indic = 0
        for i in dic:
            if i - 1 >= 1 and i - 1 <= len(dic):
                if dic[i][sort_type] > dic[i-1][sort_type]:
                    dic['temp'] = dic[i-1]
                    dic[i-1] = dic[i]
                    dic[i] = dic['temp']
                    dic.pop('temp')
                    indic =1

            elif i + 1 <= len(dic):
                if dic[i][sort_type] < dic[i+1][sort_type]:
                    dic['temp'] = dic[i]
                    dic[i] = dic[i+1]
                    dic[i+1] = dic['temp']
                    dic.pop('temp')
                    indic =1
    return dic

def yesterday():
    yesterday_1 = int(sec_to_str(now(), 'b')[:4]) - 1
    yesterday = str(yesterday_1) + sec_to_str(now(), 'b')[3:]
    return (sec_to_str(str_to_sec(yesterday, 'b'), 'a'))[:10]

def tomorrow():
    tomorrow_1 = int(sec_to_str(now(), 'b')[:4]) + 1
    tomorrow = str(tomorrow_1) + sec_to_str(now(), 'b')[3:]
    return sec_to_str(str_to_sec(tomorrow, 'b'), 'c')

def test(arg):
    print (arg)
    input('TEST STOPPER')

today = sec_to_str(now(), 'a')[:10]
day_case = today
#day_case = yesterday()
post_log = []

indic = 1
for gid in gids:
    time.sleep(0.3)
    wall_get = {'url': 'https://api.vk.com/method/wall.get?',
    'data': {'access_token': token, 'v': 5.71, 'owner_id': -gid, 'count': 50 }}
    wall = post(wall_get['url'], wall_get['data'])['response']['items']

    users_get = {'url': 'https://api.vk.com/method/groups.getMembers?',
    'data': {'access_token': token, 'v': 3, 'group_id': gid, 'count': 50 }}
    users = post(users_get['url'], users_get['data'])['response']['count']
    for i in range(1, len(wall)):
        if sec_to_str(wall[i]['date'], 'a')[:10] == day_case:
        #if sec_to_str(wall[i]['date'], 'a')[:10] == sec_to_str(now(), 'a')[:10]:
        #if sec_to_str(wall[i]['date'], 'a')[:10] == yesterday()[:10]:
            try:
                content_quantity = (len(wall[i]['attachments']) == 1)
                content_type = wall[i]['attachments'][0]['type'] == 'photo'
                not_an_ad = wall[i]['marked_as_ads'] == 0
                #has_no_text = wall[i]['text'] == ''
                if content_quantity and content_type and not_an_ad: #and has_no_text:
                    if str(wall[i]['attachments'][0]['photo']['id']) not in post_log:
                        views = wall[i]['views']['count']
                        if views != 0:
                            post_list[indic] = {}
                            post_list[indic]['owner_id'] = wall[i]['attachments'][0]['photo']['owner_id']
                            post_list[indic]['photo_id'] = wall[i]['attachments'][0]['photo']['id']
                            post_list[indic]['likes'] = wall[i]['likes']['count'] / views * 100000
                            post_list[indic]['reposts'] = wall[i]['reposts']['count'] / views * 100000
                            post_list[indic]['full_link'] = wall[i]['attachments'][0]['photo']['photo_604']
                            post_list[indic]['text'] = wall[i]['text']
                        #post_list[indic]['post_id'] = wall[i]['id']
                        #print ('\n', wall[i]['attachment']['photo']['pid'])
                        #print (post_list[indic]['photo_id'])
                        #post_list[indic]['pid_link'] = 'photo' +  str(post_list[indic]['owner_id']) + '_' + str(post_list[indic]['photo_id'])
                        indic +=1
                #else:
                    #print ('ELSE CASE')
                    #print ('content_quantity: ', content_quantity)
                    #print ('content_type: ', content_type)
                    #print ('not_an_ad: ', not_an_ad)
                    #print ('has_no_text: ', has_no_text)
                    #input()
            except KeyError:
                break

sl = sort(post_list, sort_type)
