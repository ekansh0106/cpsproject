from django.shortcuts import render

def home(request):
    return render(request,'CPSapp/homepage.html')

def about (request):
    return render(request,'CPSapp/aboutme.html')
