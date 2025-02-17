from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect
from django.views import View


class UserRegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")  # Change to the homepage URL
        return render(request, "register.html", {"form": form})


class UserLoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, "login.html", {"form": form})

    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        next_url = request.POST.get("next") or request.GET.get("next")
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # If there is a 'next' URL, redirect to it
            if next_url:
                return redirect(next_url)
            return redirect("home")  # Change to the homepage URL
        return render(request, "login.html", {"form": form})


class UserLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("home")  # Change to the homepage URL
