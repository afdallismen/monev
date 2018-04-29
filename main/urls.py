from django.urls import path

from main import views

app_name = "main"
urlpatterns = [
    path(
        'questionnaire/',
        views.questionnaire_index,
        name='questionnaire_index',
    ),
    path(
        'questionnaire/<int:pk>',
        views.questionnaire_detail,
        name='questionnaire_detail',
    ),
]
