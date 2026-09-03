from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.cash_flow_dashboard, name='cash_flow_dashboard'),
]