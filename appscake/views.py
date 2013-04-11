from django.shortcuts import render


def home(request):
    """ Default view for the root """
    return render(request, 'base/home.html')

def about(request):
    return render(request, 'base/about.html')