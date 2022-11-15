from django.urls import path
from . import views

urlpatterns = [
    path("register/", views.UserViewRegister.as_view(), name="register"),
    path("login/", views.UserViewLogin.as_view(), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("general_data_list/", views.GeneralDataFilterView.as_view(), name="general_data_list"),
    path("edit_general_data/", views.EditGeneralData.as_view(), name="edit_general_data")
]
