"""Régénère le site et met à jour le dossier site/ publié par Netlify (préprod).

Usage : python3 scripts/maj_preprod.py          met à jour site/
        python3 scripts/maj_preprod.py --verifier  échoue si site/ n'est pas à jour (utilisé par la CI)

Le dossier site/ = dist/prod + la configuration propre à la préprod (_headers, _redirects, robots.txt),
avec une double barrière contre l'indexation : en-tête X-Robots-Tag (Netlify) et balise robots noindex dans chaque page.
"""
import os, re, shutil, subprocess, sys, filecmp, tempfile

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONFIG_PREPROD = ("_headers", "_redirects", "robots.txt")

def construire(cible):
    subprocess.run([sys.executable, os.path.join(RACINE, "build.py")], check=True, cwd=RACINE)
    prod = os.path.join(RACINE, "dist", "prod")
    shutil.copytree(prod, cible, ignore=shutil.ignore_patterns(".htaccess"))
    for f in CONFIG_PREPROD:
        shutil.copy(os.path.join(RACINE, "config", "preprod", f), os.path.join(cible, f))
    for dossier, _, fichiers in os.walk(cible):
        for nom in fichiers:
            if nom.endswith(".html"):
                p = os.path.join(dossier, nom); doc = open(p, encoding="utf-8").read()
                doc = re.sub(r'<meta name="robots" content="[^"]*">', '<meta name="robots" content="noindex, nofollow">', doc, count=1)
                open(p, "w", encoding="utf-8").write(doc)

def identiques(a, b):
    c = filecmp.dircmp(a, b)
    if c.left_only or c.right_only or c.diff_files or c.funny_files:
        print("Différences :", c.left_only, c.right_only, c.diff_files); return False
    return all(identiques(os.path.join(a, s), os.path.join(b, s)) for s in c.common_dirs)

if __name__ == "__main__":
    tmp = os.path.join(tempfile.mkdtemp(), "site")
    construire(tmp)
    site = os.path.join(RACINE, "site")
    if "--verifier" in sys.argv:
        if not identiques(tmp, site):
            print("site/ n'est pas à jour : lancez python3 scripts/maj_preprod.py et commitez."); sys.exit(1)
        print("site/ est à jour.")
    else:
        if os.path.exists(site): shutil.rmtree(site)
        shutil.copytree(tmp, site)
        print("site/ mis à jour : vérifiez avec git diff puis poussez sur main pour publier la préprod.")
