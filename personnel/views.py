"""
TP3 - Vue fournie aux étudiants.

Connexion du personnel de la clinique à un espace dédié (distinct de
l'admin Django). L'authentification elle-même est correcte : Django
compare un hash de mot de passe, pas un mot de passe en clair. Mais rien
n'empêche un script d'essayer des milliers de mots de passe à la suite sur
le même compte, aussi vite que le réseau le permet (chapitre 3, attaque
par force brute).

NE MODIFIEZ PAS CE FICHIER avant d'avoir lu le README de ce dossier.
"""
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render


def connexion(request):
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("password", "")

        # TODO (TP3) : aucune limite sur le nombre de tentatives, ni par
        # compte ni par adresse IP. Rien ne ralentit un script de force
        # brute qui essaierait un dictionnaire de mots de passe ici.
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Bienvenue, {user.username}")
            return redirect("personnel:connexion")

        messages.error(request, "Identifiants incorrects")
        return redirect("personnel:connexion")

    return render(request, "personnel/connexion.html")
