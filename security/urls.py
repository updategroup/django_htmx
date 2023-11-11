from django.urls import path
from security import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    # path('logout/', LogoutView.as_view(), name='logout'),
    path("register/", views.RegisterView.as_view(), name="register")
]

url_htmx = [
    path('username-check/', views.username_check, name='username_check'),
    path('register-submit/', views.register_submit, name='register'),
]
urlpatterns+=url_htmx