from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import FormView
from returns.io import IOResult, IOSuccess
from security.forms import RegisterForm
User = get_user_model()


class Login(LoginView):
    template_name = 'login.html'


class RegisterView(FormView):
    form_class = RegisterForm
    template_name = 'register.html'
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        print("go______________________", form)
        form.save()  # save the user
        return super().form_valid(form)

def username_check(request):
    """
        Case response
            - innerHTML: default, replace inner element
            - outerHTML: replace element
    """
    email = request.POST.get("email")
    user: User = User.objects.filter(email=email)
    if user.exists():
        return HttpResponse("Email exists") #innerHTML
    else:
        return HttpResponse("")

    # return HttpResponse(username)

def register_submit(request):

    form = RegisterForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        print("eorr:", form.errors)
    print("form______", form.data, User.objects.all())

    return HttpResponseRedirect("/login/")
