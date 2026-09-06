from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('logout/', LogoutView.as_view(), name='logout'),
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/create/', views.owner_create, name='owner_create'),
    path('owners/<int:pk>/edit/', views.owner_edit, name='owner_edit'),
    path('owners/<int:pk>/delete/', views.owner_delete, name='owner_delete'),
]
