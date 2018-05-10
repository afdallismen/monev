from django.shortcuts import render, redirect

from account.forms import RespondentCreationForm, RespondentChangeForm
from account.models import Respondent


def register(request):
    if request.method == 'POST':
        form = RespondentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = RespondentCreationForm()
    return render(request, 'account/register.html', {'form': form})


def edit(request, username):
    respondent = Respondent.objects.get(user=request.user)
    if request.method == 'POST':
        form = RespondentChangeForm(request.POST, instance=respondent)
        if form.is_valid():
            form.save()
            return redirect('main:index')
    else:
        form = RespondentChangeForm(instance=respondent)
    return render(request, 'account/edit.html', {'form': form})
