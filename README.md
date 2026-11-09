# yasmine-la-belle-gosses

Un petit site d'une seule page (`index.html`), signé Yassine : un terminal `yassine@rif`
qui « compile » une tête dure et une fierté rifaine, un rapport de bugs, un diagnostic en
JavaScript, puis **la** question… avec un bouton « Non » qui a la tête dure, lui aussi
(il finit quand même par se laisser cliquer, et propose un thé à la menthe à la place).

Elle répond en DM sur X : le site lui demande d'envoyer une capture du certificat.

Aucune dépendance, aucun serveur : c'est un fichier HTML statique.

**En ligne :** <https://asmaray42.github.io/yasmine-la-belle-gosses/>

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

## Mise en ligne (GitHub Pages)

Le site est servi par GitHub Pages depuis la branche `main`, dossier racine.
À activer une seule fois : *Settings → Pages → Build and deployment* :
Source = **Deploy from a branch**, branche = `main`, dossier = `/ (root)` → **Save**.
Une minute plus tard, le site est en ligne sur <https://asmaray42.github.io/yasmine-la-belle-gosses/>.

Chaque push sur `main` met le site à jour automatiquement.
