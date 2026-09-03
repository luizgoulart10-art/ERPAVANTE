from django.urls import path
from . import views

urlpatterns = [
    path('painel-abertos/', views.open_orders_dashboard, name='open_orders_dashboard'),
]