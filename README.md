# yasmine-la-belle-gosses

Un petit site d'une seule page (`index.html`), signé Yassine : un terminal `yassine@rif`
qui « compile » une tête dure et une fierté rifaine, un rapport de bugs, un diagnostic en
JavaScript, puis **la** question… avec un bouton « Non » qui a la tête dure, lui aussi
(il finit quand même par se laisser cliquer, et propose un thé à la menthe à la place).

Elle répond en DM sur X : le site lui demande d'envoyer une capture du certificat.

Aucune dépendance, aucun serveur : c'est un fichier HTML statique.

**En ligne :** <https://claude.ai/artifact/TzTfYHMcZ1iEfbQqEaocEF>
(à partager via le menu *Share* de la page, en accès « toute personne ayant le lien »).

## Personnaliser

En bas de `index.html`, le bloc `CONFIG` :

```js
const CONFIG = {
  prenom: "Yasmine",
  signature: "Yassine",
};
```

Les textes (bugs, code, etc.) sont directement dans le HTML.

Pour tester : ouvre simplement `index.html` dans ton navigateur (idéalement sur ton téléphone).

## Mettre en ligne gratuitement (sans domaine, sans serveur)

### Option A : Netlify Drop (le plus simple, le repo reste privé)

1. Va sur <https://app.netlify.com/drop> et crée un compte gratuit (sinon le lien expire).
2. Glisse-dépose le dossier du projet (ou juste `index.html`).
3. Tu obtiens un lien du type `https://quelque-chose.netlify.app`.
4. *Site configuration → Change site name* pour un joli lien, par ex. `https://pour-yasmine.netlify.app`.

### Option B : GitHub Pages

GitHub Pages est gratuit pour un repo **public** (pour un repo privé, il faut GitHub Pro).

1. *Settings → General → Danger Zone → Change visibility → Public*.
2. *Settings → Pages → Build and deployment* : Source = **Deploy from a branch**,
   branche = `main` (ou `claude/awesome-volta-xbtxy5`), dossier = `/ (root)` → **Save**.
3. Après une minute, le site est en ligne sur
   <https://asmaray42.github.io/yasmine-la-belle-gosses/>

Ensuite, envoie-lui le lien en DM. L'aperçu affichera « Un petit programme pour toi ♥ ».
