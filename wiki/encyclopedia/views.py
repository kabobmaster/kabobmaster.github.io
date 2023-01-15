from django.shortcuts import render
from django.http import HttpResponse
from django import forms
from random import choice

from . import util

import markdown2

class newform(forms.Form):
    formtitle = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={"rows":"5"}), label="Markdown Content")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    list_of_entries = util.list_entries()
    if title.upper() in list_of_entries:
        new = title.upper()
    elif title.capitalize() in list_of_entries:
        new = title.capitalize()
    else:
        return HttpResponse("<h1 style=\"color:red\">Error, page not found.</h1>")

    return render(request, "encyclopedia/Entry.html", {
        "entries": markdown2.markdown(util.get_entry(new)),
        "title": new
    })

def search(request):
    if request.method == "POST":
        word = request.POST['q']
        if word.upper() in util.list_entries() or word.capitalize() in util.list_entries():
            return entry(request, word)
    allitems = []
    for i in util.list_entries():
        if i.lower().find(word.lower()) != -1:
            allitems.append(i)
    if len(allitems) == 0:
            return HttpResponse(f"<h1 style=\"color:red\">Your search for ({word}) was not found in wiki encylopedia.</h1>")
    return render(request, "encyclopedia/index.html", {
        "entries": allitems
    })

def newfile(request):
    return render(request, "encyclopedia/newfile.html", {
        "form": newform()
    })

def savepage(request):
        # Check if method is POST
    if request.method == "POST":

        # Take in the data the user submitted and save it as form
        form = newform(request.POST)
        if form.is_valid():
            title = form.cleaned_data["formtitle"]
            body = form.cleaned_data["content"]
            name = request.POST['name']
            if title in util.list_entries() and name != "edit":
                return HttpResponse("<h1 style=\"color:red\">Try a new title!</h1>")

            #save and write to md file
            file = open(f"entries/{title}.md", "w")
            file.write(f"{body}")
            file.close()

            #take to the new entry

    return render(request, "encyclopedia/Entry.html", {
        "entries": markdown2.markdown(util.get_entry(title)),
        "title": title
        })

def editpage(request):
    #check post, send page title
    #read title and body, pre-populate 
    #save writes over file, not required because should be handled by savepage fxn
    if request.method == "POST":
        title = request.POST['title']
        file = open(f"entries/{title}.md", "r")
        form = newform(initial={'formtitle': title, 'content': file.read()})
        file.close()
    return render(request, "encyclopedia/edit.html", {
        "form": form
        })

def randompage(request):
    title = util.list_entries()
    return entry(request, choice(title))