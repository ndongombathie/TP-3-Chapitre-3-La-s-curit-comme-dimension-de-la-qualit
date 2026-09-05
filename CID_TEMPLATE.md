# Le triptyque CID appliqué à SunuSanté

Nom / Groupe : Ndongo MBATH et Khady KA / Groupe 6

Le cours illustre le CID avec l'exemple d'un dossier médical électronique
(chapitre 3, partie 2) : c'est exactement ce que gère SunuSanté. Ne
recopiez pas l'exemple du cours. Reliez chaque propriété au **code réel**
de votre projet.

## Confidentialité

*Seules les personnes autorisées accèdent à l'information.*

- Qui peut aujourd'hui consulter la liste des patients et leurs
  rendez-vous dans SunuSanté (regardez `/admin/`, `/patients/recherche/`,
  `/rendezvous/facture/<id>/`) ? Y a-t-il un contrôle d'accès sur ces
  pages ?

  Non ,les views ne sont pas protégées par une autorisation(permission,Role-Based Access Control) donc tout le monde peut accéder à la liste des patients et leurs
  rendez-vous dans SunuSanté.
  
- Le mot de passe du personnel est-il stocké et vérifié correctement
  (indice : regardez comment Django gère `User.objects.create_user`) ?

  Oui ,le mot de passe est stocké et vérifié correctement avec le hash de mot de passe de Django.

  ![alt text](<images/Capture d’écran du 2026-08-28 13-01-36.png>)

## Intégrité

*Les données ne sont pas altérées de façon non autorisée.*

- Le champ `notes` d'un rendez-vous peut-il être falsifié ou détourné pour
  faire exécuter du code à quelqu'un d'autre que son auteur ? (Vous allez
  vérifier concrètement ce point dans `ATTAQUES_TEMPLATE.md`.)
  
  Oui, l'utilisation du filtre |safe dans {{ rdv.notes|safe }} désactive l'échappement automatique de Django et peut permettre l'interprétation de contenu HTML non fiable. Si rdv.notes contient une donnée contrôlée par un utilisateur et stockée en base, cela peut exposer l'application à une vulnérabilité XSS stockée.

- Si deux membres du personnel modifient le même rendez-vous en même
  temps, qu'est-ce qui garantit (ou ne garantit pas) que la dernière
  écriture ne corrompt pas silencieusement les données ?

  Rien ne garantit que la dernière écriture ne corrompt pas silencieusement les données. Il n'y a pas de mécanisme de verrouillage ou de gestion des conflits pour prévenir les modifications concurrentes.
  
  Selon le besoin, on peut utiliser :
  - transaction.atomic() ;
  - select_for_update() pour verrouiller la ligne pendant une transaction ;
  - un mécanisme de verrouillage optimiste avec un champ de version ;
  - des contraintes et validations en base de données ;
  - une journalisation des modifications.

## Disponibilité

*Les services et données sont accessibles quand il le faut.*

- Que se passe-t-il si on appelle `/rendezvous/facture/99999/` avec un ID
  de patient qui n'existe pas ? (Rappel du TP2 : ceci a déjà été identifié
  comme un risque dans `RISQUES_TEMPLATE.md`.)

  Oui, si le patient 99999 n'existe pas, Django lève une exception `Patient.DoesNotExist`et 
  si cette exception n'est pas gérée, la requête peut provoquer une erreur serveur 500.
  Cela touche la disponibilité, car une entrée invalide peut provoquer l'échec de la fonctionnalité de facturation.
- Le formulaire de connexion personnel, avant correctif, a-t-il un lien
  avec la disponibilité du service pour les vrais utilisateurs autorisés,
  au-delà de la seule confidentialité ?

  Oui, Avant le correctif, il n'y avait aucune limitation des tentatives de connexion
  puis chaque tentative échouée était simplement traitée et redirigée.

  Un attaquant peut donc envoyer un très grand nombre de requêtes.

  Cela peut :

  - consommer le CPU ;
  - consommer la mémoire ;
  - augmenter les requêtes vers la base de données ;
  - ralentir la page de connexion ;
  - éventuellement contribuer à rendre le service moins disponible.

  Donc le risque n'est pas seulement la confidentialité. Une attaque massive sur l'authentification peut également affecter la disponibilité.

## Synthèse

Comme dans l'exemple du cours, remplissez ce tableau pour votre projet :

| Pilier CID | Exigence concrète pour SunuSanté | Statut actuel (respecté / à risque) |
|---|---|---|
| Confidentialité | Les données des patients doivent être accessibles uniquement aux personnes autorisées ; communications HTTPS/TLS ; protection des données sensibles ; contrôle des accès ; authentification forte pour éviter le phishing. | à risque |
| Intégrité | Les données des rendez-vous ne doivent pas pouvoir être modifiées de manière non autorisée ; supprimer l'utilisation dangereuse de `\|safe` ; gérer les modifications concurrentes ; utiliser validations, transactions et contrôles d'autorisation. | à risque |
| Disponibilité | L'application doit rester accessible malgré les erreurs et les fortes sollicitations ; gérer les `Patient.DoesNotExist` ; limiter les tentatives de connexion, prévoir du rate limiting et une protection anti-DoS. | à risque |
