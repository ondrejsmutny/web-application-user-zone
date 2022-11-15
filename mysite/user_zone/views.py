from django.shortcuts import render, redirect, reverse
from django.views import generic
from .models import User, GeneralData
from .forms import UserForm, LoginForm, GeneralDataForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from .tables import GeneralDataTable
from .filters import GeneralDataFilter
from django_tables2.config import RequestConfig

class UserViewRegister(generic.edit.CreateView):
    # Registration of new user
    form_class = UserForm
    model = User
    template_name = "user_zone/user_form.html"

    def get(self, request):
        # Getting blank template
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # Posting new data
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se registrovat.")
            return redirect(reverse("index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            user = form.save(commit = False)
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()
            login(request, user)
            return redirect("index")

        return render(request, self.template_name, {"form": form})

class UserViewLogin(generic.edit.CreateView):
    # Login existing user
    form_class = LoginForm
    template_name = "user_zone/user_form.html"

    def get(self, request):
        # Getting blank template
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("index"))
        else:
            form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        # Posting new data
        if request.user.is_authenticated:
            messages.info(request, "Už jsi přihlášený, nemůžeš se přihlásit znovu.")
            return redirect(reverse("index"))
        form = self.form_class(request.POST)
        if form.is_valid():
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            user = authenticate(email = email, password = password)
            if user:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Tento účet neexistuje.")
        return render(request, self.template_name, {"form": form})

def logout_user(request):
    # Logout user logged in
    if request.user.is_authenticated:
        logout(request)
    else:
        messages.info(request, "Nemůžeš se odhlásit, pokud nejsi přihlášený.")
    return redirect(reverse("login"))

class GeneralDataFilterView(SingleTableMixin, FilterView):
    # Show user list from table with lookup and filter functionality
    model = GeneralData
    table_class = GeneralDataTable
    template_name = "user_zone/general_data_list.html"
    filterset_class = GeneralDataFilter

    def get_table(self):
        # Getting table from model with is-admin authentication
        if self.request.user.is_admin:
            table_class = self.get_table_class()
            table = table_class(data=self.get_table_data())
            return RequestConfig(self.request, paginate=self.get_table_pagination(table)).configure(
                table
            )
        else:
            raise ValueError("Na tuto stránku má přístup jen administrátor!")

class EditGeneralData(generic.edit.UpdateView):
    # Edit general data for existing user
    form_class = GeneralDataForm
    template_name = "user_zone/edit_general_data.html"

    def get(self, request):
        # Getting blank template
        if request.user.is_admin:
            form = self.form_class(None)
            return render(request, self.template_name, {"form": form})
        else:
            messages.info(request, "Na tuto stránku má přístup jen administrátor!")
            return redirect(reverse("index"))


    def post(self, request):
        # Posting new data
        if request.user.is_admin:
            form = self.form_class(request.POST)
            if form.is_valid():
                form.save(commit=True)
            return render(request, self.template_name, {"form": form})
        else:
            messages.info(request, "Na tuto stránku má přístup jen administrátor!")
            return redirect(reverse("index"))
