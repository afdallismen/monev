from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from account.models import Respondent
from main.models import (
    Questionnaire, Recommendation, Question, Response, Option, Measure,
    EssayResponse, ObjectiveResponse, GroupOfObjectiveResponse, Topic, Diklat)


@login_required
def questionnaire_list(request):
    questionnaires = Questionnaire.objects.filter(status='publish')
    diklats = Diklat.objects.filter(regencies=request.user.respondent.regency)
    if hasattr(request.GET, 'diklat') and request.GET.diklat:
        questionnaires.filter(diklat=request.GET.diklat)

    ctx = {
        'diklats': diklats,
        'questionnaires': questionnaires,
    }

    return render(
        request,
        'main/questionnaires.html',
        ctx,
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


@login_required
def questionnaire_responses(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)

    topics = []
    parent = questionnaire.topic_set.filter(parent=None)
    for topic in parent:
        responses = []
        for question in topic.question_set.all():
            responses.append({
                'question': question,
                'responses': Response.objects.filter(
                    question=question).order_by('-respondent')
            })

        childs = questionnaire.topic_set.filter(parent=topic)
        child_responses = []
        for topic in childs:
            resps = []
            for question in topic.question_set.all():
                resps.append({
                    'question': question,
                    'responses': Response.objects.filter(
                        question=question).order_by('respondent')
                })
            child_responses.append({
                'topic': topic,
                'responses': resps
            })

        topics.append({
            'parent': {
                'topic': topic,
                'responses': responses
            },
            'childs': child_responses,
        })

    questions = Question.objects.filter(topic__questionnaire=questionnaire)
    num_of_responses = Response.objects.filter(
            question__in=questions
        ).values('respondent').distinct().count()

    context = {
        'questionnaire': questionnaire,
        'topics': topics,
        'num_of_responses': num_of_responses
    }
    return render(request, 'result/questionnaires.html', context)
