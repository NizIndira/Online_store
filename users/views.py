import random

from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.crypto import get_random_string
from django.views.generic import CreateView, UpdateView

from config import settings
from users.forms import UserRegisterView, UserProfileView
from users.models import User


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterView
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        self.object = form.save()
        self.object.verification_token = get_random_string(30)
        send_mail(
            subject='Activate Your Account Now',
            message=f'Hello!\nPlease, click link below to confirm your email\n'
                    f'http://{get_current_site(self.request)}/users/confirm/{self.object.verification_token}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[self.object.email]
        )
        return super().form_valid(form)

class ProfileView(UpdateView):
    model = User
    form_class = UserProfileView
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user

# def activate_user(request, token):
#     user = User.objects.get(verification_token=token)
#     user.verification_token = ''
#     user.is_active = True
#     user.save()
#     return redirect(reverse('users:login'))


def password_reset(request):
    context = {
        'title': 'Resetting Password',
        'sub_title': 'You will receive a new password to the specified email'
    }

    if request.method == 'POST':
        try:
            user = User.objects.get(email=request.POST.get('email'))
        except User.DoesNotExist:
            context = {
                'title': 'Пользователя с указанной почтой не существует',
                'sub_title': 'Попробуйте ввести ещё раз'
            }
            return render(request, 'users/pass_reset.html', context)
        new_password = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        send_mail(
            subject='Новый пароль',
            message=f'Здравствуйте!\nВаш новый пароль: {new_password}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user.email]
        )
        user.set_password(new_password)
        user.save()
        return redirect(reverse_lazy('users:login'))
    return render(request, 'users/password_reset.html', context)
