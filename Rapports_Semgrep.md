## Partie 4 - Détecter outillé : SAST, DAST, SCA
### SAST - Semgrep
Apres le scan semgrep, on a trouvé 0 vulnérabilité :
il ne détecte  pasle `\|safe (XSS)` et l'injection SQL par `connection.cursor().execute(...)`
![alt text](<Capture d’écran du 2026-09-02 14-43-08.png>)

Mais le scan SAST rate la detection de l'attque par Force brute .