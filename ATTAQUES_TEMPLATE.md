# Attaques identifiées sur SunuSanté

Nom / Groupe :

Le chapitre 3 couvre 6 attaques : injection, force brute, DoS/DDoS, XSS,
Man-in-the-Middle, phishing. Trois sont codées et exploitables dans ce
starter ; les trois autres sont à analyser sans preuve de code (elles ne
se démontrent pas proprement dans un TP local).

## 1. Injection SQL - `patients/views.py`

**Mécanisme observé dans le code :** (comment la requête est construite,
pourquoi c'est dangereux)

**Preuve d'exploitation :** testez `GET /patients/recherche/?q=' OR '1'='1`
et comparez le nombre de résultats avec une recherche normale. Collez
votre observation (nombre de résultats avant/après).

**CID visé :**

**Correctif appliqué :** (nom de la méthode/fonction, principe utilisé)

## 2. XSS stocké - `rendezvous/templates/rendezvous/facture.html`

**Mécanisme observé dans le code :**

**Preuve d'exploitation :** créez un rendez-vous avec la note
`<script>alert('xss')</script>`, puis consultez la page facture du
patient. Que se passe-t-il avant correctif ? Après ?

**CID visé :**

**Correctif appliqué :**

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
