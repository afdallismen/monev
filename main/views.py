from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.models import Respondent
from main.models import (Diklat, Questionnaire, Recommendation, Question,
                         Response, Option, Measure)


@login_required
def questionnaire_index(request):
    diklats = Diklat.objects.all()

    return render(
        request,
        "main/questionnaire/index.html",
        {'diklats': diklats}
    )


@login_required
def questionnaire_detail(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    topics = []
    parent = questionnaire.topic_set.filter(parent=None)
    for topic in parent:
        childs = questionnaire.topic_set.filter(parent=topic)
        topics.append({'parent': topic, 'childs': childs})

    return render(
        request,
        "main/questionnaire/detail.html",
        {
            'questionnaire': questionnaire,
            'topics': topics,
        }
    )


@login_required
def questionnaire_submit(request, pk):
    print(Respondent.objects.all())
    respondent = Respondent.objects.get(user=request.user)
    post_data = dict(request.POST)
    del post_data['csrfmiddlewaretoken']
    recommendations = {}
    essays = {}
    objectives = {}
    groups_of_objectives = {}
    for key, val in post_data.items():
        if key.startswith('r') and val[0]:
            recommendations[key[1:]] = val[0]
        elif key.startswith('e'):
            essays[key[1:]] = val[0]
        elif key.startswith('o'):
            objectives[key[1:]] = val[0]
        elif key.startswith('g'):
            groups_of_objectives[key[1:]] = val[0]

    if recommendations:
        for pk, val in recommendations.items():
            obj, _ = Recommendation.objects.get_or_create(
                respondent=respondent,
                question=Question.objects.get(pk=pk),
            )
            obj.text = val
            obj.save()
    for pk, val in essays.items():
        obj, _ = Response.objects.get_or_create(
            respondent=respondent,
            question=Question.objects.get(pk=pk),
        )
        obj.text = val
        obj.save()
    for pk, val in objectives.items():
        obj, _ = Response.objects.get_or_create(
            respondent=respondent,
            question=Question.objects.get(pk=pk),
        )
        obj.selected = Option.objects.get(pk=val)
        obj.save()
    for pk, val in groups_of_objectives.items():
        question = Measure.objects.get(pk=pk).question
        obj, _ = Response.objects.get_or_create(
            respondent=respondent,
            question=question,
            measure=Measure.objects.get(pk=pk),
        )
        obj.selected = Option.objects.get(pk=val)
        obj.save()

    return redirect('main:questionnaire_index')
