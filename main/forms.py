from django import forms

from main.models import Question


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'
        widgets = {
            'text': forms.Textarea(attrs={'rows': 1})
        }
