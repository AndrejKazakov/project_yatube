from django.urls import path
from core import views

app_name = 'core'

urlpatterns = [
    path('404/', views.page_not_found, name='404'),
    path('403/', views.csrf_failure, name='403'),
]
