from django.shortcuts import render
# from django.http import HttpResponse
from basic_app.forms import UserForm, UserProfileInfoForm

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth import authenticate, login, logout



# Create your views here.
def index(request):
    return render(request, 'basic_app/index.html')

def register(request):

    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save() # Save directly to the database
            user.set_password(user.password)    # hash the password
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user # populates the one-to-one relationship

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            registered = True
        else:   # if one or other of the forms are not
            print(user_form.errors, profile_form.errors)

    else:   # not a post
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'basic_app/registration.html',
            context={'user_form':user_form,
            'profile_form':profile_form,
            'registered':registered})

def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('index'))
            else: # account not is_active
                return HttpResponse("Account is not active")
        else: # account not recognised
            print("Someone tried to login and failed!")
            print("Username: {} and Password: {}", format(username, password))
            return HttpResponse("Invalid Login details supplied")

    else: # not a post
        return render(request, 'basic_app/login.html', {}) # empty context

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def special(request):
    return HttpResponse("You are logged in. Nice!")
