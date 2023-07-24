import json
from django.http import HttpResponse, JsonResponse, QueryDict
from django.core import serializers
from django.shortcuts import (get_object_or_404, render, HttpResponseRedirect)
from .models import MyNotes
from .forms import NotesForm
from django.views.decorators.csrf import csrf_exempt


# Create your views here.
def show_json(request):
    data = MyNotes.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

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

@csrf_exempt
def post_note(request):
    if (request.method == "POST"):
        request_data = request.body
        request_data = json.loads(request_data.decode('utf-8'))
        data = QueryDict('', mutable = True)
        data.update(request_data)
        form_req = NotesForm(data)

        if form_req.is_valid():
            form_req.save()

        return HttpResponseRedirect("/notes")

@csrf_exempt
def delete_flutter(request):
    if (request.method == "POST"):
        request_data = request.body
        pk = json.loads(request_data.decode('utf-8'))['pk']
        note = MyNotes.objects.get(id=pk)
        note.delete()
    
    return HttpResponseRedirect("/notes")

@csrf_exempt
def update_flutter(request):
    if (request.method == "PUT"):
        request_data = request.body
        pk = json.loads(request_data.decode('utf-8'))['pk']
        note = MyNotes.objects.get(id=pk)
        for key, value in request_data.items():
            setattr(note, key, value)
        note.save()
        return HttpResponseRedirect("/notes")

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