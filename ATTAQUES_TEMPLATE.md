# Attaques identifiées sur SunuSanté

Nom / Groupe : Ndonog MBATH et Khady KA / Groupe 6

Le chapitre 3 couvre 6 attaques : injection, force brute, DoS/DDoS, XSS,
Man-in-the-Middle, phishing. Trois sont codées et exploitables dans ce
starter ; les trois autres sont à analyser sans preuve de code (elles ne
se démontrent pas proprement dans un TP local).

## Partie 1 - La sécurité comme dimension de la qualité (ISO/IEC 25010)

*À remplir avant de coder (voir README, Partie 1).* Pour chacune des 3
vulnérabilités codées, citez au moins une caractéristique ISO/IEC 25010
**autre que la sécurité** qu'elle dégrade aussi, et justifiez en une phrase.

| Vulnérabilité | Caractéristique ISO 25010 dégradée (hors sécurité) | Pourquoi |
|---|---|---|
| Injection SQL | Fiabilité, maintenabilité, performance | Une injection peut provoquer des erreurs ou des comportements imprévus, perturber les données et entraîner des requêtes coûteuses. Un code construit avec des requêtes SQL non maîtrisées est également plus difficile à maintenir et à faire évoluer. |
| XSS stocké | Utilisabilité, fiabilité, compatibilité | Le contenu malveillant peut modifier l'affichage de l'application, perturber son fonctionnement et provoquer des comportements différents selon le navigateur ou l'environnement d'exécution. |
| Force brute | Performance, fiabilité, disponibilité | De nombreuses tentatives de connexion consomment des ressources, ralentissent le service et peuvent finir par rendre l'application indisponible ou instable. |

## 1. Injection SQL - `patients/views.py`

**Mécanisme observé dans le code :** (comment la requête est construite,
pourquoi c'est dangereux)

**Preuve d'exploitation :** testez `GET /patients/recherche/?q=' OR '1'='1`
et comparez le nombre de résultats avec une recherche normale. Collez
votre observation (nombre de résultats avant/après).
* **Recherche normale**

![alt text](<Capture d’écran du 2026-08-28 10-02-14.png>)

* **Recherche avancée avec injection SQL**

![alt text](<Capture d’écran du 2026-08-28 10-07-28.png>)

**CID visé :** la confidentialité.

**Correctif appliqué :** (nom de la méthode/fonction, principe utilisé)

* Correctif :
```python
def recherche(request):
    q = request.GET.get('q', '')
    if q:
        results = Patient.objects.filter(Q(nom__icontains=q) | Q(prenom__icontains=q))
    else:
        results = Patient.objects.all()
    return render(request, 'rendezvous/recherche.html', {'results': results})
```
* Principe utilisé : filtrer les résultats par nom et prénom.

## 2. XSS stocké - `rendezvous/templates/rendezvous/facture.html`

**Mécanisme observé dans le code :** l'utilisation du filtre |safe dans {{ rdv.notes|safe }} désactive l'échappement automatique de Django et peut permettre l'interprétation de contenu HTML non fiable. Si rdv.notes contient une donnée contrôlée par un utilisateur et stockée en base, cela peut exposer l'application à une vulnérabilité XSS stockée.


**Preuve d'exploitation :** créez un rendez-vous avec la note
`<script>alert('xss')</script>`, puis consultez la page facture du
patient. Que se passe-t-il avant correctif ? Après ?

* **avant correctif**

![alt text](<Capture d’écran du 2026-08-28 10-50-34.png>)

Une boite de dialogue apparaît avec le message "xss" donc le contenu HTML est injecté dans la page facture du patient. le navigateur exécute le script et affiche le message "xss" dans la console du navigateur.

**CID visé :** la confidentialité.

**Correctif appliqué :** 
```html
<td>{{ rdv.notes }}</td> 
```

Mesure de protection : conserver l'échappement automatique de Django et ne désactiver cette protection qu'après une sanitisation appropriée du contenu.

## 3. Force brute - `personnel/views.py`

**Mécanisme observé dans le code :**

**Preuve d'exploitation :** créez un compte de test
(`python manage.py createsuperuser` ou `User.objects.create_user`) et
écrivez un petit script (ou utilisez le shell Django / `curl` en boucle)
qui tente 20 mauvais mots de passe d'affilée sur `/personnel/connexion/`.
Que se passe-t-il avant correctif ? Après ?

**CID visé :**

**Correctif appliqué :**

## 4. Déni de service (DoS/DDoS) - analyse sans code

SunuSanté n'a pas de protection anti-DoS. En vous appuyant sur le cours
(WAF, rate limiting, CDN, redondance), décrivez : (a) un scénario DoS
plausible sur SunuSanté tel qu'il existe aujourd'hui, (b) une contre-mesure
réaliste à l'échelle d'un projet comme celui-ci.

## 5. Man-in-the-Middle - analyse sans code

SunuSanté tourne en HTTP non chiffré en développement local
(`runserver`). Qu'est-ce qui protège (ou ne protège pas) les données en
transit dans ce TP ? Que faudrait-il changer avant une mise en production
réelle ?

## 6. Phishing - analyse sans code

Le personnel de la clinique se connecte via `/personnel/connexion/`.
Décrivez un scénario de phishing plausible visant ce personnel, et une
mesure de sensibilisation (pas technique) qui le limiterait.

## Panorama récapitulatif

Remplissez ce tableau pour les 6 attaques (reprend la structure du cours) :

| Attaque | Confidentialité | Intégrité | Disponibilité | Statut sur SunuSanté |
|---|---|---|---|---|
| Injection | | | | |
| Force brute | | | | |
| DoS/DDoS | | | | |
| XSS | | | | |
| MITM | | | | |
| Phishing | | | | |
