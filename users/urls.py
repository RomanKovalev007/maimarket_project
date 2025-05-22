from django.contrib.auth.views import LogoutView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, \
    PasswordResetConfirmView, PasswordChangeDoneView

from . import views
from django.urls import path, reverse_lazy

app_name = 'users'

urlpatterns = [
    path('profile/<int:user_id>/', views.profile_goods, name='profile'),
    path('profile/not_published/', views.profile_unpublished_goods, name='profile_not_published'),
    path('profile/change_data/', views.edit_profile, name='profile_change_data'),
    path('profile/change_password/', views.UserPasswordChange.as_view(), name='password_change'),
    path('profile/change_password/done/',
         PasswordChangeDoneView.as_view(template_name='users/password_change_done.html'), name='password_change_done'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('register_done/', views.register_done, name='register_done'),
    path('password_reset/', PasswordResetView.as_view(
        template_name='users/password_reset_form.html',
        email_template_name='users/password_reset_email.html',
        success_url=reverse_lazy('users:password_reset_done')),
         name='password_reset'),

    path('password_reset/done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
         name='password_reset_done'),

    path('password_reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(
        template_name='users/password_reset_confirm.html',
        success_url=reverse_lazy('users:password_reset_complete')),
         name='password_reset_confirm'),

    path('password_reset_complete/', PasswordResetCompleteView.as_view(
        template_name='users/password_reset_complete.html'),
         name='password_reset_complete')
]