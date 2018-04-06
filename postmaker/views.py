from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from django.contrib import auth
from django.contrib.auth.models import User

from .models import *
from .forms import *
from . import postgetter
from prototype.settings import LINK

import requests
import json
import time

token='6bca1415abf87ea3b901fa146a010209449123cf9020df5d9ced8569f61ee5ff920647e59fef2361fba6f'

def posting(url, data):
    response = requests.post(url, data)
    return json.loads(response.text)

def index(request):
    if not request.user.is_authenticated:
        return redirect(LINK + 'login/')
    return render(request, 'postmaker/index.html')

def vkauth(request):
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

def user_account(request, user):
    if not request.user.is_authenticated:
        return redirect(LINK + 'login/')
    if request.method == "POST":
        if "new_pid" in request.POST:
            # There must be some data-checking
            pid = request.POST["new_pid"]
            user = User.objects.filter(username=request.user.username)[0]
            cp = ConnectedPublic(user=user, pid=pid)
            cp.save()
            return redirect('/')
        if "delete_public" in request.POST:
            # You must complete this
            msg = 'Delete button was pushed with value - %s' % request.POST["delete_public"]
            return render(request, 'postmaker/info_page.html', {'msg': msg})
        publics = request.POST["publics"]
        username = request.user.username
        user = User.objects.filter(username=username)[0]
        user_account = Account.objects.filter(user=user)[0]
        #user_account.publics = publics
        user_account.save()
        return render(request, 'postmaker/info_page.html', {'msg':
        'Your publics updated successfully. Or not. I do not know, actually.'})
    username = request.user.username
    user = User.objects.filter(username=username)[0]
    account = Account.objects.filter(user=user)[0]
    token = account.access_token
    #publics = account.publics
    publics = get_connected_pubs(user)
    return render(request, 'postmaker/user_account_page.html', {'username':
    username, 'token': token, 'publics': publics})

def login_view(request):
    msg = ''
    error = ''
    if request.method == 'POST':
        if "log_out" in request.POST:
            auth.logout(request)
            error = 'You are logged out.'
        else:
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user is not None and user.is_active:
                auth.login(request, user)
                msg = 'Logged in successfully.'
            else:
                msg = 'Login failure occured. Retry.'
            return redirect(LINK)
    return render(request, 'postmaker/login_page.html', {'msg': msg,
    'error': error, 'link': LINK})

def registration(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        email = request.POST['email']
        user = User.objects.create_user(username=username, password=password, email=email)
        user.save()
        # Registrating the Account
        user = User.objects.filter(username=username)[0]
        account = Account(user=user)
        account.save()
        msg = "Thank you for joining us, %s. Now you can login into your account." % user.get_username()
        return render(request, 'postmaker/info_page.html', {'msg': msg})
    else:
        form = RegistrationForm
        return render(request, 'postmaker/registration_page.html', {'form': form})

def make_post(post, gid):
    save_photo = {'url': 'https://api.vk.com/method/photos.copy?',
    'data': {'access_token': token, 'v': 3, 'owner_id': post['owner_id'], 'photo_id': post['photo_id']}}
    saved_id = posting(save_photo['url'], save_photo['data'])['response']
    likes_indic = post['likes']
    reposts_indic = post['reposts']
    msg = post['text']
    link = 'photo78767814_' + str(saved_id)

    postt = {'url': 'https://api.vk.com/method/wall.post?',
    'data': {'access_token': token, 'v': 3, 'owner_id': -gid, 'message': msg, 'attachments': link,'from_group': 1,}}
    return posting(postt['url'], postt['data'])

def get_connected_pubs(user):
    # The following line returns list of CP objects, so you must make additional opening, like this: publist[0].pid
    publist = ConnectedPublic.objects.filter(user=user)
    pubdict = {}
    for pub in publist:
        time.sleep(0.3)
        name_data = {'url': 'https://api.vk.com/method/groups.getById?',
        'data': {'access_token': token, 'v': 5.73, 'group_id': pub.pid}}
        pubdict[pub.pid] = posting(name_data['url'], name_data['data'])['response'][0]['name']
    return pubdict

def get_posts():
    return postgetter.sl

def postmaker(request):
    response = ''
    post_list = get_posts()
    page = 1
    if request.method == 'POST':
        page = int(request.POST["page"])
        if request.POST.get('direct'):
            direct = request.POST["direct"]
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
        if "make_post" in request.POST:
            gid = request.POST["make_post"]
            post_data = post_list[page]
            response = make_post(post_data, int(gid))
    link = post_list[page]['full_link']
    if post_list[page]['text'] == '':
        text = 'Sample text.'
    else:
        text = post_list[page]['text']
    if request.user.is_authenticated:
        user = User.objects.filter(username=request.user.username)[0]
        pubdict = get_connected_pubs(user)

    else:
        msg = 'You are not authenticated! Please, log in.'
        return render(request, 'postmaker/info_page.html', {'msg': msg})
    return render(request, 'postmaker/postmaker.html', {'request': request,
    'link': link, 'text': text, 'page': page, 'response': response,
    'pubdict': pubdict, 'slug': 'postmaker'})
