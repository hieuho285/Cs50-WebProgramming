from django.shortcuts import render, redirect

from . import util

import markdown
import random as rd


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, entry):
    if (f := util.get_entry(entry)) != None:
        html = markdown.markdown(f)
        return render(request, "encyclopedia/titles.html", {
            "title": entry,
            "body": html
        })
    return render(request, "encyclopedia/titles.html", {
        "title": "Error page",
        "body": "<h1>Requested page was not found.</h1>"
    })

def search(request):
    if request.method == "POST":
        query = request.POST['q']
        entries = util.list_entries()
        if not query:
            return redirect('index')

        if (util.get_entry(query) is not None):
            return redirect("entry", entry = query)

        else:
            titles = []
            for entry in entries:
                if query.lower() in entry.lower():
                    titles.append(entry)
            if len(titles) == 1:    
                return redirect("entry", entry = titles[0])
            elif len(titles) > 1:
                return render(request, "encyclopedia/search.html", {
                    "entries": titles
                })
            else:
                return render(request, "encyclopedia/titles.html", {
                    "title": "Search Result",
                    "body": "<h1> No matching query </h1>"
                })

def newpage(request):
    if request.method == "POST":
        title = request.POST['title']

        if util.get_entry(title) is not None:
            return render(request, "encyclopedia/error.html", {
                "tittle" : "Error",
                "body": "<h1> This title is already taken </h1>"
            })

        else:
            content = request.POST['mdcontent']
            util.save_entry(title, content)
            
            return redirect("index")

    return render(request, "encyclopedia/newpage.html")

def edit(request):
    if request.method == "POST":
        title = request.POST['entry_title']            
        return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title)
    })

def newcontent(request):
    if request.method == "POST":
        content = request.POST['content']
        title = request.POST['title']
        util.save_entry(title, content)
        return redirect("entry", entry=title)

def random(request):   
    entries = util.list_entries()
    rand_entry = rd.choice(entries)
    return redirect('entry', entry=rand_entry)

    
    
