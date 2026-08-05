# SunuSanté - TP3 : La sécurité comme dimension de la qualité (Django)

## Contexte

La clinique a validé le TP2 et demande trois nouvelles fonctionnalités,
livrées en urgence par un développeur pressé : chercher un patient par
nom, ajouter des notes à un rendez-vous, et un espace de connexion pour le
personnel. Les trois marchent... et les trois sont vulnérables.

## Installation

```bash
python -m venv venv
# Windows : venv\Scripts\activate   |   macOS/Linux : source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

- Recherche de patients : http://127.0.0.1:8000/patients/recherche/
- Prise de rendez-vous (avec notes) : http://127.0.0.1:8000/rendezvous/
- Facture (affiche les notes) : http://127.0.0.1:8000/rendezvous/facture/1/
- Connexion personnel : http://127.0.0.1:8000/personnel/connexion/
- Admin : http://127.0.0.1:8000/admin/

---

## Partie 1 - La sécurité comme dimension de la qualité

En groupe, sans coder : relisez les 8 caractéristiques ISO/IEC 25010 vues
au TP1. Pour chacune des 3 vulnérabilités que vous allez trouver dans ce
TP (SQLi, XSS, force brute), identifiez au moins une caractéristique de
qualité (autre que "sécurité") qu'elle dégrade aussi. Notez vos réponses
en haut de `ATTAQUES_TEMPLATE.md`.

## Partie 2 - Le triptyque CID

Complétez `CID_TEMPLATE.md` en reliant Confidentialité, Intégrité et
Disponibilité au code réel de SunuSanté (pas à l'exemple générique du
cours).

## Partie 3 - Casser puis réparer

Pour chacune des 3 vulnérabilités ci-dessous : reproduisez l'exploitation,
documentez-la dans `ATTAQUES_TEMPLATE.md`, corrigez le code, puis écrivez
un test qui aurait échoué avant votre correctif.

### 3.1 - Injection SQL (`patients/views.py`)

`rechercher_patient` construit sa requête SQL par concaténation de
chaîne. Lancez le serveur et testez dans votre navigateur :

```
http://127.0.0.1:8000/patients/recherche/?q=Ndiaye
http://127.0.0.1:8000/patients/recherche/?q=' OR '1'='1
```

Comparez le nombre de résultats. **Correctif attendu** : remplacez le SQL
brut par un `QuerySet` Django (`Patient.objects.filter(...)` avec `Q`),
qui paramètre automatiquement la requête.

### 3.2 - XSS stocké (`rendezvous/templates/rendezvous/facture.html`)

Créez un rendez-vous (`/rendezvous/`) avec, dans le champ Notes :

```html
<script>alert('xss')</script>
```

Consultez ensuite `/rendezvous/facture/<id>/`. **Correctif attendu** :
supprimez le filtre `|safe` sur `{{ rdv.notes }}`. L'échappement
automatique de Django suffit, il ne faut jamais le désactiver sur du
contenu saisi par un utilisateur.

### 3.3 - Force brute (`personnel/views.py`)

Créez un utilisateur de test, puis tentez de vous connecter avec un
mauvais mot de passe autant de fois que vous voulez sur
`/personnel/connexion/` : rien ne vous arrête.

**Correctif attendu** : créez `personnel/services.py` avec une classe
`LoginThrottle` qui compte les échecs par identifiant (via
`django.core.cache.cache`) et bloque après 5 tentatives échouées pendant
15 minutes. Utilisez-la dans `connexion()` avant d'appeler
`authenticate()`.

## Partie 4 - Détecter outillé : SAST, DAST, SCA

### SAST - Semgrep

```bash
pip install semgrep
semgrep --config p/security-audit --config p/django --config p/python .
```

Observez : Semgrep détecte-t-il le `|safe` (XSS) ? Détecte-t-il
l'injection SQL par `connection.cursor().execute(...)` ? Notez ce qu'il
trouve **et** ce qu'il rate dans `ATTAQUES_TEMPLATE.md`. C'est le point
clé de cette partie : le SAST ne remplace pas une revue humaine ni le DAST.

### DAST - OWASP ZAP

Avec le serveur Django lancé (`python manage.py runserver`), dans un autre
terminal (nécessite Docker) :

```bash
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t http://host.docker.internal:8000/rendezvous/
```

Le "baseline scan" est une analyse passive rapide, adaptée à un TP.
Consultez le rapport généré et notez les alertes pertinentes (headers de
sécurité manquants, cookies sans flag `Secure`, etc.).

### SCA - pip-audit

```bash
pip install pip-audit
pip-audit -r requirements.txt
```

`requirements.txt` pointe encore sur Django 5.0.6. **Correctif attendu** :
identifiez, dans le rapport, la branche de Django encore maintenue et
sans vulnérabilité connue, puis mettez à jour `requirements.txt` en
conséquence. Réinstallez (`pip install -r requirements.txt --upgrade`) et
relancez `python manage.py test` pour vérifier que rien n'a cassé.

## Rendu attendu

- `CID_TEMPLATE.md` et `ATTAQUES_TEMPLATE.md` complétés
- Les 3 correctifs appliqués (`patients/views.py`, `facture.html`,
  `personnel/services.py` + `personnel/views.py`)
- `requirements.txt` mis à jour vers une version de Django sans CVE connue
- Tests de non-régression pour les 3 correctifs, tous verts
  (`python manage.py test`)
- Rapports Semgrep, ZAP et pip-audit (fichiers ou captures) avec un court
  commentaire sur ce que chaque outil a trouvé ou raté
