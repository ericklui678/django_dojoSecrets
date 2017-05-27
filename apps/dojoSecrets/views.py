from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from .models import User, Secret, Like
from datetime import datetime, timedelta

def index(request):
    if request.session.get('id') == None:
        return render(request, 'dojoSecrets/index.html')
    else:
        secrets = Secret.objects.all().order_by('-created_at')[:10]
        now = timezone.localtime(timezone.now())
        return_list = []
        for secret in secrets:
            dt = now - secret.created_at
            return_list.append(
                (secret,
                Like.objects.filter(user_id=request.session['id'],secret=secret),
                {'days': dt.days, 'hours': dt.seconds/3600, 'minutes': (dt.seconds/60)%60})
            )
        context = {
            'secrets': return_list
        }
        return render(request, 'dojoSecrets/secrets.html', context)

def create(request):
    postData = {
        'first_name': request.POST['first_name'],
        'last_name': request.POST['last_name'],
        'email': request.POST['email'],
        'password': request.POST['password'],
        'confirm': request.POST['confirm'],
    }
    errors = User.objects.register(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['first_name']
        return redirect('/secrets')
    else:
        for error in errors:
            messages.info(request, error)
        return redirect('/')

def login(request):
    postData = {
        'email': request.POST['email'],
        'password': request.POST['password']
    }
    errors = User.objects.login(postData)
    if len(errors) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = User.objects.filter(email=postData['email'])[0].first_name
        return redirect('/secrets')
    for error in errors:
        messages.info(request, error)
    return redirect('/')

def secrets(request):
    # return query of secrets ordered by most recent first
    secrets = Secret.objects.all().order_by('-created_at')[:10]
    now = timezone.localtime(timezone.now())
    return_list = []
    # return list of tuple with (secret, whether user liked that secret, time duration)
    for secret in secrets:
        dt = now - secret.created_at
        return_list.append(
            (secret,
            Like.objects.filter(user_id=request.session['id'],secret=secret),
            {'days': dt.days, 'hours': dt.seconds/3600, 'minutes': (dt.seconds/60)%60})
        )
    context = {
        'secrets': return_list
    }
    return render(request, 'dojoSecrets/secrets.html', context)

def secret_post(request):
    secret_post = request.POST['secret_post']
    if len(secret_post) < 5:
        messages.info(request, 'Your secret must be at least 5 characters!')
    else:
        Secret.objects.create(info=secret_post, user_id=request.session['id'])
    return redirect('/secrets')

def delete(request, id, page):
    Secret.objects.get(id=id).delete()
    if page == 'recent':
        return redirect('/secrets')
    else:
        return redirect('/secrets/')

def like(request, sID, uID, page):
    # if user already liked that post, don't increment the like counter
    if Like.objects.filter(user_id=request.session.get('id'), secret_id=sID):
        if page == 'recent':
            return redirect('/secrets')
        else:
            return redirect('/secrets/')
    # Add new entry to Like table
    Like.objects.create(secret_id=sID, user_id=uID)
    # Get like count of the secret the user liked
    like_count = len(Like.objects.filter(secret_id=sID))
    # Update Secret Table's like_count column
    Secret.objects.filter(id=sID).update(like_count=like_count)
    if page == 'recent':
        return redirect('/secrets')
    else:
        return redirect('/secrets/')

def popular(request):
    secrets = Secret.objects.all().order_by('-like_count')
    now = timezone.localtime(timezone.now())
    return_list = []
    for secret in secrets:
        dt = now - secret.created_at
        return_list.append(
            (secret,
            Like.objects.filter(user_id=request.session['id'],secret=secret),
            {'days': dt.days, 'hours': dt.seconds/3600, 'minutes': (dt.seconds/60)%60})
        )
    context = {
        'secrets': return_list
    }
    return render(request,'dojoSecrets/popular.html', context)

def logoff(request):
    request.session.clear()
    return redirect('/')
