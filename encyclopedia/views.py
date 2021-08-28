import re
import random

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.views.generic import TemplateView, ListView
from django.urls import reverse
from django import forms


import markdown2
from . import util


class NewPageForm(forms.Form):
    title = forms.CharField(label="", widget=forms.TextInput(attrs={'placeholder': 'Title'}))
    content = forms.CharField(label="", widget=forms.Textarea(attrs={'placeholder': 'Content',
    'style': 'height: 20em',
    }))
    

def index(request):
    return render(request, "encyclopedia/index.html", {
    "entries": util.list_entries()
})

def entry(request, title):
    if title in util.list_entries():
        text = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "text": text,
            "title": title
        })
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def search(request):
    query = request.GET.get('q')
    articles = util.list_entries()
    results = []
    if query in articles:
        return redirect(entry, title=query)
    else:
        for article in articles:
            if re.findall(query, article, re.IGNORECASE):
                results.append(article)
        
        return render(request, "encyclopedia/search.html", {
            "results": results,
            'query': query
        })

def randomPage(request):
    articles = util.list_entries()
    title = random.choice(articles)
    return redirect(entry, title=title)

def new_page(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if not title in util.list_entries():
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("index"))

            return HttpResponse("<h1>Entry already exists</h1>")

    return render(request, "encyclopedia/new_page.html", {
    "form": NewPageForm()
    })

def edit(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        content = request.POST.get("content")
        util.save_entry(title, content)
        text = markdown2.markdown(util.get_entry(title))
        return render(request, "encyclopedia/entry.html", {
            "text": text,
            "title": title,
        })

    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": entry
    })
