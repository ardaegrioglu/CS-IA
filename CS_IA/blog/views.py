from enum import auto
from django.shortcuts import render
from . import views
from django.contrib.auth.forms import UserCreationForm
from django.views import generic
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from blog.models import User, Agegroup, Article, History, Genres, Favorite
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO
import base64

class homeblog:
    def __init__(self, headline, content, id):
        self.headline = headline
        self.content = content
        self.id = id
        

class articlesingle(homeblog):
    def __init__ (self, headline, content, id, genre):
        homeblog.__init__(self, headline, content, id)
        self.genre = genre
    #article single diye bir method aç, constructor yaz, initial parameterlar verirse onlara göre vermezse default çıkar
    


# Function to find the partition position
def partition(array, low, high):

	# choose the rightmost element as pivot
	pivot = array[high]

	# pointer for greater element
	i = low - 1

	# traverse through all elements
	# compare each element with pivot
	for j in range(low, high):
		if array[j].id <= pivot.id:

			# If element smaller than pivot is found
			# swap it with the greater element pointed by i
			i = i + 1

			# Swapping element at i with element at j
			(array[i], array[j]) = (array[j], array[i])

	# Swap the pivot element with the greater element specified by i
	(array[i + 1], array[high]) = (array[high], array[i + 1])

	# Return the position from where partition is done
	return i + 1

# function to perform quicksort


def quickSort(array, low, high):
	if low < high:

		# Find pivot element such that
		# element smaller than pivot are on the left
		# element greater than pivot are on the right
		pi = partition(array, low, high)

		# Recursive call on the left of pivot
		quickSort(array, low, pi - 1)

		# Recursive call on the right of pivot
		quickSort(array, pi + 1, high)


    
def index(request):
    blog_list = []
    Blogs = list(Article.objects.values())
    for blog in Blogs:
        blog_list.append(homeblog(blog["headline"], f'{blog["content"][0:10]}...', blog["id"]))
    try:
        username = request.session['username']
    except:
        username = "Visitor"
        pass
    quickSort(blog_list, 0, len(blog_list) - 1)

    return render(request, 'blog/index.html', {
        "blog_list": blog_list,
        "username": username
    })

CHOICES = [
    ('1','0-8'),
    ('2','9-16'),
    ('3','17-24'),
    ('4','25-36'),
    ('5','36+')
]


class SignUpForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password")
    age_group = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    mail = forms.EmailField(label="Mail")


class LoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(label="Password")

class ArticleForm(forms.Form):
    headline = forms.CharField(label="Headline")
    content = forms.CharField(label="Content")
    genre = forms.CharField(label="Genre")


def signup(request):
    if request.method == "POST":

            # Take in the data the user submitted and save it as form
            form = SignUpForm(request.POST)

            # Check if form data is valid (server-side)
            if form.is_valid():

                # Isolate the task from the 'cleaned' version of form data
                form = form.cleaned_data
                save = User(username=form['username'], password=form['password'], age_group=Agegroup.objects.get(id = form['age_group']), mail=form['mail'])

                # Add the new task to our list of tasks
                save.save()

                # Redirect user to list of tasks
                return HttpResponseRedirect(reverse("login"))

            else:
                # If the form is invalid, re-render the page with existing information.
                return render(request, "blog/signup.html", {
                    "form": form
                })
    form = SignUpForm()
    return render(request, "blog/signup.html", {
        "form": form
    })

def login(request):
    if request.method == "POST":

            # Take in the data the user submitted and save it as form
            form = LoginForm(request.POST)
            post = request.POST
            querry = User.objects.filter(username = post['username'], password = post['password'])
            # Check if form data is valid (server-side)
            if querry.exists():

                request.session['username'] = post['username']
                request.session['agegroup'] = list(querry.values())[0]['age_group_id']
                return HttpResponseRedirect(reverse("index"))

            else:
                # If the form is invalid, re-render the page with existing information.
                return render(request, "blog/login.html", {
                    "form": form
                })
    form = LoginForm()

    return render(request, "blog/login.html", { 
        "form": form
    })

# Python 3 program for recursive binary search.
# Modifications needed for the older Python 2 are found in comments.

# Returns index of x in arr if present, else -1
def binary_search(arr, low, high, x):

	# Check base case
	if high >= low:

		mid = (high + low) // 2

		# If element is present at the middle itself
		if arr[mid].id == x:
			return mid

		# If element is smaller than mid, then it can only
		# be present in left subarray
		elif arr[mid].id > x:
			return binary_search(arr, low, mid - 1, x)

		# Else the element can only be present in right subarray
		else:
			return binary_search(arr, mid + 1, high, x)

	else:
		# Element is not present in the array
		return -1



def article(request, id):
    blog_list = []
    Blogs = list(Article.objects.values())
    for blog in Blogs:
        blog_list.append(articlesingle(blog["headline"], blog["content"], blog["id"], blog["genre_id"]))
    num = binary_search(blog_list, 0, len(blog_list)-1, id)
    save = History(user = User.objects.get(username = request.session['username']), article = Article.objects.get(id = id), genre = Genres.objects.get(id = blog_list[num].genre), age_group = Agegroup.objects.get(id = request.session['agegroup']), date_read = datetime.now())
    save.save()
    return render(request, "blog/article.html", {
        "blog": blog_list[num]
    })

def history(request):
    history_list = []
    user = request.session['username']
    user_data = (list(User.objects.filter(username = user).values()))[0]["id"]
    querry = list((History.objects.filter(user_id = user_data).values().distinct("article_id")))
    for history in querry:
        blog = list(Article.objects.filter(id = (querry)[0]['article_id']).values())
        history_list.append(homeblog(blog[0]["headline"], f'{blog[0]["content"][0:10]}...', blog[0]["id"]))
    return render(request, "blog/history.html", {
        "history": history_list
    })

