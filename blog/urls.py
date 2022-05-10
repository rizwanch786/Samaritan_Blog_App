from django.urls import path,include
from blog import views
from django.contrib.auth import logout, views as auth_views
from .forms import *

urlpatterns = [
    path('', views.index, name='home'),
    path('post/<int:pk>', views.PostDetail, name='PostDetail'),
    path('post/create', views.PostCreateView.as_view(), name='PostCreateView'),
    path('post/<int:pk>/edit', views.PostEditView.as_view(), name='PostEditView'),
    path('post/<int:pk>/approve', views.ApprovePost, name='ApprovePost'),
    path('post/<int:pk>/delete', views.PostDelete, name='delete'),
    path('dashboard/', views.deshboard, name='dashboard'),
    path('postComment/', views.postComment, name="postComment"),
    path('blog-list/<str:username>', views.user_blogs_list, name='blog-list'),
    path('comment/<int:pk>/delete', views.CommentDelete, name='comment-delete'),
    # Authentication Urls

# Login
    path('login/', views.user_login, name='login'),
# Logout
    path('logout/', auth_views.LogoutView.as_view(next_page = 'login'), name='logout'),

# Change Password
    path('changepassword/', auth_views.PasswordChangeView.as_view(template_name = 'blog/changepassword.html', form_class = MYPasswordChangeForm, success_url = '/passwordchangedone/'), name='changepassword'),

# password change Done
    path('passwordchangedone/', auth_views.PasswordChangeDoneView.as_view(template_name = 'blog/passwordchangedone.html'), name='passwordchangedone'),

# Password Reset 
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name = 'blog/password_reset.html', form_class = MyPasswordResetForm), name='password_reset'),

# Password Rest Done
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name = 'blog/password_reset_done.html'), name='password_reset_done'),

# Password Reset Confirm
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name = 'blog/password_reset_confirm.html', form_class = MySetPasswordForm), name='password_reset_confirm'),

# Password Reset Complete
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(template_name = 'blog/password_reset_complete.html'), name='password_reset_complete'),

# Registration
    path('registration/', views.signup.as_view(), name='signup'),
]