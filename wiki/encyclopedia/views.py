from django.shortcuts import render
from django.http import HttpResponse

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    all = util.list_entries()
    if title.upper() in all:
        new = title.upper()
    elif title.capitalize() in all:
        new = title.capitalize()
    else:
        return HttpResponse("<h1 style=\"color:red\">Error, page not found.</h1>")

    return render(request, "encyclopedia/Entry.html", {
        "entries": markdown2.markdown(util.get_entry(new)),
        "title": new
    })
