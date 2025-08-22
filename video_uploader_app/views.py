from http.client import HTTPResponse
from django.shortcuts import render

def add(request):
    return HTTPResponse("Hello world!")
