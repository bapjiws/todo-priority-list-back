# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers import serialize

import json

from .models import Todo

# Create your views here.
def index(request):
    return HttpResponse("Hi! You're at the API app index. Welcome!")

def loadTodos(request):
    if request.method == "GET":
        return HttpResponse(serialize('json', Todo.objects.order_by('-priority')))

@csrf_exempt # probably better to add localhost to CSRF_TRUSTED_ORIGINS
def addTodo(request):
    if request.method == "POST":
        payload = json.loads(request.body)
        todo = Todo.objects.create(
            priority=payload['priority'],
            name=unicode(payload['name']),
            description=payload['description']
        )
        todo.save()
        return HttpResponse(request.body)

def dropTodos(request):
    if request.method == "GET":
        Todo.objects.all().delete()
        return HttpResponse("DROPPED EVERYTHING!")