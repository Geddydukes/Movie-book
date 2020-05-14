from django.shortcuts import render

# Create your views here.

def home(request):
    return render(request, 'home.html')

def nav(request):
  return render(request, 'nav.html')    

