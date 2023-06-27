from django import forms
from .models import Client, Compte

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ['nom', 'prenom', 'sexe', 'email', 'nom_utilisateur', 'mdp']


class CompteForm(forms.ModelForm):
    class Meta:
        model = Compte
        fields = ['client']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].empty_label = 'Sélectionner un client'
