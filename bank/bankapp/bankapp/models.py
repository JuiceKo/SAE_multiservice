# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class Client(models.Model):
    #id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=75, null=True)
    prenom = models.CharField(max_length=75, null=True)
    SEXE_CHOICES = [
        ('Homme', 'Homme'),
        ('Femme', 'Femme'),
    ]
    sexe = models.CharField(max_length=10, choices=SEXE_CHOICES, null=True)
    email = models.CharField(max_length=100, null=True)
    nom_utilisateur = models.CharField(max_length=50, null=True)
    mdp = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'client'


"""class Client(AbstractUser):
    nom_utilisateur = models.CharField(max_length=150, unique=True)
    mdp = models.CharField(max_length=128)

    USERNAME_FIELD = 'nom_utilisateur'
    REQUIRED_FIELDS = ['email']  # Ajoutez ici les champs requis pour la création d'un utilisateur

    def __str__(self):
        return self.nom_utilisateur"""


class Compte(models.Model):
    #id = models.IntegerField(primary_key=True)
    IBAN = models.CharField(max_length=50, unique=True, null=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True)
    solde = models.DecimalField(max_digits=10, decimal_places=2, null=True, default=0.00)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'compte'

    def __str__(self):
        return self.iban


class Personnel(models.Model):
    #id = models.IntegerField(primary_key=True)
    nom = models.CharField(max_length=75, blank=True, null=True)
    prenom = models.CharField(max_length=75, blank=True, null=True)
    email = models.CharField(max_length=100, blank=True, null=True)
    date_arrive = models.DateTimeField(blank=True, null=True)
    nom_utilisateur = models.CharField(max_length=50, blank=True, null=True)
    mdp = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'personnel'


class Transaction(models.Model):
    #id = models.IntegerField(primary_key=True)
    compte_source = models.ForeignKey(Compte, on_delete=models.DO_NOTHING, db_column='compte_source', blank=True, null=True, related_name='transactions_source')
    compte_cible = models.ForeignKey(Compte, on_delete=models.DO_NOTHING, db_column='compte_cible', blank=True, null=True, related_name='transactions_cible')
    montant = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    type = models.CharField(max_length=25, blank=True, null=True)

    class Meta:
        db_table = 'transaction'
