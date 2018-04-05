"""
Here I store my old functions, wich was working good, but lost actuality
And if I'll need some old fashion and good workind functions, that i can trust
- i can find em there.
"""

def postmaker_old(request, page=0, direct='next'):
    """This is good old postmaker. But it shits on URL line"""
    response = ''
    from . import postgetter
    post_list = postgetter.sl

    if direct == 'prev':
        page -=1
        try:
            link = post_list[page]['full_link']
        except KeyError:
            page = page+1
    elif direct == 'next':
        page +=1
        try:
            link = post_list[page]['full_link']
        except KeyError:
            page = page-1

    if request.method == 'POST' and "make_post" in request.POST:
        gid = int(request.POST["make_post"])
        post_data = post_list[page]
        response = make_post(post_data, gid)

    link = post_list[page]['full_link']
    if post_list[page]['text'] == '':
        text = 'Sample text.'
    else:
        text = post_list[page]['text']
    return render(request, 'postmaker/postmaker.html', {'request': request,
    'link': link, 'text': text, 'page': page, 'response': response})

def get_connected_pubs_1(username):
    """This function takes a User class instance, like below:
    user_name = User.objects.filter(username=username)[0]
    So this is not actually a "username"
    """
    pubs = Publics.objects.filter(username=username)[0]
    pubs = pubs.destringalize()
    pubdict = {}
    for pub in pubs:
        name_data = {'url': 'https://api.vk.com/method/groups.getById?',
        'data': {'access_token': token, 'v': 5.73, 'group_id': pub}}
        pubdict[pub] = posting(name_data['url'], name_data['data'])['response'][0]['name']
    return pubdict

def get_connected_pubs_2(user):
    #user = User.objects.filter(username=username)[0]
    account = Account.objects.filter(user=user)[0]
    publist = account.destringalize()
    return HttpResponse(publist)
    # token = account.token
    pubdict = {}
    for pub in publist:
        time.sleep(0.3)
        name_data = {'url': 'https://api.vk.com/method/groups.getById?',
        'data': {'access_token': token, 'v': 5.73, 'group_id': pub}}
        pubdict[pub] = posting(name_data['url'], name_data['data'])['response'][0]['name']
    return pubdict


def login_view(request):
    """ Just an old and dirty login view. """
    data = {}
    #if request.user.is_authenticated:
    #    ath = 'You are logged as %s.' % request.user.username
    #else:
    #    ath = 'You are NOT logged in.'

    if "log_out" in request.POST:
        auth.logout(request)
        return render(request, 'postmaker/info_page.html', {'msg': 'You are logged out.'})

    #if request.method == 'POST' and 'log_out' not in request.POST:
    if request.method == 'POST': # Looks loike the above version doesn't make sense
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            msg = 'Logged in successfully.'
        else:
            msg = 'Login failure occured. Retry.'
        #return render(request, 'postmaker/login_page.html', {'msg': msg, 'ath': ath, 'link': LINK})
        return redirect(LINK)
    else:
        msg = ''
        error = ''
        return render(request, 'postmaker/login_page.html', {'msg': msg, 'error': error, 'link': LINK})

def send(request):
    #if request.method == 'POST':
    #    user = request.POST["user"]
    #    msg = request.POST["message"]
    #    token='1ba1f52a377dca1bc65a435efa3ae4b5213c344163d04bdbbce1431b06b1af10f6b0c33e283cc0caa50e3'
    #    data={'url': 'https://api.vk.com/method/messages.send?',
    #    'data': {'access_token': token, 'v': 5.71, 'user_id': user, 'message': msg}}
    #    response = requests.post(data['url'], data['data'])
    #    result = str(json.loads(response.text))
    #    return render (request, 'blog/send_result.html', {'result': result})
    if 'code' in request.GET:
        code = request.GET['code']
        token_link = "https://oauth.vk.com/access_token?client_id=5898704&client_secret=AmGtZ1I4meDTrmIx5XgI&redirect_uri=https://hell0world.pythonanywhere.com/send/&code=" + str(code)
        response = requests.post(token_link)
        token = json.loads(response.text)['access_token']
        return HttpResponse("Here's you token, cowboy - " + str(token))
    elif 'error' in request.GET:
        error = request.GET['error']
        error_description = request.GET['error_description']
        # Эту ветвь надо продлить (!)
    else:
        return redirect('https://oauth.vk.com/authorize?client_id=5898704&display=popup&redirect_uri=https://hell0world.pythonanywhere.com/send/&scope=notify,friends,photos,audio,video,pages,status,notes,wall,ads,offline,docs,groups,notifications,stats,email&response_type=code&v=5.71&state=6666666')

# MODELS
class Account(models.Model):
    """
    from django.db import models
    from django.contrib.auth.models import User
    from postmaker.models import Publics
    142223503, 124367984, 124367240
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=100, null=True, blank=True)
    publics = models.CharField(max_length=500, null=True, blank=True)

    def stringalize(self, publics):
        self.publics = json.dumps(publics)

    def destringalize(self):
        return json.loads(self.publics)

    def get_clear_pubs(self):
        publics = self.publics[1:]
        publics = publics[:-1]
        return publics
