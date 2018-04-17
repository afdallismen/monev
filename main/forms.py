from django import forms

from main.models import Diklat


class DiklatForm(forms.ModelForm):
    class Meta:
        model = Diklat
        fields = '__all__'
        widgets = {
            'regency': forms.CheckboxSelectMultiple()
        }
