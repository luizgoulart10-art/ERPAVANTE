from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('credit-cards/', include('credit_cards.urls')),
    # Redireciona a página inicial (raiz) direto para o Admin do ERP:
    path('', RedirectView.as_view(url='/admin/', permanent=False)),
]