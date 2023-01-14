from django.shortcuts import render
from django.http import HttpResponse

from . import util

import markdown2


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
