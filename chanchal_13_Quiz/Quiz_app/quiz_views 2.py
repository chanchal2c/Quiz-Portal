from django.shortcuts import render, redirect, get_object_or_404
from Quiz_app.forms import *
from Quiz_app.models import *


# Create your views here.

def add_quiz_view(request):

    form = QuizForm()

    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save()
            return redirect('add_question_view', quiz_id=quiz.id)
    
    context = {
        'form': form,
        'title': 'Add a Quiz ',
        'btn': ' Add Quiz'
    }
    return render(request, 'base_form.html', context)


def add_question_view(request, quiz_id):

    quiz_data = QuizModel.objects.get(id=quiz_id)

    form = QuestionForm()

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz_data
            question.save()
            return redirect('add_option_view', ques_id=question.id, quiz_id=quiz_id)
        
    context = {
        'form': form,
        'title': 'Add a Question ',
        'btn': ' Add '
    }
    return render(request, 'base_form.html', context)



def add_option_view(request, ques_id, quiz_id):

    question_data = QuestionModel.objects.get(id=ques_id)
    option_count = OptionModel.objects.filter(question=question_data).count()

    if option_count >= 4:
        return redirect('quiz_questions', quiz_id)

    form = OptionForm()

    if request.method == 'POST':
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question_data
            option.save()
            return redirect('add_option_view', ques_id, quiz_id)


    context = {
        'form': form,
        'title': 'Add a Option ',
        'btn': ' Add ',
    }
    return render(request, 'base_form.html', context)



def quiz_list_view(request):

    quiz_list = QuizModel.objects.all()

    context = {
        'quiz_list': quiz_list
    }

    return render(request, 'quiz_list.html', context)


def quiz_questions(request, quiz_id):
    quiz = get_object_or_404(QuizModel.objects.prefetch_related('questions__options'), pk=quiz_id)
    return render(request, 'quiz_questions.html', {'quiz': quiz})


def delete_question_view(request, ques_id, quiz_id):

    question_data = QuestionModel.objects.get(id=ques_id)

    question_data.delete()

    return redirect('quiz_questions', quiz_id)


def delete_option_view(request, opt_id, quiz_id):

    option_data = OptionModel.objects.get(id=opt_id)

    option_data.delete()

    return redirect('quiz_questions', quiz_id)


def edit_question_view(request, ques_id, quiz_id):

    question_data = QuestionModel.objects.get(id=ques_id)

    form = QuestionForm(instance=question_data)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question_data)
        if form.is_valid():
            form.save()
            return redirect('quiz_questions', quiz_id)
        
    context = {
        'form': form,
        'title': 'Edit Question ',
        'btn': ' Edit '
    }
    return render(request, 'base_form.html', context)



def edit_option_view(request, opt_id, quiz_id):

    option_data = OptionModel.objects.get(id=opt_id)

    form = OptionForm(instance=option_data)

    if request.method == 'POST':
        form = OptionForm(request.POST, instance=option_data)
        if form.is_valid():
            form.save()
            return redirect('quiz_questions', quiz_id)


    context = {
        'form': form,
        'title': 'Edit a Option ',
        'btn': ' Edit ',
    }
    return render(request, 'base_form.html', context)


def take_quiz_view(request, quiz_id):

    quiz = get_object_or_404(QuizModel, id=quiz_id)
    questions = quiz.questions.prefetch_related('options')

    questions = quiz.questions.order_by('?')

    # Randomize options
    for question in questions:
        question.random_options = question.options.order_by('?')

    if request.method == 'POST':
        score = 0

        for question in questions:
            selected_option_id = request.POST.get(f'question_{question.id}')
            if selected_option_id:
                selected_option = get_object_or_404(OptionModel, id=selected_option_id)
                if selected_option.is_correct:
                        score += 1

        participant = get_object_or_404(ParticipantModel, user=request.user)
        total_questions = questions.count()

        QuizResult.objects.update_or_create(
            participant=participant,
            quiz=quiz,
            defaults={'score': score, 'total_questions': total_questions},
        )
        return redirect('quiz_result_view', quiz_id=quiz.id)

    

    return render(request, 'take_quiz.html', {'quiz': quiz, 'questions': questions})


def quiz_result_view(request, quiz_id):

    participant = get_object_or_404(ParticipantModel, user=request.user)
    quiz = get_object_or_404(QuizModel, id=quiz_id)
    result = get_object_or_404(QuizResult, participant=participant, quiz=quiz)

    return render(request, 'quiz_result.html', {
        'quiz': quiz,
        'result': result,
        'participant': participant,
    })



def quiz_attempt_view(request):

    participant = get_object_or_404(ParticipantModel, user=request.user)

    quiz_data = QuizResult.objects.filter(participant=participant)

    context = {
        'quiz_data':quiz_data
    }

    return render(request, 'quiz_attempt.html', context)

