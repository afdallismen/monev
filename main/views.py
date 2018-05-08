from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.models import Respondent
from main.models import (
    Questionnaire, Recommendation, Question, Response, Option, Measure,
    EssayResponse, ObjectiveResponse, GroupOfObjectiveResponse)


@login_required
def questionnaire_list(request):
    respondent = request.user.respondent
    responses = Response.objects.filter(respondent=respondent)
    questionnaires = Questionnaire.objects.all()

    if responses.exists():
        submitted = set(
            resp.question.topic.questionnaire.id for resp in responses)
        questionnaires = Questionnaire.objects.all().exclude(id__in=submitted)

    return render(
        request,
        'main/questionnaire_list.html',
        {'questionnaires': questionnaires},
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
        "main/questionnaire_detail.html",
        {
            'questionnaire': questionnaire,
            'topics': topics,
        }
    )


@login_required
def questionnaire_submit(request, pk):
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
        response = Response.objects.create(
            respondent=respondent,
            question=Question.objects.get(pk=pk),
            type=Question.objects.get(pk=pk).type,
        )
        EssayResponse.objects.get_or_create(
            response=response,
            text=val,
        )
    for pk, val in objectives.items():
        response = Response.objects.create(
            respondent=respondent,
            question=Question.objects.get(pk=pk),
            type=Question.objects.get(pk=pk).type,
        )
        ObjectiveResponse.objects.get_or_create(
            response=response,
            selected=Option.objects.get(pk=val),
        )
    for pk, val in groups_of_objectives.items():
        question = Measure.objects.get(pk=pk).question
        response = Response.objects.create(
            respondent=respondent,
            question=question,
            type=question.type,
        )
        GroupOfObjectiveResponse.objects.get_or_create(
            response=response,
            measure=Measure.objects.get(pk=pk),
            selected=Option.objects.get(pk=val),
        )

    return redirect('main:questionnaire_list')
