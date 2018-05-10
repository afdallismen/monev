from django.urls import path

from main import views


app_name = "main"
urlpatterns = [
    path(
        'questionnaires/',
        views.questionnaire_list,
        name="questionnaire_list",
    ),
    path(
        'questionnaires/<int:pk>',
        views.questionnaire_detail,
        name="questionnaire_detail",
    ),
    path(
        'questionnaires/<int:pk>/responses',
        views.questionnaire_responses,
        name="questionnaire_responses",
    ),
    path(
        'questionnaires/<int:pk>/submit',
        views.questionnaire_submit,
        name="questionnaire_submit",
    ),
    path(
        '',
        views.questionnaire_list,
        name="index",
    ),
]
