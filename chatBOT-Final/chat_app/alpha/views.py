

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse

from django.shortcuts import render, redirect

from passlib.handlers.pbkdf2 import pbkdf2_sha256
from django.contrib import messages

from .forms import userForm
from .models import User
from passlib.utils import pbkdf2
from chatbot import Chat,MultiFunctionCall
import requests, os
from django.views.decorators.csrf import csrf_exempt
from nltk.chat.util import reflections

from django.contrib import messages



# from .models import Conversation


def whoIs(query, sessionID="general"):
    if query[-2] == '?':
        query = query[:len(query) - 2]
    try:
        response = requests.get('http://api.stackexchange.com/2.2/tags/' + query + '/wikis?site=stackoverflow')
        data = response.json()
        return data['items'][0]['excerpt']
    except:
        pass
    return "Oh, You misspelled somewhere!"


def results(query, sessionID="general"):
    query_list = query.split(' ')
    query_list = [x for x in query_list if
                  x not in ['posted', 'questions', 'recently', 'recent', 'display', '', 'in', 'of', 'show']]
    # print(query_list)
    if len(query_list) == 1:
        # print('con 1')
        try:
            response = requests.get(
                'https://api.stackexchange.com/2.2/questions?pagesize=5&order=desc&sort=activity&tagged=' + query_list[
                    0] + '&site=stackoverflow')
            data = response.json()
            data_list = [str(i + 1) + '. ' + data['items'][i]['title'] for i in range(5)]
            return '<br/>'.join(data_list)
        except:
            pass
    elif len(query_list) == 2 and 'unanswered' not in query_list:
        # print('con 2')
        query_list = sorted(query_list)
        n = query_list[0]
        tag = query_list[1]
        try:
            response = requests.get(
                'https://api.stackexchange.com/2.2/questions?pagesize=' + n + '&order=desc&sort=activity&tagged=' + tag + '&site=stackoverflow')
            data = response.json()
            data_list = [str(i + 1) + '. ' + data['items'][i]['title'] for i in range(int(n))]
            return '<br/>'.join(data_list)
        except:
            pass

    else:
        # print('con 3')
        query_list = [x for x in query_list if
                      x not in ['which', 'where', 'whos', 'who\'s' 'is', 'are', 'answered', 'not', 'unanswered', 'for']]
        # print(query_list)
        if len(query_list) == 1:
            try:
                response = requests.get(
                    'https://api.stackexchange.com/2.2/questions/no-answers?pagesize=5&order=desc&sort=activity&tagged=' +
                    query_list[0] + '&site=stackoverflow')
                data = response.json()
                data_list = [str(i + 1) + '. ' + data['items'][i]['title'] for i in range(5)]
                return '<br/>'.join(data_list)
            except:
                pass
        elif len(query_list) == 2:
            query_list = sorted(query_list)
            n = query_list[0]
            tag = query_list[1]
            try:
                response = requests.get(
                    'https://api.stackexchange.com/2.2/questions/no-answers?pagesize=' + n + '&order=desc&sort=activity&tagged=' + tag + '&site=stackoverflow')
                data = response.json()
                data_list = [str(i + 1) + '. ' + data['items'][i]['title'] for i in range(int(n))]

                return '<br/>'.join(data_list)
            except:
                pass
    return "Oh, You misspelled somewhere!"


# Display recent 3 python questions which are not answered
firstQuestion = "Hi, How may i help you?"

call = MultiFunctionCall({"whoIs": whoIs,
                                  "results": results})

chat = Chat(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 "chatbotTemplate",
                                 "Example.template"
                                 ),
                    reflections, call=call)


def Home(request):
    return render(request, "alpha/home.html", {'home': 'active', 'chat': 'chat'})


# return render(request, "alpha/login1.html", {'home': 'active', 'chat': 'chat'})

def login_view(request):
    # if utils.is_authenticated(request):
    # return render(request, 'website/message.html')

    if request.method == 'POST':
        form = userForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username').strip()
            password = form.cleaned_data.get('password')
            try:
                u = User.objects.get(username=username)
                # if pbkdf2_sha256.verify(password, u.password):
                if password == u.password:
                    # request.session['userid'] = u.username

                    # return render(request, 'website/message.html')
                    return render(request, 'alpha/home.html')
                else:
                    messages.add_message(request, messages.ERROR, 'Invalid username or password')
                    return redirect('login')
            except User.DoesNotExist:
                # messages.add_message(request, messages.ERROR, "User doesn't exist. Please create an account first.")
                messages.error(request, messages.INFO, "User doesn't exist. Please create an account first.")
                return redirect('login')
        else:
            messages.add_message(request, messages.ERROR, 'Invalid username or password')
            return redirect('login')
    else:
        form = userForm()
        # print(request.user)
        return render(request, 'alpha/login1.html', {'form': form})


def signup_view(request):
    if request.method == 'POST':
        if not request.POST['password'] or not request.POST['username']:
            messages.add_message(request, messages.ERROR, 'Please provide a username/password')
            return render(request, 'alpha/signup.html')
        elif not request.POST['confirmpassword']:
            messages.add_message(request, messages.ERROR, 'Please enter confirm password')
            return render(request, 'alpha/signup.html', {'username': request.POST['username'],
                                                         'password': request.POST['password']})

        form = userForm(request.POST)

        if form.is_valid():
            try:
                username = form.cleaned_data['username']
                # print(username)
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
                    # print(hash)
                    form.password = hash
                    # print(form.password)
                    form.save()
                else:
                    messages.add_message(request, messages.ERROR, "Password mismatch.")
                    context = {
                        'username': username,
                        'password': password
                    }
                    return render(request, 'alpha/signup.html', context)
            return redirect('/')
        else:
            messages.add_message(request, messages.ERROR, '')
            print(form.errors)

    else:
        return render(request, 'alpha/signup.html')


@csrf_exempt
def Post(request):
    while len(chat.conversation["general"]) < 2:
        chat.conversation["general"].append('initiate')
    if request.method == "POST":
        query = request.POST.get('msgbox', None)
        response = chat.respond(query)
        chat.conversation["general"].append('<br/>'.join(['ME: ' + query, 'BOT: ' + response]))
        if query.lower() in ['bye', 'quit', 'bbye', 'seeya', 'goodbye']:
            chat_saved = chat.conversation["general"][2:]
            response = response + '<br/>' + '<h3>Chat Summary:</h3><br/>' + '<br/><br/>'.join(chat_saved)
            chat.conversation["general"] = []
            return JsonResponse({'response': response, 'query': query})
        # c = Conversation(query=query, response=response)
        return JsonResponse({'response': response, 'query': query})
    else:
        return HttpResponse('Request must be POST.')


'''
def Post(request):
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        c = Chat(message=msg)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': 'user'})
    else:
        return HttpResponse('Request must be POST.')'''
