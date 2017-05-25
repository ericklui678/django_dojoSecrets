from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User

def index(request):
    return render(request, 'dojoSecrets/index.html')

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
    print 'got login info'
    return redirect('/')

def secrets(request):
    context = {'users': User.objects.all().order_by('-created_at')}
    return render(request, 'dojoSecrets/secrets.html', context)
