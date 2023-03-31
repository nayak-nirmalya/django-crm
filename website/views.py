from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

from .forms import SignUpForm
from .models import Record


def home(request):
    records = Record.objects.all()

    # check to see if logging in
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        # authenticate
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In.")
            return redirect("home")

        else:
            messages.success(
                request, "There Was An Error Logging In!. Please Try Again."
            )
            return redirect("home")

    else:
        return render(request, "home.html", {"records": records})


def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out.")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()

            # authenticate and login user
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]

            user = authenticate(username=username, password=password)
            login(request, user)

            messages.success(request, "You've Successfully Registerd.")

            return redirect("home")

    else:
        form = SignUpForm()
        return render(request, "register.html", {"form": form})

    return render(request, "register.html", {"form": form})


def customer_record(request, pk):
    if request.user.is_authenticated:
        # look up record
        customer_record = Record.objects.get(id=pk)
        return render(request, "record.html", {"customer_record": customer_record})
    else:
        messages.error(request, "You Must Be Logged In to View That Page!")
        return redirect("home")


def delete_record(request, pk):
    if request.user.is_authenticated:
        delet_it = Record.objects.get(id=pk)
        delet_it.delete()
        messages.success(request, "Record Deleted Successfully.")
        return redirect("home")
    else:
        messages.error(request, "You Must Be Logged In to Delete Record!")
        return redirect("home")


def add_record(request):
    return render(request, "add_record.html", {})
