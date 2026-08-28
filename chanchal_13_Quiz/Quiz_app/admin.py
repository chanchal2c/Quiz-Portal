from django.contrib import admin
from Quiz_app.models import *

# Register your models here.

admin.site.register([CustomUser, ParticipantModel, QuizModel, QuestionModel, OptionModel, QuizResult])