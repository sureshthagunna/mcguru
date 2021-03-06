from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.shortcuts import render, redirect, get_object_or_404
from questions.models import Info, Question

def get_correct_answer(question):
    if question.answer == "a":
        answer = question.opt_a
    elif question.answer == "b":
        answer = question.opt_b
    elif question.answer== "c":
        answer = question.opt_c
    elif question.answer == "d":
        answer = question.opt_d
    elif question.answer == "e":
        answer = question.opt_e
    elif question.answer == "f":
        answer = question.opt_f

    return answer

def answer(request):
    template = "answers/answer.html"

    info = get_object_or_404(Info, identifier=1)
    category = request.path_info.replace("/", "").replace("answer", "")
    if category == "":
        category = "computer_misc"

    if 'last_answered_' + category not in request.session:
        category_last_answered = request.session['last_answered_' + category] = 0
    else:
        category_last_answered = request.session['last_answered_' + category]

    if category_last_answered == 0:
        try:
            question = Question.objects.get(category=category, question_num=1)
        except Question.DoesNotExist:
            print(
                "=====================++++++++++++++++=================="
            )
            print("Question number 1 does not exist for some reason fix it")
            print(
                "=====================++++++++++++++++=================="
            )
            raise
    else:
        try:
            question = Question.objects.get(
                question_num = category_last_answered + 1, category=category
            )

        except MultipleObjectsReturned:
            print(
                "=====================++++++++++++++++=================="
            )
            print(
                "There is more than one question with question number {} in the {} category fix it.".format(
                    category_last_answered + 1, category
                )
            )
            print(
                "=====================++++++++++++++++=================="
            )
            raise

        except ObjectDoesNotExist:
            messages.success(
                request, "Congratulations all questions are done in this category."
            )
            request.session['last_answered_'+category] = 0
            return redirect("about")

    if request.method == "POST":

        if 'jump' in request.POST:
            jump = int(request.POST["jump"])-1
        else:
            answered_num = request.POST["answer"].lower()
            if answered_num == "1":
                answered_num = "a"
            if answered_num == "2":
                answered_num = "b"
            if answered_num == "3":
                answered_num = "c"
            if answered_num == "4":
                answered_num = "d"
            if answered_num == "5":
                answered_num = "e"
            if answered_num == "6":
                answered_num = "f"

            answer = get_correct_answer(question)

            if answered_num == question.answer:
                messages.success(
                    request,
                    "Congratulations, correct answer is {}: {}.".format(
                        answered_num, answer
                    ),
                )
            else:
                messages.warning(
                    request,
                    "The correct answer was {} : {}. but you selected {}. Good luck for this one.".format(
                        question.answer,answer, answered_num
                    ),
                )

        if 'jump' in locals():
            request.session["last_answered_" + category] = jump
        else:
            request.session["last_answered_" + category] = question.question_num
        return redirect("answers:" + category)
    total_questions = getattr(info, "total_questions_"+category)
    total_questions_total = info.total_questions

    context = {"title": "answer", "question": question, "total_questions": total_questions, "total_questions_total": total_questions_total}

    return render(request, template, context)
