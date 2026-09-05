## Partie 4 - Détecter outillé : SAST, DAST, SCA
### SAST - Semgrep
### Résultat du scan Semgrep

![alt text](<images/Capture d’écran du 2026-09-02 14-43-08.png>)

Après l'exécution du scan SAST avec **Semgrep**, aucune vulnérabilité n'a été détectée (**0 finding**).

Cependant, l'absence de résultat ne signifie pas que le code est totalement sécurisé. Dans notre cas, Semgrep n'a pas détecté :

* l'utilisation de `|safe` dans le template, qui peut introduire un risque de **XSS** lorsqu'une donnée non fiable est affichée sans échappement ;
* l'utilisation de `connection.cursor().execute(...)` dans le contexte de notre code, qui peut présenter un risque d'**injection SQL** lorsque des données utilisateur sont intégrées à la requête de manière non sécurisée ;
* l'attaque par **force brute**, car ce type d'attaque concerne principalement le comportement de l'application en fonctionnement (nombre de tentatives, absence de rate limiting, etc.) et ne peut pas être identifié uniquement par l'analyse statique du code dans notre cas.

### Ce que cela montre

Cette expérience montre que le **SAST a des limites**. Un outil comme Semgrep peut détecter certaines constructions dangereuses dans le code, mais il ne détecte pas nécessairement toutes les vulnérabilités.

Le SAST ne remplace donc :

* ni une **revue de code humaine** ;
* ni les **tests de sécurité dynamiques (DAST)** ;
* ni les tests fonctionnels et de sécurité réalisés dans différents scénarios.

Le résultat **0 vulnérabilité détectée** signifie donc uniquement que **Semgrep n'a trouvé aucune vulnérabilité correspondant aux règles utilisées lors du scan**, et non que l'application est exempte de vulnérabilités.

Lien du depot git : https://github.com/ndongombathie/TP-3-Chapitre-3-La-s-curit-comme-dimension-de-la-qualit
