# Le triptyque CID appliqué à SunuSanté

Nom / Groupe :

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
- Le mot de passe du personnel est-il stocké et vérifié correctement
  (indice : regardez comment Django gère `User.objects.create_user`) ?

## Intégrité

*Les données ne sont pas altérées de façon non autorisée.*

- Le champ `notes` d'un rendez-vous peut-il être falsifié ou détourné pour
  faire exécuter du code à quelqu'un d'autre que son auteur ? (Vous allez
  vérifier concrètement ce point dans `ATTAQUES_TEMPLATE.md`.)
- Si deux membres du personnel modifient le même rendez-vous en même
  temps, qu'est-ce qui garantit (ou ne garantit pas) que la dernière
  écriture ne corrompt pas silencieusement les données ?

## Disponibilité

*Les services et données sont accessibles quand il le faut.*

- Que se passe-t-il si on appelle `/rendezvous/facture/99999/` avec un ID
  de patient qui n'existe pas ? (Rappel du TP2 : ceci a déjà été identifié
  comme un risque dans `RISQUES_TEMPLATE.md`.)
- Le formulaire de connexion personnel, avant correctif, a-t-il un lien
  avec la disponibilité du service pour les vrais utilisateurs autorisés,
  au-delà de la seule confidentialité ?

## Synthèse

Comme dans l'exemple du cours, remplissez ce tableau pour votre projet :

| Pilier CID | Exigence concrète pour SunuSanté | Statut actuel (respecté / à risque) |
|---|---|---|
| Confidentialité | | |
| Intégrité | | |
| Disponibilité | | |