def favoriteapi(request, id):
    username = request.session['username']
    querry = Favorite.objects.filter(user = User.objects.get(username = username), article = Article.objects.get(id = id))
    if querry.exists():
        return HttpResponseRedirect(reverse("index"))
    else:
        save = Favorite(user = User.objects.get(username = username), article = Article.objects.get(id = id))
        save.save()
        return HttpResponseRedirect(reverse("index"))


def unfavoriteapi(request, id):
    username = request.session['username']
    querry = Favorite.objects.filter(user = User.objects.get(username = username), article = Article.objects.get(id = id))
    if querry.exists():
        querry.delete()
        return HttpResponseRedirect(reverse("index"))
    else:
        return HttpResponseRedirect(reverse("index"))


def favorite(request):
    favorite_list = []
    username = request.session['username']
    querry = list(Favorite.objects.filter(user = User.objects.get(username = username)).values())
    for favorite in querry:
        blog = (list(Article.objects.filter(id = favorite['article_id']).values()))[0]
        favorite_list.append(homeblog(blog["headline"], f'{blog["content"][0:10]}...', blog["id"]))
    return render(request, "blog/favorite.html", {
        'favorite_list': favorite_list
        })

def create(request):
    user = request.session['username']
    if request.method == "POST":

            # Take in the data the user submitted and save it as form
            form = ArticleForm(request.POST)
            
            
            if form.is_valid():
                form = form.cleaned_data
                querry = Genres.objects.filter(genre_name = form['genre'])
                if querry.exists():
                    pass
                else:
                    save = Genres(genre_name = form['genre'])
                    save.save()
                # Isolate the task from the 'cleaned' version of form data
                save = Article(headline = form['headline'], content = form['content'], genre = Genres.objects.get(genre_name = form['genre']), date_added = datetime.now())

                # Add the new task to our list of tasks
                save.save()
                return HttpResponseRedirect(reverse("create"))

            else:
                # If the form is invalid, re-render the page with existing information.
                return render(request, "blog/create.html", {
                    "form": form
                })
    form = ArticleForm()

    return render(request, "blog/create.html", { 
        "form": form,
        "username": user
    })

def delete(request):
    blog_list = []
    Blogs = list(Article.objects.values())
    for blog in Blogs:
        blog_list.append(homeblog(blog["headline"], f'{blog["content"][0:10]}...', blog["id"]))

    username = request.session['username']


    return render(request, "blog/delete.html", {
        "blog_list": blog_list,
        "username": username
    })

def deleteapi(request, id):
    querry = Article.objects.filter(id = id)
    if querry.exists():
        querry.delete()
        return HttpResponseRedirect(reverse("delete"))
    else:
        return HttpResponseRedirect(reverse("delete")) 

def edit(request):
    blog_list = []
    Blogs = list(Article.objects.values())
    for blog in Blogs:
        blog_list.append(homeblog(blog["headline"], f'{blog["content"][0:10]}...', blog["id"]))

    username = request.session['username']


    return render(request, "blog/edit.html", {
        "blog_list": blog_list,
        "username": username
    })

def editblog(request, id):
    user = request.session['username']
    if request.method == "POST":

            # Take in the data the user submitted and save it as form
                form = request.POST
            
                querry = Genres.objects.filter(genre_name = form['genre'])
                if querry.exists():
                    pass
                else:
                    save = Genres(genre_name = form['genre'])
                    save.save()
                # Isolate the task from the 'cleaned' version of form data
                article = Article.objects.get(id = id)
                article.headline = form['headline']
                article.content = form['content']
                article.genre = Genres.objects.get(genre_name = form['genre'])
                article.date_added = datetime.now()
                article.save()

                return HttpResponseRedirect(reverse("edit"))
    querry = list(Article.objects.filter(id = id).values())
    genre = Genres.objects.get(id = querry[0]['genre_id'])
    return render(request, "blog/editblog.html", { 
        "blog": querry[0],
        "user": user,
        "genre": genre,
        "username": user
    })


class queue:
    def __init__(self, list):
       self.list = list        
    def que(self, value):
        self.list.append(value)
    def deque(self):
        value = self.list[-1]
        self.list = self.list[:-1]
        return value
    def display(self):
        return self.list

def to_integer(dt_time):
    return 10000*dt_time.year + 100*dt_time.month + dt_time.day

def visualise(request):
    genre_list = []
    time_list = []
    visualise_list = []
    age_group_list = []
    querry = list(History.objects.all().values())
    user = request.session['username']
    for entry in querry:
        for key in entry:
            if (key == 'date_read' or key == 'age_group_id' or key == 'genre_id'):
                visualise_list.append(entry[key])
        visualise = queue(list = visualise_list)
    total_read = len(visualise.display())
    datetime = visualise.display()
    iter = int(total_read)/3
    for x in range(int(iter)):
        time = (visualise.deque())
        time_list.append(time)
        age_group_list.append(visualise.deque())
        genre = list(Genres.objects.filter(id = visualise.deque()).values())
        genre_list.append(genre)
        
        
        
        
        
        
        
        
    nparray = pd.DataFrame({"time":time_list, "genre":genre_list, "age_group":age_group_list, "count":total_read})
    catplot = sns.catplot(data = nparray, x="time", y="count", hue = "age_group", kind = "box")
    plot_file = BytesIO() 
    catplot.savefig(plot_file, format='png')
    encoded_file = base64.b64encode(plot_file.getValue())
    return render(request, "blog/visualise.html", {
        "totalread": total_read,
        "catplot": encoded_file,
        "username": user,
        "datetime": datetime

    })




