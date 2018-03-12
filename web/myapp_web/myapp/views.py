from django.shortcuts import render
from django.http import JsonResponse, HttpResponse


def home(request):

    return HttpResponse("This is the home page")

def listing(request):

    return HttpResponse("This is the listing page")
