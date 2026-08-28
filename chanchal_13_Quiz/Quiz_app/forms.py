from django.contrib.auth.forms import UserCreationForm
from Quiz_app.models import *
from django import forms

class RegisterForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'email', 'password1', 'password2']


class ParticipantForm(forms.ModelForm):
    class Meta:
        model = ParticipantModel
        fields = '__all__'
        exclude = ['user']


class QuizForm(forms.ModelForm):
    class Meta:
        model = QuizModel
        fields = '__all__'


class QuestionForm(forms.ModelForm):
    class Meta:
        model = QuestionModel
        fields = ['question']


class OptionForm(forms.ModelForm):
    class Meta:
        model = OptionModel
        fields = ['option', 'is_correct']