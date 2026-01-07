from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView, \
    PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView

from .views import dashboard_view, register_view, edit_user, EditUserView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(http_method_names=['get', 'post', 'options']), name='logout'),
    path('password_change/', PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/complete/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('signup/', register_view, name='signup'),
    # path('signup/', SignUpView.as_view(), name='signup'),
    path('profile/', dashboard_view, name='user_profile'),
    # path('profile/edit/', edit_user, name='edit_user'),
    path('profile/edit/', EditUserView.as_view(), name='edit_user'),
]