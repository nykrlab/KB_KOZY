from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = 'accounts'

# urlpatterns = [
#     # path('login/', login_view, name="login"), 
#     path('', views.login_view, name="login"),
#     path('register/', views.register_user, name="register"),
#     path('logout/', views.logout, name='logout'),
# ]

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("", views.SignInView.as_view(), name="signin"),
    path("signout/", views.signout, name="signout"),
]