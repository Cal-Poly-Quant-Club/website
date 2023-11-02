from django.shortcuts import render

# Create your views here.

def base(request):
    return render(request, 'base/base.html')


def page1(request):
    return render(request, 'base/page1.html')

def page2(request):
    context = {}
    context['hello'] = 'Hello World!'
    return render(request, 'base/page2.html', context)