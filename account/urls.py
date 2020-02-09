from django.urls import path, include 
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from . import views 

urlpatterns = [

    # Login 
    path('login/', views.user_login, name = 'login'),
    #path('login/', auth_views.LoginView.as_view(template_name="account/login.html"), name = 'login'),
    
    # Logout
    path('logout/', auth_views.LogoutView.as_view(template_name="account/logged_out.html", next_page = 'account:login'), name = 'logout'),

    # Password change
    path('password_change/', 
            auth_views.PasswordChangeView.as_view(template_name='account/password_change_form.html',
                                                  success_url = reverse_lazy('account:password_change_done')),
            name = 'password_change'),
    
    path('password_change/done/', 
            auth_views.PasswordChangeDoneView.as_view(template_name='account/password_change_done.html'), 
            name = 'password_change_done'),

    # Custom password reset
    path('password_reset/', views.user_password_reset, name = 'password_reset'),
    
    path('password_reset/done', 
            auth_views.PasswordResetDoneView.as_view(template_name='account/password_reset_done.html'), 
            name = 'password_reset_done'), 

    path('reset/<uidb64>/<token>/', 
            auth_views.PasswordResetConfirmView.as_view(template_name='account/password_reset_confirm.html',
                                                        success_url = reverse_lazy('account:password_reset_complete')), 
            name = 'password_reset_confirm'),

    path('reset/done', 
            auth_views.PasswordResetCompleteView.as_view(template_name='account/password_reset_complete.html'), 
            name = 'password_reset_complete'),

    # User edit form 
    path('edit/', views.edit, name = 'edit'),

    # Registration
    path('register/', views.register, name = "register"),
    
    # Delete account
    path('delete/', views.delete, name = "delete_account"),
    path('delete/<int:confirm>/', views.delete, name = "delete_account_confirm"),
    
    # Deactivate account
    path('deactivate/', views.deactivate, name = "deactivate_account"),
    path('deactivate/<int:confirm>/', views.deactivate, name = "deactivate_account_confirm"),

    # Dashboard -sends to login if not authenticated-
    path('', views.dashboard, name = 'dashboard')
]