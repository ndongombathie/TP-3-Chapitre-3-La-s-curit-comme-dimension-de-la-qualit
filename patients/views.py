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

from .models import Patient


def rechercher_patient(request):
    q = request.GET.get("q", "")
    resultats = []

    if q:
        # TODO (TP3) : requête construite par concaténation de chaîne,
        # sans paramètre lié. Testez avec q = ' OR '1'='1
        requete_sql = (
            "SELECT id, nom, prenom, email, est_vip FROM patients_patient "
            f"WHERE nom LIKE '%{q}%' OR prenom LIKE '%{q}%'"
        )
        with connection.cursor() as cursor:
            cursor.execute(requete_sql)
            colonnes = [col[0] for col in cursor.description]
            resultats = [dict(zip(colonnes, ligne)) for ligne in cursor.fetchall()]

    return render(request, "patients/recherche.html", {"q": q, "resultats": resultats})
