from django.shortcuts import render

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    if title.upper() == "CSS" or title.upper() == "HTML":
        new = title.upper()
    else:
        new = title.capitalize()
    
    return render(request, "encyclopedia/Entry.html", {
        "entries": markdown2.markdown(util.get_entry(new)),
        "title": new
    })
