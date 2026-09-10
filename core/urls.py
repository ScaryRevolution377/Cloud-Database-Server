from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('delete/<int:file_id>/', views.delete_file, name='delete_file'),
]