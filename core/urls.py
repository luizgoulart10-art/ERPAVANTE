from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('credit-cards/', include('credit_cards.urls')),
    # ... suas outras rotas ...
]