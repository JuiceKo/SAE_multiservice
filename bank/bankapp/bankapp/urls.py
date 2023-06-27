from django.urls import path
from . import views
from .views import *



urlpatterns = [
    path('', views.index, name='index'),
    path('nouveau_client/', views.nouveau_client, name='nouveau_client'),
    path('ajout_compte/', views.ajout_compte, name='ajout_compte'),
    path('client/supprimer/<int:client_id>/', views.supprimer_client, name='supprimer_client'),
    path('execute-sql/', views.execute_sql, name='execute_sql'),
    path('depot/', views.depot, name='depot'),
    path('retrait/', views.retrait, name='retrait'),
    path('comptes/', compte_list, name='compte_list'),
    path('versement/', views.versement, name='versement'),
    path('rechercher_comptes/', rechercher_comptes, name='rechercher_comptes')
]