import json

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
    selected = False
    if 'diklat' in request.GET and request.GET['diklat']:
        selected = request.GET['diklat']
        questionnaires.filter(diklat=selected)

    submitted_questions = set(
        request.user.respondent.response_set.values_list('question', flat=True)
    )
    submitted_questionnaire = Questionnaire.objects.filter(
        topic__question__in=submitted_questions
    ).distinct()
    unsubmitted_questionnaire = Questionnaire.objects.exclude(
        id__in=submitted_questionnaire
    )

    questionnaires = {
        'all': questionnaires,
        'submitted': submitted_questionnaire,
        'unsubmitted': unsubmitted_questionnaire,
    }

    ctx = {
        'diklats': diklats,
        'questionnaires': questionnaires,
        'selected': int(selected),
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

    ctx = {
        'questionnaire': questionnaire,
        'topics': topics,
    }

    print(ctx)

    return render(
        request,
        "main/questionnaire.html",
        ctx,
    )


@login_required
def questionnaire_submit(request, pk):
    respondent = Respondent.objects.get(user=request.user)
    questions = Question.objects.filter(
        topic__in=Questionnaire.objects.get(pk=pk).topic_set.all())
    responses = Response.objects.filter(
        respondent=respondent, question__in=questions)
    if responses:
        for response in responses:
            response.delete()
        recs = Recommendation.objects.filter(
            respondent=respondent, question__in=questions)
        for rec in recs:
            rec.delete()
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
            Recommendation.objects.create(
                respondent=respondent,
                question=Question.objects.get(pk=pk),
                text=val,
            )
    for pk, val in essays.items():
        response = Response.objects.create(
            respondent=respondent,
            question=Question.objects.get(pk=pk),
            type=Question.objects.get(pk=pk).type,
        )
        EssayResponse.objects.create(
            response=response,
            text=val,
        )
    for pk, val in objectives.items():
        response = Response.objects.create(
            respondent=respondent,
            question=Question.objects.get(pk=pk),
            type=Question.objects.get(pk=pk).type,
        )
        ObjectiveResponse.objects.create(
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
        GroupOfObjectiveResponse.objects.create(
            response=response,
            measure=Measure.objects.get(pk=pk),
            selected=Option.objects.get(pk=val),
        )

    return redirect('main:questionnaire_list')


def get_responses(questionnaire):
    questions = Question.objects.filter(
        topic__questionnaire=questionnaire,
        type='group_of_objective',
    )
    topics = Topic.objects.filter(question__in=questions)

    data = []
    for topic in topics:
        questions = []
        for question in topic.question_set.filter(type='group_of_objective'):
            results = []
            for measure in question.measure_set.all():
                counts = []
                for regency in questionnaire.diklat.regencies.all():
                    for option in question.option_set.all():
                        responses = Response.objects.filter(
                            respondent__regency=regency,
                            question=question,
                        )
                        counts.append(GroupOfObjectiveResponse.objects.filter(
                            response__in=responses,
                            measure=measure,
                            selected=option,
                        ).count())
                results.append({
                    'measure': measure.name,
                    'counts': counts,
                })
            questions.append({
                'regencies': list(questionnaire.diklat.regencies.values_list(
                    'name', flat=True)),
                'options': list(
                    question.option_set.values_list('name', 'code')),
                'results': results,
            })
        data.append({
            'title': topic.title,
            'questions': questions
        })
    return data


@login_required
def questionnaire_responses(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    data = get_responses(questionnaire)

    ctx = {
        'data': data
    }

    return render(request, 'main/user_responses.html', ctx)


@login_required
def questionnaire_responses_chart(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)
    data = get_responses(questionnaire)
    print(data)
    ctx = {
        'data': data,
        'json_data': json.dumps(data)
    }
    return render(request, 'main/user_responses_chart.html', ctx)
