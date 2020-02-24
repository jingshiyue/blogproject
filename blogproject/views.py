from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

def about(request):
    return render (request,'common/about.html',locals())

@csrf_exempt
def contact(request):
    return render (request,'common/contact.html',locals())
