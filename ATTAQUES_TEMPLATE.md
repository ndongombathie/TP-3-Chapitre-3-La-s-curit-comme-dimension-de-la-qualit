# Attaques identifiées sur SunuSanté

Nom / Groupe : Ndongo MBATH et Khady KA / Groupe 6

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

La requête SQL est construite en concaténant directement la valeur q fournie par l'utilisateur dans la chaîne SQL grâce à une f-string :

requete_sql = (
    "SELECT id, nom, prenom, email, est_vip FROM patients_patient "
    f"WHERE nom LIKE '%{q}%' OR prenom LIKE '%{q}%'"
)

Cette construction est dangereuse car la valeur de q est intégrée directement dans la requête sans être séparée du code SQL. Un utilisateur malveillant peut donc fournir une entrée spécialement conçue pour modifier la structure de la requête au lieu d'être considérée uniquement comme une donnée. Cela expose l'application à une injection SQL, pouvant notamment permettre la lecture ou la modification non autorisée de données.


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
        resultats = Patient.objects.filter(Q(nom__icontains=q) | Q(prenom__icontains=q))
    else:
        resultats = Patient.objects.all()
    return render(request, 'patients/recherche.html', {'resultats': resultats})
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

**Mécanisme observé dans le code :** La fonction connexion() utilise authenticate() pour vérifier les identifiants, mais aucun mécanisme de limitation des tentatives de connexion n'est présent. Il n'y a ni compteur d'échecs, ni blocage temporaire du compte, ni limitation par adresse IP, ni délai progressif. Un attaquant peut donc effectuer de nombreuses tentatives de mot de passe successives.ù


**Preuve d'exploitation :** créez un compte de test
(`python manage.py createsuperuser` ou `User.objects.create_user`) et
écrivez un petit script (ou utilisez le shell Django / `curl` en boucle)
qui tente 20 mauvais mots de passe d'affilée sur `/personnel/connexion/`.
Que se passe-t-il avant correctif ? Après ?

* **Que se passe-t-il avant correctif ?**

Avant le correctif, la fonction connexion() accepte les tentatives de connexion successives sans appliquer de limitation. Chaque mauvais mot de passe provoque simplement le message « Identifiants incorrects » puis une redirection HTTP 302 vers la page de connexion. Même après 20 tentatives consécutives, aucun blocage, ralentissement ou limitation n'est appliqué. L'application est donc vulnérable aux attaques par force brute.

* **Que se passe-t-il après correctif ?**

Après le correctif, un mécanisme de limitation des tentatives est mis en place. Après un certain nombre d'échecs consécutifs, les nouvelles tentatives sont ralenties, temporairement bloquées ou refusées, par exemple avec une réponse HTTP 429 Too Many Requests. Cela réduit fortement la possibilité pour un attaquant d'essayer rapidement un grand nombre de mots de passe.


**CID visé :** la confidentialité, la disponibilité(si le nombre de tentatives de connexion est tres important).

**Correctif appliqué :** 
Mise en place d'un mécanisme de limitation des tentatives de connexion (rate limiting). Après plusieurs échecs consécutifs, les nouvelles tentatives sont temporairement bloquées ou ralenties afin de réduire l'efficacité d'une attaque par force brute. Le nombre de tentatives échouées est également surveillé et peut faire l'objet d'une journalisation et d'une alerte.

## 4. Déni de service (DoS/DDoS) - analyse sans code

SunuSanté n'a pas de protection anti-DoS. En vous appuyant sur le cours
(WAF, rate limiting, CDN, redondance), décrivez : (a) un scénario DoS
plausible sur SunuSanté tel qu'il existe aujourd'hui, (b) une contre-mesure
réaliste à l'échelle d'un projet comme celui-ci.

* **Scénario :** un attaquant envoie massivement des requêtes vers SunuSanté afin de saturer le serveur ou la base de données, rendant le service lent ou indisponible.

* **Contre-mesure :** mettre en place un rate limiting sur les endpoints sensibles et placer un WAF/CDN devant l'application afin de filtrer et absorber une partie du trafic malveillant.

## 5. Man-in-the-Middle - analyse sans code

SunuSanté tourne en HTTP non chiffré en développement local
(`runserver`). Qu'est-ce qui protège (ou ne protège pas) les données en
transit dans ce TP ? Que faudrait-il changer avant une mise en production
réelle ?

En développement local, SunuSanté utilise HTTP avec runserver. Les données ne sont donc pas chiffrées par TLS en transit ; cependant, avec 127.0.0.1, le trafic reste local et le risque de MITM réseau est limité. Avant la production, il faut utiliser HTTPS/TLS avec un certificat valide, un serveur/reverse proxy correctement configuré et des cookies sécurisés.

## 6. Phishing - analyse sans code

Le personnel de la clinique se connecte via `/personnel/connexion/`.
Décrivez un scénario de phishing plausible visant ce personnel, et une
mesure de sensibilisation (pas technique) qui le limiterait.

Scénario : un attaquant envoie au personnel un faux email imitant la direction ou l'administrateur de SunuSanté et contenant un lien vers une fausse page /personnel/connexion/. Le personnel saisit ses identifiants, qui sont récupérés par l'attaquant.
Mesure : sensibiliser régulièrement les employés à reconnaître les emails et liens suspects et organiser des simulations de phishing pour renforcer leurs réflexes.

## Panorama récapitulatif

Remplissez ce tableau pour les 6 attaques (reprend la structure du cours) :

| Attaque | Confidentialité | Intégrité | Disponibilité | Statut sur SunuSanté |
|---|---|---|---|---|
| Injection | O | O | | requête SQL construite avec q directement |
| Force brute | O | | O | aucune limitation des tentatives |
| DoS/DDoS | | | O | aucune protection anti-DoS, WAF ou rate limiting global |
| XSS | O | | | utilisation de html `{{ rdv.notes\|safe }} ` |
| MITM | O | O | | HTTP non chiffré avec runserver |
| Phishing | O | O | |sensibilisation nécessaire |
