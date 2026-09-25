from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
# from .forms import LoginForm
from django.urls import reverse_lazy
from .forms import LoginForm

app_name = 'account'

urlpatterns = [
    path('login/' , auth_views.LoginView.as_view(authentication_form=LoginForm) , name='login'),
    path('logout/' , views.log_out , name='logout'),
    path('register/' , views.register , name='register'),
    path('user/edit/' , views.edit_user , name='edit_account'),

    path('password-change/' , auth_views.PasswordChangeView.as_view(success_url=reverse_lazy('account:password_change_done')) , name='password_change'),
    path('password-change/done/' , auth_views.PasswordChangeDoneView.as_view() , name='password_change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(
    success_url=reverse_lazy('account:password_reset_done')
    ), name='password_reset'),
    path('password-reset/done/' , auth_views.PasswordResetDoneView.as_view() , name='password_reset_done'),
    path('password-reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
    success_url=reverse_lazy('account:password_reset_complete')
    ), name='password_reset_confirm'),
    path('password-reset/complete/' , auth_views.PasswordResetCompleteView.as_view() , name='password_reset_complete'),

    path('users/' , views.user_detail , name='user_detail'),

]

