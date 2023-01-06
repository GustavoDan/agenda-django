"""agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LoginView
from django.urls import path, reverse_lazy
from django.views.generic import RedirectView
from core import views

urlpatterns = [
    path("", RedirectView.as_view(url=reverse_lazy("root"))),
    path("admin/", admin.site.urls),
    path("register/", views.register_user, name="register"),
    path("login/", LoginView.as_view(redirect_authenticated_user=True, template_name='user/login.html'), name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("user/", views.user_page, name="user"),
    path("user/change-password/", views.CustomPasswordChangeView.as_view(), name="change-password"),
    path("schedules/", views.list_events, name="root"),
    path("schedules/past/", views.list_passed_events, name="past-schedules"),
    path("schedules/event/", views.create_or_update_event, name="event"),
    path("schedules/event/<int:event_id>/delete", views.delete_event, name="delete_event"),
    path("schedules/json/<int:user_id>/", views.json_list_events),
]
