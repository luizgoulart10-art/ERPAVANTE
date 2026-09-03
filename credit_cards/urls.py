from django.urls import path
from .views import credit_card_dashboard_view

app_name = 'credit_cards'

urlpatterns = [
    path('dashboard/', credit_card_dashboard_view, name='dashboard'),
    path('dashboard/<int:card_id>/', credit_card_dashboard_view, name='dashboard_card'),
]