from django.shortcuts import render
from .forms import PostForm
from initial_test import Recipes

def query_chatbot(request):
    return render(request, 'query/query_chatbot.html', {})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']

            c = {'query' : query}
            return render(form, 'form/results.html', c)

def results