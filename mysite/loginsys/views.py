from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm


def user_login(request):
    form = request.POST
    if form:
        username = form.get('username', '')
        password = form.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            error_message = {
                'login_error': 'Пользователь не найден'
            }
            return render(request, 'loginsys/user_login.html', error_message)
    else:
        return render(request, 'loginsys/user_login.html')

def user_logout(request):
    auth.logout(request)
    return redirect('/')


def user_new(request):
    form = request.POST
    user_form = {
        'form': UserCreationForm()
    }
    if form:
        newuser_form = UserCreationForm(form)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(
                username=newuser_form.cleaned_data['username'],
                password=newuser_form.cleaned_data['password2']
            )
            auth.login(request, newuser)
            return redirect('/')
        else:
            user_form = {
                'form': newuser_form
            }
    return render(request, 'loginsys/new_user.html', user_form)
