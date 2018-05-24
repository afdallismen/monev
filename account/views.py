from django.shortcuts import render, redirect

from account.forms import RespondentCreationForm, RespondentChangeForm


def signin(request):
    if request.method == 'POST':
        form = RespondentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = RespondentCreationForm()
    return render(request, 'account/signin_form.html', {'form': form})


def edit(request):
    if request.method == 'POST':
        form = RespondentChangeForm(
            request.POST,
            instance=request.user.respondent,
        )
        if form.is_valid():
            form.save()
            return redirect('main:index')
    else:
        form = RespondentChangeForm(instance=request.user.respondent)
    return render(request, 'account/profile_form.html', {'form': form})
