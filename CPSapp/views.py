from django.shortcuts import render

def home(request):
    return render(request,'CPSapp/homepage.html')

def about (request):
    return render(request,'CPSapp/aboutme.html')

def disp (request):
    myweek = request.POST[ 'week' ]
    mycity = request.POST[ 'city' ]
    return render(request,'CPSapp/page2.html',{'myweek': myweek ,'mycity': mycity})