from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import userForm
from django.contrib import messages


from website import utils
from website.models import User
from website.send_mail import send_mail


def login(request):
    return render(request, "website/login1.html")


def app_signup_view(request):
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
                    if 'otp' not in request.POST:
                        otp = utils.generateOTP()
                        message = "Please use the One Time Password " + otp + " to create your account on IMaaS."
                        subject = "Signup Request"
                        email = username + '@vmware.com'
                        send_mail(subject, message, email)
                        context = {
                            'username': username,
                            'password': password,
                            'confirmpassword': confirmpassword,
                            'otp': True
                        }
                        try:
                            userInstance = User.objects.get(username=('temp-' + username))
                            userInstance.password = otp
                            userInstance.save()
                        except:
                            userInstance = User(username=('temp-' + username), password=otp, email=email)
                            userInstance.save()
                        messages.add_message(request, messages.ERROR, 'OTP sent to your email address.')
                        return render(request, 'website/signup.html', context)


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
