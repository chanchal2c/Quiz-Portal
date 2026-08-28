from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from Quiz_app.models import *
from Quiz_app.forms import *

# Quiz CRUD
# ........................................
@login_required
def quiz_list_view(request):

    quiz_list = QuizModel.objects.all()

    context = {
        'quiz_list': quiz_list
    }

    return render(request, 'quiz_list.html', context)

@login_required
def quiz_create_view(request):

    form = QuizForm()

    if request.method == "POST":
        form = QuizForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('quiz_list_view')

    context = {
        'form': form,
        'title': 'Add a Quiz ',
        'btn': ' Add'
    }
    return render(request, 'base_form.html', context)


@login_required
def quiz_edit_view(request, quiz_id):

    quiz_data = get_object_or_404(QuizModel, id=quiz_id)

    form = QuizForm(instance=quiz_data)

    if request.method == "POST":
        form = QuizForm(request.POST, instance=quiz_data)
        if form.is_valid():
            form.save()
            return redirect('quiz_list_view')

    context = {
        'form': form,
        'title': 'Edit a Quiz ',
        'btn': ' Edit'
    }
    return render(request, 'base_form.html', context)


@login_required
def quiz_delete_view(request, quiz_id):

    quiz_data = get_object_or_404(QuizModel, id=quiz_id)
    quiz_data.delete()

    return redirect('quiz_list_view')



# Question CRUD
# ........................................

@login_required
def question_list_view(request, quiz_id):

    quiz_data = get_object_or_404(QuizModel, id=quiz_id)

    question_data = QuestionModel.objects.filter(quiz=quiz_data)

    return render(request, 'question_list.html', {
        'quiz_data': quiz_data,
        'question_data': question_data,
    })


@login_required
def question_add_view(request, quiz_id):

    quiz_data = get_object_or_404(QuizModel, id=quiz_id)

    form = QuestionForm()

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz_data
            question.save()

            return redirect('question_list_view', quiz_id=quiz_data.id)

    context = {
        'form': form,
        'title': 'Add a question ',
        'btn': ' Add'
    }
    return render(request, 'base_form.html', context)


@login_required
def question_edit_view(request, question_id):

    question_data = get_object_or_404(QuestionModel,id=question_id)

    form = QuestionForm(instance=question_data)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question_data)
        if form.is_valid():
            form.save()

            return redirect('question_list_view', quiz_id=question_data.quiz.id)

    context = {
        'form': form,
        'title': 'Edit question ',
        'btn': ' Edit'
    }
    return render(request, 'base_form.html', context)


@login_required
def question_delete_view(request, question_id):

    question_data = get_object_or_404(QuestionModel, id=question_id)

    question_data.delete()

    return redirect('question_list_view', quiz_id=question_data.quiz.id)



# Option CRUD
# ........................................

@login_required
def option_list_view(request, question_id):

    question_data = get_object_or_404(QuestionModel, id=question_id)

    option_data = OptionModel.objects.filter(question=question_data)

    context={
        'question_data': question_data,
        'option_data': option_data,
    }
    return render(request,'option_list.html', context)


@login_required
def option_add_view(request, question_id):

    question_data = get_object_or_404(QuestionModel, id=question_id)

    option_count = OptionModel.objects.filter(question=question_data).count()

    if option_count >= 4:
        return redirect('option_list_view', question_id=question_data.id)

    form = OptionForm()

    if request.method == "POST":
        form = OptionForm(request.POST)
        if form.is_valid():
            option = form.save(commit=False)
            option.question = question_data
            option.save()

            return redirect('option_list_view', question_id=question_data.id)

    context = {
        'form': form,
        'title': 'Add option ',
        'btn': ' Add'
    }
    return render(request, 'base_form.html', context)


@login_required
def option_edit_view(request, option_id):

    option_data = get_object_or_404(OptionModel, id=option_id)

    form = OptionForm(instance=option_data)

    if request.method == "POST":
        form = OptionForm(request.POST, instance=option_data)
        if form.is_valid():
            form.save()

            return redirect('option_list_view', question_id=option_data.question.id)

    context = {
        'form': form,
        'title': 'Edit option ',
        'btn': ' Edit'
    }
    return render(request, 'base_form.html', context)


@login_required
def option_delete_view(request, option_id):

    option_data = get_object_or_404(OptionModel, id=option_id)

    option_data.delete()

    return redirect('option_list_view', question_id=option_data.question.id)



# Quiz take and result
# ........................................
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