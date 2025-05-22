from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from goods.models import Goods
from users.forms import LoginUserForm, RegisterForm, ProfileUserDataChangeForm, UserPasswordChangeForm


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'
    extra_context = {'title': 'Авторизация'}
    success_url = reverse_lazy('users:register_done')

class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = 'users/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('users:register_done')

def register_done(request):
    return render(request, 'users/register_done.html')

def profile_goods(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    ads = Goods.objects.filter(seller=user, is_published=1)
    data = {'ads': ads,
            'user': user,
            'title': f'Профиль {user.username}'}
    return render(request, 'users/profile.html', data)

def edit_profile(request):
    user = request.user

    if request.method == 'POST':
        form = ProfileUserDataChangeForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('users:profile', user_id=request.user.id)
    else:
        form = ProfileUserDataChangeForm(instance=user)

    context = {
        'form': form,
        'user': user,
        'title': 'Редактирование профиля'
    }

    return render(request, 'users/edit_profile.html', context)

def profile_unpublished_goods(request):
    ads = Goods.objects.filter(seller=request.user, is_published=0)
    data = {'ads': ads, 'title': f'Профиль {request.user.username}'}
    return render(request, 'users/profile.html', data)

class UserPasswordChange(PasswordChangeView):
    form_class = UserPasswordChangeForm
    success_url = reverse_lazy('users:password_change_done')
    extra_context = {'title': 'Изменение пароля'}
    template_name = 'users/password_change.html'

def my_profile(request):
    return render(request, 'users/my_profile.html')
