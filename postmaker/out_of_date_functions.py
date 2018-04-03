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
