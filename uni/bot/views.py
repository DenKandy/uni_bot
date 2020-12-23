from django.shortcuts import render
from django.views.generic import View
from django.http import HttpResponse
from .forms import UserUniForm

# Create your views here.
class RegisterUser(View):
    NAME = "register_page"
    URL = "register/"
    URL_PATTERN  = URL + "<int:id>"
    TEMPLATE_PATH = "signup.html"
    TEMPLATE_PATH_SUCCESS = "signup_response.html"

    def __init__(self):
        pass

    def get(self, request, id):
        form = UserUniForm()
        form
        return HttpResponse(
            render(
                request, 
                self.TEMPLATE_PATH, 
                context={'form' : form, 'token' : id}))

    def post(self, request, id):
        bound_form = UserUniForm(request.POST)
        
        if bound_form.is_valid():
            user = bound_form.save(commit=False)
            bound_form.instance.is_active = True
            user.save()
            return render(
                request, 
                self.TEMPLATE_PATH_SUCCESS)
        else:
            self.error_list = bound_form.errors
            return render(request, 
                self.TEMPLATE_PATH, 
                context={'form' : form, 'token' : id,'error_list' : self.error_list})