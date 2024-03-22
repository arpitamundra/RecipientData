from django.urls import path
from . import views

urlpatterns = [
    path('tallydata/upload', views.upload_file, name='upload_file'),
    path('success/', views.success_view, name='success'),
]
