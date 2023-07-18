import json
from django.http import HttpResponse
from django.core import serializers
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from .models import MyNotes
from .forms import NotesForm

# Create your views here.
def show_json_by_id(request, id):
    data = MyNotes.objects.filter(id=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

# https://realpython.com/django-and-ajax-form-submissions/
def create_note(request):
    if request.method == 'POST':
        note_title = request.POST['note_title']
        note_text = request.POST['note_text']
        response_data = {}

        note = MyNotes(title=note_title, text=note_text)
        note.save()

        response_data['title'] = note.title
        response_data['noteid'] = note.id
        print(note_title)

        return HttpResponse(
            json.dumps(response_data),
            content_type="application/json"
        )
    else:
        return HttpResponse(
            json.dumps({"nothing to see": "this isn't happening"}),
            content_type="application/json"
        )

def create(request):
    context = {}
    
    form = NotesForm(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/notes")

    context['form'] = form
    return render(request, "create.html", context)

def read(request, id):
    context = {}

    context["data"] = MyNotes.objects.get(id=id)
    return render(request, "read.html", context)

def update(request, id):
    context = {}

    obj = get_object_or_404(MyNotes, id=id)

    form = NotesForm(request.POST or None, instance = obj)

    if form.is_valid():
        form.save()
        return HttpResponseRedirect("/notes/"+id)
    
    context["form"] = form

    return render(request, "update.html", context)

def delete(request, id):
    context = {}

    obj = get_object_or_404(MyNotes, id=id)

    if request.method == "POST":
        obj.delete()
        return HttpResponseRedirect("/notes")
    return render(request, "delete.html", context)

def index(request):
    context = {}

    context["dataset"] = MyNotes.objects.all().order_by("-id")
    
    form = NotesForm(request.POST or None)
    context["form"] = form

    return render(request, "index.html", context)