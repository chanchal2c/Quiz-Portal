from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):

    phone = models.CharField(max_length=100, null=True)

def __str__(self):
    return f'{self.username}'


class ParticipantModel(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True)
    age = models.IntegerField(null=True)
    gender = models.CharField(max_length=25, null=True)
    class_level = models.CharField(max_length=50, null=True)
    institution = models.CharField(max_length=150, null=True)

    # quizzes_attempted = models.IntegerField(default=0)
    # quizzes_completed = models.IntegerField(default=0)
    # score = models.IntegerField(default=0)
    # total_score = models.IntegerField(default=0)
    # created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.name}'


class QuizModel(models.Model):

    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f'{self.title}'

    def question_count(self):
        return self.questions.count()


class QuestionModel(models.Model):
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, null=True, related_name='questions')
    question = models.CharField(max_length=100, null=True)

    def __str__(self):
        return f'{self.question}'


class OptionModel(models.Model):
    question = models.ForeignKey(QuestionModel, on_delete=models.CASCADE, null=True, related_name='options')
    option = models.CharField(max_length=100, null=True)
    is_correct = models.BooleanField(null=True)

    def __str__(self):
        return f'{self.option}'



class QuizResult(models.Model):
    participant = models.ForeignKey(ParticipantModel, on_delete=models.CASCADE, related_name='results')
    quiz = models.ForeignKey(QuizModel, on_delete=models.CASCADE, related_name='results')
    score = models.PositiveIntegerField(default=0)
    total_questions = models.PositiveIntegerField(default=0)
    submitted_at = models.DateTimeField(auto_now=True)

    # class Meta:
    #     unique_together = ('participant', 'quiz')
    #     ordering = ['-score', 'submitted_at']

    # def __str__(self):
    #     return f'{self.participant} - {self.quiz}: {self.score}/{self.total_questions}'