from django.shortcuts import render
from typing import Optional
from returns.maybe import Maybe, maybe

# Create your views here.
def home(request):

    return render(request, "home.html")
