from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
from validate_email_address import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage


# Create your views here.

class EmailValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email = data.get('email', '')
            
            if not validate_email(email):
                return JsonResponse(
                    {'email_error': 'Email is invalid.'},
                    status=400
                )
            if User.objects.filter(email=email).exists():
                return JsonResponse(
                    {'email_error': 'sorry email is use, chose another one'},
                    status=409
                )

            # Tambahkan validasi tambahan jika diperlukan (misalnya, cek duplikat username di database)
            return JsonResponse({'email_valid': True}, status=200)

        except json.JSONDecodeError:
            return JsonResponse(
                {'valid': False, 'email_error': 'Invalid JSON data.'},
                status=400
            )

class RegistrationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')
    
    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }

        if not User.objects.filter(username=username).exists():
             if not User.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'authentication/register.html', context)
                
                user = User.objects.create_user(username=username, email=email)
                user.set_password(password)
                user.is_active = False
                user.save()
                email_subject = 'Activate your account'
                email_body = 'Test body'
                email = EmailMessage(
                    email_subject,
                    email_body,
                    "noreply@semycolon.com",
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created')
                return render(request, 'authentication/register.html')
            
        return render(request, 'authentication/register.html')
    
class UsernameValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            username = data.get('username', '')

            # Validasi username
            if not username.isalnum():
                return JsonResponse(
                    {'error': 'Username should only contain alphanumeric characters.'},
                    status=400
                )
            if User.objects.filter(username=username).exists():
                return JsonResponse(
                    {'error': 'sorry username is use, chose another one'},
                    status=409
                )

            # Tambahkan validasi tambahan jika diperlukan (misalnya, cek duplikat username di database)
            return JsonResponse({'username_valid': True}, status=200)

        except json.JSONDecodeError:
            return JsonResponse(
                {'valid': False, 'error': 'Invalid JSON data.'},
                status=400
            )
