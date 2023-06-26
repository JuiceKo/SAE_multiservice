from django.shortcuts import render, redirect
from django.http import HttpResponse
import mysql.connector
from .forms import ClientForm, CompteForm
import random, string
from django.db import connection
from . import models
from .models import Client, Compte
from django.template import loader
import asyncio
from nats.aio.client import Client
import nats
from nats.aio.errors import ErrConnectionClosed, ErrTimeout
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
import csv



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


#_________________________________________________________________________________________________________________________#



def supprimer_client(request, client_id):
    client = Client.objects.get(id=client_id)
    client.delete()
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


#_________________________________________________________________________________________________________________________#

"""async def publish_deposit_message():
    nc = NATS()
    await nc.connect(servers=["10.128.200.7:4222"])

    message = "test"

    await nc.publish("deposit", message.encode())

    await nc.close()

async def publish_verification_message(montant):
    if montant > 10000:
        await publish_deposit_message()"""




def depot(request):
    if request.method == 'POST':
        iban = request.POST.get('iban')  # Récupérer l'IBAN à partir des données POST
        montant = float(request.POST.get('montant'))  # Récupérer le montant à partir des données POST

        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="toto",
            database="bankapp",
            port="3307",
        )

        # Création d'un curseur pour exécuter des requêtes SQL
        cursor = cnx.cursor()

        # Fonction pour trouver le solde d'un compte en fonction de son IBAN
        def trouver_solde_par_iban(iban):
            query = "SELECT solde FROM compte WHERE IBAN = %s"
            cursor.execute(query, (iban,))
            result = cursor.fetchone()
            if result:
                solde = result[0]
                return solde
            else:
                print(f"Aucun compte trouvé avec l'IBAN {iban}.")
                return None

        # Fonction pour mettre à jour le solde d'un compte
        def mettre_a_jour_solde(iban, montant):
            solde = trouver_solde_par_iban(iban)
            if solde is not None:
                solde = float(solde)
                nouveau_solde = solde + montant
                query = "UPDATE compte SET solde = %s WHERE IBAN = %s"
                cursor.execute(query, (nouveau_solde, iban))
                cnx.commit()
                print(f"Le solde du compte {iban} a été mis à jour : {nouveau_solde} euros.")

                """if montant > 10000:
                    asyncio.run(publish_verification_message(montant))"""

        # Exemple d'utilisation : ajout du montant donné au solde d'un compte avec un IBAN spécifique
        mettre_a_jour_solde(iban, montant)

        """asyncio.run(publish_verification_message(montant))"""

        # Fermeture du curseur et de la connexion à la base de données
        cursor.close()
        cnx.close()

        return HttpResponse("Le solde a été mis à jour avec succès.")
    else:
        return HttpResponse("Erreur : méthode non autorisée.")

#_________________________________________________________________________________________________________________________#

"""async def publish_verification_message(montant):
    nc = await nats.connect("ws://10.128.200.7:4222")

    async def error_cb(e):
        print("Error:", e)

    async def closed_cb():
        print("Connection closed.")

    try:
        await nc.connect(servers=["ws://10.128.200.7:4222"], error_cb=error_cb, closed_cb=closed_cb)

        montant = "10001"
        #if montant > 10000:
        await nc.publish("deposit", float(montant).encode())

        await nc.flush()
        await nc.close()

    except (ErrConnectionClosed, ErrTimeout) as e:
        print("Error:", e)"""



