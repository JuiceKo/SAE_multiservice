from django.urls import path
from . import views



urlpatterns = [
    path('', views.index, name='index'),
    path('nouveau_client/', views.nouveau_client, name='nouveau_client'),
    path('ajout_compte/', views.ajout_compte, name='ajout_compte'),
    path('compte/supprimer/<int:compte_id>/', views.supprimer_compte, name='supprimer_compte'),
    path('execute-sql/', views.execute_sql, name='execute_sql'),
    path('depot/', views.depot, name='depot'),
    path('retrait/', views.retrait, name='retrait'),
]