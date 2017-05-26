from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Secret, Like

def index(request):
    if request.session.get('name') == None:
        return render(request, 'dojoSecrets/index.html')
    else:
        context = {
            'secrets': Secret.objects.all().order_by('-created_at')[:10],
            'likes': Like.objects.all(),
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
    print request.session['id']
    print Like.objects.filter(user_id=request.session['id'])
    for like in Like.objects.all():
        print like.user.id, '-', like.secret.id
    # Secret.objects.all().delete()
    # return_list = []
    # secrets = Secret.objects.all()
    # for secret in secrets:
    #     return_list.append((secret,Like.objects.filter(user_id=request.session['id'], secret=secret)))
    # print return_list
    # print return_list
    # find all the rows with my likes
    # mylikes = Like.objects.filter(user_id=request.session['id'])
    # for like in mylikes:
    #     # find all secret posts that i liked
    #     print like.secret.id
    context = {
        'secrets': Secret.objects.all().order_by('-created_at')[:10],
        'likes': Like.objects.all(),
        'users': User.objects.all(),
    }
    return render(request, 'dojoSecrets/secrets.html', context)

def secret_post(request):
    secret_post = request.POST['secret_post']
    if len(secret_post) < 5:
        messages.info(request, 'Your secret must be at least 5 characters!')
    else:
        Secret.objects.create(info=secret_post, user_id=request.session['id'])
    return redirect('/secrets')

def delete(request, id):
    Secret.objects.get(id=id).delete()
    return redirect('/secrets')

def like(request, sID, uID):
    # if user already liked that post, don't increment the like counter
    if Like.objects.filter(user_id=request.session.get('id'), secret_id=sID):
        return redirect('/secrets')
    # Add new entry to Like table
    Like.objects.create(secret_id=sID, user_id=uID)
    # Get like count of the secret the user liked
    like_count = len(Like.objects.filter(secret_id=sID))
    # Update Secret Table's like_count column
    Secret.objects.filter(id=sID).update(like_count=like_count)

    return redirect('/secrets')

def plike(request, sID, uID):
    if Like.objects.filter(user_id=request.session.get('id'), secret_id=sID):
        return redirect('/secrets/')
    Like.objects.create(secret_id=sID, user_id=uID)
    like_count = len(Like.objects.filter(secret_id=sID))
    Secret.objects.filter(id=sID).update(like_count=like_count)
    return redirect('/secrets/')

def popular(request):
    context = {
        'secrets': Secret.objects.all().order_by('-like_count'),
        'likes': Like.objects.all(),
    }
    return render(request,'dojoSecrets/popular.html', context)

def logoff(request):
    request.session.clear()
    return redirect('/')
