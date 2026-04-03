from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

#_______________________________________________________________________________________#

# Funções especiais:

def enviar_email_confirmacao(user, link):
    print("CHEGOU AQUI 🔥")
    html = render_to_string('confirm.html', {
        "link": link,
        "user": user
    })

    email = EmailMultiAlternatives(
        'Confirme sua conta',
        'Clique no link para confirmar sua conta',
        settings.EMAIL_HOST_USER,
        [user.email]
    )
    email.attach_alternative(html, 'text/html')
    email.send(fail_silently=False)

#_______________________________________________________________________________________#

def home(request):
    return render(request, 'home.html')

# 🔐 renomeado pra evitar conflito com auth.login
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {
                'error': 'Usuário ou senha inválidos'
            })

    return render(request, 'login.html')


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        # validação básica
        if User.objects.filter(username=username).exists():
            return render(request, 'register.html', {
                'error': 'Usuário já existe'
            })

        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {
                'error': 'Email já cadastrado'
            })

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_active = False
        user.save()

        # gerar token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # gerar link dinâmico
        link = request.build_absolute_uri(
            f"/confirmar/{uid}/{token}/"
        )

        enviar_email_confirmacao(user, link)

        return render(request, 'register.html', {
            'success': 'Registro realizado com sucesso! Verifique seu email para confirmar a conta.'
        })

    return render(request, 'register.html')


def sair(request):
    logout(request)
    return redirect('home')


def confirmar_email(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'confirmado.html')
    else:
        return render(request, 'erro.html')