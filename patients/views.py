"""
TP3 - Vue fournie aux étudiants.

Fonctionnalité demandée par la clinique : permettre au personnel de
rechercher un patient par nom ou prénom. Le développeur pressé a répondu
avec du SQL brut construit par concaténation de chaîne — ça marche pour une
recherche normale, mais c'est une injection SQL en bonne et due forme
(chapitre 3, partie 3).

NE MODIFIEZ PAS CE FICHIER avant d'avoir lu le README de ce dossier.
"""
from django.db import connection
from django.shortcuts import render
from django.db.models import Q

from .models import Patient


def rechercher_patient(request):
    q = request.GET.get("q", "")
    resultats = []

    if q:
        resultats = Patient.objects.filter(Q(nom__icontains=q) | Q(prenom__icontains=q))
    else:
        resultats = Patient.objects.all()
        
    return render(request, "patients/recherche.html", {"q": q, "resultats": resultats})

