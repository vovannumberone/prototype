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

def get_connected_pubs(username):
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
