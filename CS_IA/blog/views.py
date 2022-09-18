from django.shortcuts import render
from . import views
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
    return render(request, 'blog/index.html')

CHOICES = [
    ('0','0-8'),
    ('1','9-16'),
    ('2','17-24'),
    ('3','24-35'),
    ('4','36+')
]

class SignUpForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password")
    mail = forms.EmailField(label="Mail")
    age_group = forms.ChoiceField(widget=forms.Select, choices=CHOICES)


def signup(request):
    if request.method == "POST":

            # Take in the data the user submitted and save it as form
            form = SignUpForm(request.POST)

            # Check if form data is valid (server-side)
            if form.is_valid():

                # Isolate the task from the 'cleaned' version of form data
                form = form.cleaned_data

                # Add the new task to our list of tasks
                submission = form.save

                # Redirect user to list of tasks
                return HttpResponseRedirect(reverse("contribute:index"))

            else:
                # If the form is invalid, re-render the page with existing information.
                return render(request, "blog/signup.html", {
                    "form": form
                })
    form = SignUpForm()
    return render(request, "blog/signup.html", {
        "form": form
    })