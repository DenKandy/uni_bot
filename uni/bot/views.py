from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .forms import UserUniForm

# Create your views here.
class RegisterUser(View):
    NAME = "register_page"
    URL  = "register/"
    TEMPLATE_PATH = "signup.html"

    def __init__(self):
        pass

    def get(self, request):
        return HttpResponse(
            render(
                request, 
                self.TEMPLATE_PATH, 
                context={'from' : UserUniForm()}))