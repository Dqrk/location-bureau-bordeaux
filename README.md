# location-bureau-bordeaux.fr

Refonte du site du Chartrons Business Center (coworking et bureaux, 9 rue André Darbon, Bordeaux).

- `site/` : site statique déployé par Netlify (préprod, `noindex`).
- `build.py` + `src/` : générateur. Python 3.12 ou plus et Pillow (`pip install -r requirements.txt`). `python3 build.py` régénère `dist/prod` et `dist/preview`, et s'arrête en erreur sur un jeton non remplacé, un « [à compléter] », un lien interne cassé ou un title / une description trop longs.
- `config/preprod/` : `_headers`, `_redirects` et `robots.txt` de la préprod Netlify.

## Mettre à jour la préprod

1. `python3 scripts/maj_preprod.py` : build, copie de `dist/prod` dans `site/`, ajout de la config préprod et d'une balise `noindex` dans chaque page.
2. `git diff` pour relire, puis commit et push sur `main` : Netlify publie.

La CI (`.github/workflows/controle.yml`) refuse un push où `site/` n'est pas à jour ou dont le HTML est invalide.

## Mise en production (OVH)

Publier le contenu de `dist/prod` (avec son `.htaccess`). Ne pas publier `site/` : il porte le `noindex` de la préprod.
