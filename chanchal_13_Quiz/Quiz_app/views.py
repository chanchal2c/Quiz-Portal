from django.shortcuts import render, redirect
from Quiz_app.forms import *
from django.contrib.auth.forms import AuthenticationForm
from Quiz_app.models import *
from django.contrib.auth import login, logout

# Create your views here.

def home_view(request):

    quiz_list = QuizModel.objects.all()

    context = {
        'quiz_list': quiz_list
    }

    return render(request, 'home.html', context)


def register_view(request):

    form_data = RegisterForm()

    if request.method == "POST":
        form_data = RegisterForm(request.POST)
        if form_data.is_valid():
            form_data = form_data.save()

            ParticipantModel.objects.create(user=form_data)

            return redirect('login_view')

    context = {
        'form':form_data,     
        'title':'Create an account',     
        'btn':'register',     
    }

    return render(request, 'base_form.html', context)


def login_view(request):

    form_data = AuthenticationForm()

    if request.method == "POST":
        form_data = AuthenticationForm(data=request.POST)
        if form_data.is_valid():
            user_data = form_data.get_user()

            login(request, user_data)

            return redirect('home_view')

    context = {
        'form':form_data,     
        'title':'Login your account',     
        'btn':'Login',     
    }

    return render(request, 'base_form.html', context)


def logout_view(request):

    logout(request)

    return redirect('login_view')


def profile_view(request):

    participant = ParticipantModel.objects.get(user = request.user)

    context = {
        'participant':participant
    }

    return render(request, 'profile.html', context)


def profile_update_view(request):

    participant = ParticipantModel.objects.get(user = request.user)

    form_data = ParticipantForm(instance=participant)

    if request.method == "POST":
        form_data = ParticipantForm(request.POST, instance=participant)
        if form_data.is_valid():
            form_data = form_data.save()

            return redirect('profile_view')

    context = {
        'form':form_data,     
        'title':'Update profile',     
        'btn':'update',     
    }

    return render(request, 'base_form.html', context)