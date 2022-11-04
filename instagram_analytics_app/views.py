from django.shortcuts import render
from instagram_analytics_app import forms


def index(request):
    return render(request, 'index.html')

