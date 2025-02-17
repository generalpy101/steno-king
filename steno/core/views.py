from django.shortcuts import render, HttpResponse


# Create your views here.
def home(request):
    return render(request, "home.html")


def pricing(request):
    return HttpResponse("Pricing page, to be implemented")


def dashboard(request):
    return HttpResponse("Dashboard page, to be implemented")
