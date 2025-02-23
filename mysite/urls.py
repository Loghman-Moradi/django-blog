from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'mysite'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts/<category>/', views.post_list, name='post_list_category'),
    path('posts/detail/<pk>/', views.post_detail, name='post_detail'),
    path('tickets/', views.tickets, name='tickets'),
    path('posts/<post_id>/comment/', views.post_comment, name='post_comment'),
    path('create_post/', views.create_post, name='create_post'),
    path('search/', views.search, name='search'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit_post/<post_id>/', views.edit_post, name='edit_post'),
    path('profile/delete_post/<post_id>/', views.delete_post, name='delete_post'),
    path('profile/delete_image/<image_id>/', views.delete_image, name='delete_image'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.log_out, name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(success_url='done'), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(success_url='done'), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url="/mysite/password_rest/complete"), name='password_reset_confirm'),
    path('password_rest/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('register/', views.register, name='register'),
    path('edit_account/', views.edit_account, name='edit_account'),

]