def retrait(request):
    if request.method == 'POST':
        iban = request.POST.get('iban')  # Récupérer l'IBAN à partir des données POST
        montant = float(request.POST.get('montant'))  # Récupérer le montant à partir des données POST

        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            password="toto",
            database="bankapp",
            port="3307",
        )

        # Création d'un curseur pour exécuter des requêtes SQL
        cursor = cnx.cursor()

        # Fonction pour trouver le solde d'un compte en fonction de son IBAN
        def trouver_solde_par_iban(iban):
            query = "SELECT solde FROM compte WHERE IBAN = %s"
            cursor.execute(query, (iban,))
            result = cursor.fetchone()
            if result:
                solde = result[0]
                return solde
            else:
                print(f"Aucun compte trouvé avec l'IBAN {iban}.")
                return None

        # Fonction pour mettre à jour le solde d'un compte
        def mettre_a_jour_solde(iban, montant):
            solde = trouver_solde_par_iban(iban)
            if solde is not None:
                solde = float(solde)
                nouveau_solde = solde - montant
                query = "UPDATE compte SET solde = %s WHERE IBAN = %s"
                cursor.execute(query, (nouveau_solde, iban))
                cnx.commit()
                print(f"Le solde du compte {iban} a été mis à jour : {nouveau_solde} euros.")

                """if montant > 10000:
                    asyncio.run(publish_verification_message(montant))"""

        # Exemple d'utilisation : ajout du montant donné au solde d'un compte avec un IBAN spécifique
        mettre_a_jour_solde(iban, montant)

        # Fermeture du curseur et de la connexion à la base de données
        cursor.close()
        cnx.close()

        return HttpResponse("Le solde a été mis à jour avec succès.")
    else:
        return HttpResponse("Erreur : méthode non autorisée.")

#_________________________________________________________________________________________________________________________#

def get_comptes_by_client_id(client_id):
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        password="toto",
        database="bank",
        port="3307",
    )
    cursor = cnx.cursor()
    query = "SELECT * FROM compte WHERE client_id = %s"
    cursor.execute(query, (client_id,))
    comptes = cursor.fetchall()
    cursor.close()
    cnx.close()
    return comptes

# Vue pour la page avec le formulaire et les résultats des comptes
def compte_list(request):
    comptes = []
    message = ""

    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        comptes = get_comptes_by_client_id(client_id)
        if not comptes:
            message = f"Aucun compte trouvé pour l'ID du client {client_id}."

    context = {'comptes': comptes, 'message': message}
    return render(request, 'bankapp/compte_list.html', context)


#_________________________________________________________________________________________________________________________#

from django.shortcuts import render
import mysql.connector

# Connexion à la base de données
cnx = mysql.connector.connect(
    host="localhost",
    user="root",
    password="toto",
    database="bankapp",
    port="3307"
)

# Création d'un curseur pour exécuter des requêtes SQL
cursor = cnx.cursor()

def get_solde_by_iban(iban):
    query = "SELECT solde FROM compte WHERE IBAN = %s"
    cursor.execute(query, (iban,))
    result = cursor.fetchone()
    if result:
        solde = result[0]
        return solde
    else:
        print(f"Aucun compte trouvé avec l'IBAN {iban}.")
        return None

def mettre_a_jour_solde(iban, montant):
    solde = get_solde_by_iban(iban)
    if solde is not None:
        solde = float(solde)
        nouveau_solde = solde + montant
        query = "UPDATE compte SET solde = %s WHERE IBAN = %s"
        cursor.execute(query, (nouveau_solde, iban))
        cnx.commit()
        print(f"Le solde du compte {iban} a été mis à jour : {nouveau_solde} euros.")

def versement(request):
    if request.method == 'POST':
        iban_source = request.POST.get('iban_source')
        iban_cible = request.POST.get('iban_cible')
        montant = float(request.POST.get('montant'))

        mettre_a_jour_solde(iban_source, -montant)
        mettre_a_jour_solde(iban_cible, montant)

        return render(request, 'bankapp/index.html')
    else:
        return render(request, 'bankapp/index.html')


# _________________________________________________________________________________________________________________________#


"""def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('accueil')  # Rediriger vers la page d'accueil après la connexion
        else:
            error_message = "Identifiants invalides. Veuillez réessayer."
            return render(request, 'login.html', {'error_message': error_message})
    else:
        return render(request, 'login.html')"""


# _________________________________________________________________________________________________________________________#

def rechercher_comptes(request):
    if request.method == 'POST':
        client_id = request.POST.get('client_id')
        comptes = Compte.objects.filter(client_id=client_id)

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="comptes_client_{}.csv"'.format(client_id)

        writer = csv.writer(response, delimiter=' ')  # Utilisation du délimiteur d'espace
        writer.writerow(['IBAN', 'Solde'])

        for compte in comptes:
            writer.writerow([compte.IBAN, compte.solde])

        return response

    return render(request, 'bankapp/index.html')

