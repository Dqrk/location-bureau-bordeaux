# location-bureau-bordeaux.fr

Refonte du site du Chartrons Business Center (coworking et bureaux, 9 rue André Darbon, Bordeaux).

- `site/` : site statique déployé par Netlify (préprod, `noindex`).
- `build.py` + `src/` : générateur. `python3 build.py` (Python 3.12+) régénère `dist/prod` et `dist/preview`.
- `site/_headers`, `site/_redirects`, `site/robots.txt` : configuration Netlify de préprod. Pour la mise en production sur OVH, utiliser `dist/prod` (avec son `.htaccess`) et le `robots.txt` d'origine.
