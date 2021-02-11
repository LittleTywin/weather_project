from django.shortcuts import render,reverse
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required



def register_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('weather:home'))
    if request.method == 'POST':
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user = form.save()
            # Log the user in and then redirect to home page.
            authenticated_user = authenticate(username=new_user.username,
            password=request.POST['password1'])
            login(request, authenticated_user)
            
            try:
                next = request.GET['next']
                return HttpResponseRedirect(next)
            except :
                return HttpResponseRedirect(reverse('weather:home'))
            
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form':form})
