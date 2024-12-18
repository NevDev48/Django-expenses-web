from .views import ExpensesView, RegistrationView, UsernameValidationView, EmailValidationView, LoginView
from django.urls import path
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('register', RegistrationView.as_view(), name="register"),
    path('login', LoginView.as_view(), name="login"),
    path('validate-username', csrf_exempt( UsernameValidationView.as_view()),
         name="validate-username"),
    path('validate-email', csrf_exempt(EmailValidationView.as_view()), name='validate-email'),
    path('expenses/', ExpensesView.as_view(), name='expenses')
]
