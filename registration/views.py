import json
from django.http.response import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect, HttpResponseRedirectBase
from django.shortcuts import redirect, render
from .models import User

from django.contrib.auth import (
    authenticate,
    login,
    logout
)

from .forms import UserSignupForm, UserLoginForm

# Create your views here.


def signupFunc(request, type):
    form = UserSignupForm(request.POST or None)

    if request.is_ajax():
        if form.is_valid():
            user = form.save(commit=False)

            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user.set_password(password)
            user.save()

            data = User(user=user, userType=type)
            data.save()

            newUser = authenticate(username=user.username, password=password)
            login(request, newUser)

        else:
            data = json.dumps(
                {'errors': [value for key, value in form.errors.items()]}
            )
            return HttpResponseBadRequest(data)

        redirectTo = '/profile/' + type + '/' + username + '/'

        return HttpResponse(content=redirectTo)

    context = {
        'prevPageLink': ('/' + type + '/'),
        'form': form
    }

    if type == 'admin':
        return render(request, 'registration/adminSignup.html', context)
    elif type == 'student':
        return render(request, 'registration/studentSignup.html', context)


def loginFunc(request, type):
    form = UserLoginForm(request.POST or None, initial={'userType': type})

    if form.is_valid():
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')

        user = authenticate(username=username, password=password)

        login(request, user)
        return redirect('/profile/' + type + '/' + username + '/')

    context = {
        'prevPageLink': ('/' + type + '/'),
        'form': form
    }

    if type == 'admin':
        return render(request, 'registration/adminLogin.html', context)
    elif type == 'student':
        return render(request, 'registration/studentLogin.html', context)


def signupAdmin(request):
    return signupFunc(request, 'admin')


def loginAdmin(request):
    return loginFunc(request, 'admin')


def signupStudent(request):
    return signupFunc(request, 'student')


def loginStudent(request):
    return loginFunc(request, 'student')


def userLogout(request):
    logout(request)
    return redirect('/')
