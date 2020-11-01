from django.http import HttpResponse
from django.forms import modelform_factory
from django.shortcuts import render, redirect
from passlib.utils import pbkdf2

from .forms import userForm
from django.contrib import messages

from website import utils
from website.models import User
from website.send_mail import send_mail
from passlib.hash import pbkdf2_sha256





def signup_view(request):
    if request.method == 'POST':
        if not request.POST['password'] or not request.POST['username']:
            messages.add_message(request, messages.ERROR, 'Please provide a username/password')
            return render(request, 'website/signup.html')
        elif not request.POST['confirmpassword']:
            messages.add_message(request, messages.ERROR, 'Please enter confirm password')
            return render(request, 'website/signup.html', {'username': request.POST['username'],
                                                           'password': request.POST['password']})

        form = userForm(request.POST)

        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                userInstance = User.objects.get(username=username)
                messages.add_message(request, messages.ERROR, 'User already exists. Please login.')

            except User.DoesNotExist:
                userInstance = None

            if (userInstance == None):
                password = request.POST['password']
                confirmpassword = request.POST['confirmpassword']

                if password == confirmpassword:
                    hash = pbkdf2_sha256.hash(password)
                    pbkdf2_sha256. \
                        form = User()
                    form.username = request.POST['username']
                    form.password = hash
                    form.save()
                else:
                    messages.add_message(request, messages.ERROR, "Password mismatch.")
                    context = {
                        'username': username,
                        'password': password
                    }
                    return render(request, 'website/signup.html', context)
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, '')
            print(form.errors)

    else:
        return render(request, 'website/signup.html')


def login_view(request):
    #if utils.is_authenticated(request):
        #return render(request, 'website/message.html')

    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').strip()
            password = form.cleaned_data.get('password')
            try:
                u = User.objects.get(username=username)
                if pbkdf2_sha256.verify(password, u.password):
                    request.session['userid'] = u.username

                    return render(request, 'website/message.html')
                else:
                    messages.add_message(request, messages.ERROR, 'Invalid username or password')
                    return redirect('login')
            except User.DoesNotExist:
                messages.add_message(request, messages.ERROR, "User doesn't exist. Please create an account first.")
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')
            return redirect('login')
    else:
        form = userForm()
        print(request.user)
        return render(request, 'website/login1.html', {'form': form})
