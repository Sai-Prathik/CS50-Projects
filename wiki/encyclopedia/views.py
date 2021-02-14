from django.shortcuts import render,reverse,HttpResponseRedirect
from django.contrib import messages
from . import util
import random

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request,title):
     
    info=util.get_entry(title)
    if info:
        return  render(request,"encyclopedia/entry.html",{"title":info,"t":title})
    else:
        return render(request,"encyclopedia/filedonotexist.html",{"title":title})

def search_item(request):
    value=request.GET.get("q")
    l=[]
    if not (util.get_entry(value)) is None:
        return HttpResponseRedirect(reverse("get_entry",kwargs={"title":value}))
    else:
        for i in util.list_entries():
            if value in i:
                l.append(i)
        if len(l):
            return render(request,"encyclopedia/search-results.html",{"results":l})
        else:
            return HttpResponseRedirect(reverse("get_entry",kwargs={"title":value}))
def new_entry(request):
 if request.method=="POST":
  title=request.POST.get("Title")
  info=request.POST.get("info")
  if title in util.list_entries():
      messages.error(request,"Entry already exists")
      return HttpResponseRedirect(reverse("new_entry"))
  else:
      util.save_entry(title,info)
      return HttpResponseRedirect(reverse("get_entry",kwargs={"title":title}))
 return render(request,"encyclopedia/new_entry.html")

def get_random(request):
    n=random.randint(0,len(util.list_entries())-1)
    return HttpResponseRedirect(reverse("get_entry",kwargs={"title":util.list_entries()[n]}))


def edit(request):
    if request.method=="GET":
        t=request.GET.get("entry")
        return render(request,"encyclopedia/Edit.html",{"head":t,"info":util.get_entry(t)})
    elif request.method=="POST":
        t=request.POST.get("e_title")
        i=request.POST.get("e_info")
        util.save_entry(t,i)
        return HttpResponseRedirect(reverse("get_entry",kwargs={"title":t}))
    