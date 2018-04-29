from django.shortcuts import render

from main.models import Diklat, Questionnaire


def questionnaire_index(request):
    diklats = Diklat.objects.all()

    return render(
        request,
        "main/questionnaire/index.html",
        {'diklats': diklats}
    )


def questionnaire_detail(request, pk):
    questionnaire = Questionnaire.objects.get(pk=pk)

    return render(
        request,
        "main/questionnaire/detail.html",
        {'questionnaire': questionnaire}
    )
