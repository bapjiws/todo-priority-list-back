# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.serializers.json import DjangoJSONEncoder
from django.core.serializers import serialize

import json

from .models import Todo

# Create your views here.
def index(request):
    return HttpResponse("Hi! You're at the API app index. Welcome!")

def loadTodos(request):
    if request.method == "GET":
        # resp = [];
        # for t in Todo.objects.all():
        #     print(t.description)
        #     print(t.name)
        #
        #     resp.append(json.dumps({ t.priority, t.name,t.description } ))
        resp = Todo.objects.all().values()
        # print(list(resp))
        resp_json = json.dumps(list(resp), ensure_ascii=False, default=str)
        # print(resp_json)

        # class Encoder(DjangoJSONEncoder):
        #     def default(self, o):
        #         return json.dumps(list(o), ensure_ascii=False, default=str)

        # return JsonResponse(resp_json, safe=False)
        # return HttpResponse(resp_json)
        return HttpResponse(serialize('json', Todo.objects.all()))

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