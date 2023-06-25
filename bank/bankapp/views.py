from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from .forms import ClientForm, CompteForm
import random, string
from django.db import connection
from . import models
from .models import Client, Compte
from django.template import loader


def index(request):
    clientelle = list(models.Client.objects.all())
    comptes = list(models.Compte.objects.all())
    context = {"clientelle": clientelle, "comptes": comptes}
    return render(request,"bankapp/index.html", context)

def nouveau_client(request):
    if request.method == 'POST':
        form = ClientForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Le client a été ajouté avec succès.")
    else:
        form = ClientForm()

    context = {'form': form}
    return render(request, 'bankapp/index.html', context)


def ajout_compte(request):
    if request.method == 'POST':
        form = CompteForm(request.POST)
        if form.is_valid():
            compte = form.save(commit=False)
            compte.IBAN = generate_iban()
            compte.save()
            return redirect('index')
    else:
        form = CompteForm()

    context = {'form': form}
    return render(request, 'bankapp/index.html', context)

def generate_iban():
    IBAN = "FR68"
    random_part = ''.join(random.choices(string.digits, k=5))
    IBAN += f" {random_part}"
    random_part = ''.join(random.choices(string.digits, k=5))
    IBAN += f" {random_part}"
    random_part = ''.join(random.choices(string.digits, k=10))
    IBAN += f" {random_part}"
    return IBAN


def supprimer_compte(request, compte_id):
    compte = Compte.objects.get(id=compte_id)
    compte.delete()
    return redirect('index')

def execute_sql(request):
    if request.method == 'POST':
        id = request.POST.get('id')

        # Votre commande SQL à exécuter
        sql = f"DELETE FROM client WHERE id={id};"

        with connection.cursor() as cursor:
            cursor.execute(sql)

        # Rediriger vers la page principale (index)
        return redirect('index')

        # Gérer le cas où le formulaire n'a pas été soumis
    return render(request, 'template.html')