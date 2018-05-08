from django.shortcuts import render, redirect

from account.forms import RespondentCreationForm


def register(request):
    if request.method == 'POST':
        form = RespondentCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('account:login')
    else:
        form = RespondentCreationForm()
    return render(request, 'account/register.html', {'form': form})
