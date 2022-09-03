from django.urls import path
from knox import views as knox_views
from .views import LoginView, RegisterView, ActivateView

# from .views import SimpleRegisterView

urlpatterns = [
    path(r"login/", LoginView.as_view(), name="knox_login"),
    path(r"logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path(r"logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
    path(r"register/", RegisterView.as_view(), name="register"),
    path(r"activate/", ActivateView.as_view(), name="activate"),
    # path(r"simpleregister/", SimpleRegisterView.as_view(), name="simpleregister"),
]
