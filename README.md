# yasmine-la-belle-gosses

Une lettre d'excuses interactive d'une seule page (`index.html`). Elle se lit page par page
(boutons, flèches du clavier ou glisser du doigt), ou d'un coup. Il y a trois cartes à retourner
(« Tu méritais… »), et à la fin elle choisit librement : en parler, prendre du temps, ou ne plus
se parler. Chaque choix a une réponse respectueuse, et rien n'est envoyé nulle part.

**En ligne :** <https://asmaray42.github.io/yasmine-la-belle-gosses/>

## Personnaliser

En bas de `index.html`, le bloc `CONFIG` :

```js
const CONFIG = {
  prenom: "Yasmine",
  signature: "",              // vide = « Celui qui aurait dû te dire la vérité dès le début »
  mentionnerAncienSite: true, // false si elle n'a jamais vu le site de la demande en mariage
};
```

## Mise en ligne (GitHub Pages)

Le site est servi par GitHub Pages depuis la branche `main`, dossier racine.
À activer une seule fois : *Settings → Pages → Build and deployment* :
Source = **Deploy from a branch**, branche = `main`, dossier = `/ (root)` → **Save**.
Une minute plus tard, le site est en ligne sur <https://asmaray42.github.io/yasmine-la-belle-gosses/>.

Chaque push sur `main` met le site à jour automatiquement.
