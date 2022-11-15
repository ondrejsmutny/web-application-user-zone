from django.shortcuts import render

def index(request):
    # Redirecting to main page
    return render(request, "index/index.html")
