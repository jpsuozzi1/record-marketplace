from django.shortcuts import render

# Create your views here.


def create(request, model):
    #Create a new object of type model

    return HttpResponse("Create a %s" % model)

def read(request, model, model_id):
    #Read model_id of type model

    return HttpResponse("Read Model: %s id %s" % model, model_id)

def update(request, model, model_id):
    #Update model_id of type model

    return HttpResponse("Update Model: %s id %s" % model, model_id)

def delete(request, model, model_id):
    #Delete model_id of type model

    return HttpResponse("Delete Model: %s id %s" % model, model_id)
    