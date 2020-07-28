from django.urls import path
from . import views
from .views import *
from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [path('', views.homepage, name='homepage'),
            path('question/', views.questionpage, name='question'),
            path('update/<str:pk>', views.updatequestion, name='update'),
            path('delete/<str:pk>', views.deletequestion, name='delete'),

            path('question/<int:pk>/',views.showanswer, name='showanswer'),
            path('signup/',views.signup, name='signup'),
            path('login/',views.loginfn, name='login'),
            path('logout', views.logoutt, name='logout'),
            path('profilepage/', views.profile_page, name='profile'),
            path('updateanswer/<str:pk>', views.updateanswer, name='update_answer'),
            path('user_profile/edit_user', views.edit_user_info, name='edit_user'),
            path('user_profile/<str:username>', user_profile.as_view(), name='user_profile'),
            path('like_/<str:pk>/<slug:slug>', views.likeview, name='like'),
            path('delete_answer/<str:pk>', views.deleteanswer, name='delete_answer'),
            ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)