# yasmine-la-belle-gosses

Une lettre d'excuses d'une seule page (`index.html`) : je lui avoue que je lui ai menti
sur mon âge et sur qui j'étais, sans excuse et sans rien lui demander en retour.

**En ligne :** <https://asmaray42.github.io/yasmine-la-belle-gosses/>

## À remplir

En bas de `index.html`, le bloc `CONFIG` :

```js
const CONFIG = {
  prenom: "Yasmine",
  vraiPrenom: "",             // ton vrai prénom
  vraiAge: "",                // ton vrai âge
  autresVerites: [],          // autres choses vraies à lui dire
  mentionnerAncienSite: true, // false si elle n'a jamais vu le site de la demande en mariage
};
```

Tant que `vraiPrenom` et `vraiAge` sont vides, l'encadré « La vérité » lui propose de
tout lui dire si elle le demande. Rempli, il les affiche, et la lettre est signée de ton vrai prénom.

## Mise en ligne (GitHub Pages)

Le site est servi par GitHub Pages depuis la branche `main`, dossier racine.
À activer une seule fois : *Settings → Pages → Build and deployment* :
Source = **Deploy from a branch**, branche = `main`, dossier = `/ (root)` → **Save**.
Une minute plus tard, le site est en ligne sur <https://asmaray42.github.io/yasmine-la-belle-gosses/>.

Chaque push sur `main` met le site à jour automatiquement.
