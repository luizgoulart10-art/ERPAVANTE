from django.db import models

# Create your models here.
from django.db import models

class Supplier(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Fornecedor")
    # Opcionais agora: null=True, blank=True
    cnpj = models.CharField(max_length=20, null=True, blank=True, verbose_name="CNPJ")
    email = models.EmailField(null=True, blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name="Telefone")
    # Novo campo opcional de Contato
    contact = models.CharField(max_length=100, null=True, blank=True, verbose_name="Contato")

    def __str__(self):
        return self.name
class Customer(models.Model):
    name = models.CharField(max_length=200, verbose_name="Nome do Cliente")
    # Opcionais agora: null=True, blank=True
    cnpj_cpf = models.CharField(max_length=20, null=True, blank=True, verbose_name="CNPJ/CPF")
    email = models.EmailField(null=True, blank=True, verbose_name="E-mail")
    phone = models.CharField(max_length=30, null=True, blank=True, verbose_name="Telefone")
    # Novo campo opcional de Contato
    contact = models.CharField(max_length=100, null=True, blank=True, verbose_name="Contato")

    def __str__(self):
        return self.name