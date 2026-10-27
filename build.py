# -*- coding: utf-8 -*-
"""Générateur statique du site location-bureau-bordeaux.fr.
Deux sorties : dist/preview (liens relatifs .html, pour prévisualisation)
et dist/prod (URLs propres /slug/, fichiers slug/index.html, pour l'hébergement)."""
import os, re, json, shutil, html, sys

DOMAINE = "https://www.location-bureau-bordeaux.fr"
NOM = "Coworking Bordeaux Chartrons"
MARQUE = "Location Bureau Bordeaux"
TEL = "09 72 12 57 78"
TEL_INTL = "+33972125778"
EMAIL = "contact@shared-values.fr"
ADRESSE = "9 rue André Darbon"
CP = "33300"
VILLE = "Bordeaux"
DATE_MAJ = "2026-10-27"

SRC = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- visuels
def visuel(titre, variante=0, ratio="4/3"):
    """Photo du lieu si elle existe, sinon illustration SVG neutre."""
    if titre in PHOTOS:
        cle, alt = PHOTOS[titre]
        return photo(cle, alt, prioritaire=(cle == "hero"))
    w, h = (800, 600) if ratio == "4/3" else (800, 450)
    fonds = ["#f4f4f4", "#ececec", "#f4f4f4"]
    f = fonds[variante % 3]
    corps = {
        0: f"""<rect x='60' y='120' width='680' height='300' rx='8' fill='#fff' stroke='#111111' stroke-width='3'/>
<rect x='90' y='150' width='180' height='110' rx='6' fill='#111111' opacity='.15'/><rect x='310' y='150' width='180' height='110' rx='6' fill='#111111' opacity='.15'/><rect x='530' y='150' width='180' height='110' rx='6' fill='#111111' opacity='.15'/>
<rect x='90' y='290' width='180' height='110' rx='6' fill='#111111' opacity='.25'/><rect x='310' y='290' width='180' height='110' rx='6' fill='#111111' opacity='.25'/><rect x='530' y='290' width='180' height='110' rx='6' fill='#111111' opacity='.25'/>
<rect x='60' y='440' width='680' height='14' rx='7' fill='#ed1c24'/>""",
        1: f"""<rect x='100' y='90' width='600' height='380' rx='10' fill='#fff' stroke='#111111' stroke-width='3'/>
<ellipse cx='400' cy='280' rx='210' ry='110' fill='#111111' opacity='.15'/>
<circle cx='400' cy='150' r='22' fill='#ed1c24'/><circle cx='230' cy='230' r='22' fill='#111111' opacity='.7'/><circle cx='570' cy='230' r='22' fill='#111111' opacity='.7'/><circle cx='230' cy='340' r='22' fill='#111111' opacity='.7'/><circle cx='570' cy='340' r='22' fill='#111111' opacity='.7'/><circle cx='400' cy='410' r='22' fill='#111111'/>""",
        2: f"""<rect x='120' y='60' width='560' height='440' rx='10' fill='#fff' stroke='#111111' stroke-width='3'/>
<rect x='160' y='100' width='480' height='70' rx='6' fill='#ed1c24' opacity='.9'/><rect x='160' y='190' width='480' height='70' rx='6' fill='#111111' opacity='.6'/><rect x='160' y='280' width='480' height='70' rx='6' fill='#111111' opacity='.35'/><rect x='160' y='370' width='480' height='70' rx='6' fill='#111111' opacity='.15'/>
<path d='M120 500 L400 300 L680 500' fill='none' stroke='#ed1c24' stroke-width='3' opacity='.2'/>""",
    }[variante % 3]
    return (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 {w} {h}' width='{w}' height='{h}' role='img' aria-labelledby='v{abs(hash(titre))%10**6}'>"
            f"<title id='v{abs(hash(titre))%10**6}'>{html.escape(titre)}</title><rect width='{w}' height='{h}' fill='{f}'/>{corps}"
            f"<text x='400' y='{h-40}' text-anchor='middle' font-family='system-ui,sans-serif' font-size='18' fill='#555b6b'>Photo à insérer : {html.escape(titre)}</text></svg>")

PHOTOS = {
 "L'open space lumineux du Chartrons Business Center": ("hero", "Open space lumineux avec grande table partagée, arbre d'intérieur et baies vitrées au Chartrons Business Center"),
 "L'open space de 700 m² au troisième étage": ("openspace", "Postes de travail alignés le long des baies vitrées de l'open space, avec écrans et fauteuils ergonomiques"),
 "Poste de travail équipé dans l'open space": ("bureau", "Postes de travail équipés d'écrans sur bras articulé, face aux fenêtres, avec plantes vertes"),
 "La communauté de coworkers dans l'espace détente": ("coworking", "Espace détente avec fauteuils, canapés et cabine vitrée dans l'open space"),
 "Postes de travail en open space, vue générale": ("vue", "Vue générale de l'open space avec postes de travail, canapés et végétation"),
 "Grande salle de conférence": ("grande-salle", "Grande table de réunion avec deux personnes qui travaillent, dans un espace lumineux"),
 "Salle de réunion de 6 à 8 places": ("salle-1", "Salle de réunion vitrée avec parois jaunes donnant sur l'open space"),
 "Seconde salle de réunion de 6 à 8 places": ("salle-2", "Salle de réunion vitrée vue depuis l'espace détente"),
 "Salle de réunion en configuration présentation": ("presentation", "Espace de réunion avec cabine vitrée, fauteuils et table ronde"),
 "Façade de l'immeuble rue André Darbon": ("plante", "Poste de travail devant une fenêtre avec arbre d'intérieur au Chartrons Business Center"),
 "Le quartier des Chartrons et les Bassins à flot": ("fenetre", "Baies vitrées de l'open space avec vue sur les toits du quartier des Chartrons"),
 "Coworking ou bureau fermé à Bordeaux : lequel choisir ?": ("postes", "Rangée de postes de travail équipés face aux fenêtres"),
 "S'installer aux Chartrons : le quartier vu par une entreprise": ("fenetre", "Baies vitrées de l'open space avec vue sur les toits du quartier des Chartrons"),
 "Combien coûte un bureau à Bordeaux ? Comprendre les prix": ("cuisine-ilot", "Cuisine équipée avec îlot central dans l'espace détente"),
 "Louer une salle de réunion à Bordeaux : la check-list avant de réserver": ("salle-box", "Cabine de réunion vitrée avec une personne qui travaille"),
 "Domicilier son entreprise à Bordeaux : adresse, bureau ou siège ?": ("lounge", "Salon de l'espace détente avec fauteuils colorés et panneaux acoustiques"),
 "Télétravail et bureau partagé : organiser une équipe hybride à Bordeaux": ("detente", "Espace détente et postes de travail de l'open space, avec canapés"),
}
PHOTO_PREFIX = "assets/img/photos/"
PHOTO_COMPTEUR = [0]
def photo(cle, alt, prioritaire=False, sizes="(max-width: 860px) 100vw, (max-width: 1220px) 50vw, 570px"):
    PHOTO_COMPTEUR[0] += 1
    if PHOTO_COMPTEUR[0] == 1: prioritaire = True
    p = PHOTO_PREFIX_ACTIF + cle
    attrs = 'fetchpriority="high" decoding="async"' if prioritaire else 'loading="lazy" decoding="async"'
    return (f'<img src="{p}-800.webp" srcset="{p}-600.webp 600w, {p}-800.webp 800w, {p}-1000.webp 1000w, {p}-1600.webp 1600w" sizes="{sizes}" '
            f'width="1000" height="667" alt="{html.escape(alt)}" {attrs}>')
PHOTO_PREFIX_ACTIF = PHOTO_PREFIX

ICONES = {
    "bureau": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><rect x='3' y='4' width='18' height='12' rx='2'/><path d='M3 20h18M8 16v4M16 16v4'/></svg>",
    "cowork": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><circle cx='9' cy='8' r='3'/><circle cx='17' cy='10' r='2.5'/><path d='M3 20c0-3.3 2.7-6 6-6s6 2.7 6 6M14 20c0-2.2 1.3-4 3-4s3 1.8 3 4'/></svg>",
    "reunion": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><rect x='3' y='5' width='18' height='11' rx='2'/><path d='M8 21h8M12 16v5'/></svg>",
    "fibre": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M2 9a15 15 0 0 1 20 0M5.5 12.5a10 10 0 0 1 13 0M9 16a5 5 0 0 1 6 0'/><circle cx='12' cy='19.5' r='1'/></svg>",
    "telico": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M5 3h4l2 5-2.5 1.5a11 11 0 0 0 6 6L16 13l5 2v4a2 2 0 0 1-2 2A17 17 0 0 1 3 5a2 2 0 0 1 2-2z'/></svg>",
    "cafe": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M4 8h12v6a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM16 10h2a2 2 0 0 1 0 4h-2M7 3v2M11 3v2'/></svg>",
    "tram": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><rect x='5' y='3' width='14' height='15' rx='3'/><path d='M5 11h14M8 21l1-3M16 21l-1-3'/><circle cx='9' cy='15' r='1'/><circle cx='15' cy='15' r='1'/></svg>",
    "parking": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><rect x='3' y='3' width='18' height='18' rx='3'/><path d='M9 17V7h4a3 3 0 0 1 0 6H9'/></svg>",
    "pmr": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><circle cx='12' cy='4' r='2'/><path d='M10 8l1 6h5l2 6M9 12a5 5 0 1 0 6 6'/></svg>",
    "impression": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M6 9V3h12v6M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2'/><rect x='6' y='14' width='12' height='7'/></svg>",
    "securite": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M12 2l8 3v6c0 5-3.5 9-8 11-4.5-2-8-6-8-11V5z'/><path d='M9 12l2 2 4-4'/></svg>",
    "clim": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M12 2v20M2 12h20M5 5l14 14M19 5L5 19'/></svg>",
    "pin": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><path d='M12 22s7-6.5 7-12a7 7 0 1 0-14 0c0 5.5 7 12 7 12z'/><circle cx='12' cy='10' r='2.5'/></svg>",
    "mail": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><rect x='3' y='5' width='18' height='14' rx='2'/><path d='M3 7l9 6 9-6'/></svg>",
    "horloge": "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor' stroke-width='2' aria-hidden='true'><circle cx='12' cy='12' r='9'/><path d='M12 7v5l3 2'/></svg>",
}
LOGO_SVG = "<svg viewBox='0 0 40 40' aria-hidden='true'><rect width='40' height='40' rx='9' fill='#111111'/><path d='M11 29V11h5v13h8v5zM26 11h4v9l-4 3z' fill='#fff'/></svg>"

# ---------------------------------------------------------------- pages
# Chaque page : slug ('' = accueil), title, description, h1, chapo, corps (html), extras json-ld, nav (label dans le menu ou None)
PAGES = []
def page(**kw): PAGES.append(kw); return kw

def jsonld_org(abs_url):
    return {
        "@context": "https://schema.org",
        "@type": ["CoworkingSpace", "LocalBusiness", "Organization"],
        "hasMap": "https://www.google.com/maps/search/?api=1&query=9+rue+Andr%C3%A9+Darbon+33300+Bordeaux",
        "@id": DOMAINE + "/#organisation",
        "name": NOM,
        "alternateName": [MARQUE, "Chartrons Business Center"],
        "description": "Location de bureaux équipés, coworking et salles de réunion dans un open space de 700 m² au cœur du quartier des Chartrons à Bordeaux.",
        "url": DOMAINE + "/",
        "telephone": TEL_INTL,
        "email": EMAIL,
        "priceRange": "à partir de 350 € HT / mois",
        "image": abs_url("assets/img/og.jpg"),
        "logo": abs_url("assets/logo.svg"),
        "address": {"@type": "PostalAddress", "streetAddress": ADRESSE, "postalCode": CP, "addressLocality": VILLE, "addressRegion": "Nouvelle-Aquitaine", "addressCountry": "FR"},
        "areaServed": {"@type": "City", "name": "Bordeaux"},
        "parentOrganization": {"@type": "Organization", "name": "Shared Values"},
        "knowsAbout": ["location de bureaux", "coworking", "salles de réunion", "domiciliation d'équipe"],
        "makesOffer": [
            {"@type": "Offer", "name": "Poste de travail équipé en open space", "price": "350", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "350", "priceCurrency": "EUR", "unitText": "mois HT, premier poste", "valueAddedTaxIncluded": False}},
            {"@type": "Offer", "name": "Poste supplémentaire", "price": "300", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "300", "priceCurrency": "EUR", "unitText": "mois HT par poste", "valueAddedTaxIncluded": False}},
            {"@type": "Offer", "name": "Place de parking en garage couvert", "price": "130", "priceCurrency": "EUR", "priceSpecification": {"@type": "UnitPriceSpecification", "price": "130", "priceCurrency": "EUR", "unitText": "mois HT", "valueAddedTaxIncluded": False}},
        ],
        "amenityFeature": [{"@type": "LocationFeatureSpecification", "name": n, "value": True} for n in ["Fibre optique", "Salles de réunion", "Parking couvert", "Local vélos", "Ascenseur et accès PMR", "Climatisation réversible", "Espace détente"]],
    }

# ----- Accueil
page(slug="", nav="Accueil",
     title="Coworking et bureaux à Bordeaux Chartrons dès 350 € HT",
     description="Bureaux équipés, coworking et 9 salles de réunion dans un open space de 700 m² aux Chartrons, Bordeaux. Fibre, parking, tram. Dès 350 € HT. Visitez.",
     h1="Location de bureaux et coworking à Bordeaux, quartier des Chartrons",
     chapo="Le Chartrons Business Center propose des postes de travail équipés, du coworking et neuf salles de réunion dans un open space lumineux de 700 m², au dernier étage d'un immeuble d'architecte. Premier poste à 350 € HT par mois, tout compris.",
     corps="""
<section class="section">
  <div class="conteneur">
    <div class="en-tete-section centre">
      <span class="etiquette">Nos espaces</span>
      <h2>Trois façons de travailler aux Chartrons</h2>
      <p class="intro">Un poste fixe pour votre équipe, un bureau en coworking pour un indépendant, un poste en flex office pour une journée, ou une salle de réunion : le Chartrons Business Center s'adapte à votre rythme.</p>
    </div>
    <div class="grille grille-3">
      <article class="carte carte-photo"><div class="carte-visuel">{photo:bureau:Postes de travail équipés face aux fenêtres de l'open space}</div><h3><a class="carte-lien" href="{u:location-bureaux-bordeaux}">Bureaux équipés</a></h3><p>Un poste de travail neuf de 160 × 80 cm, un fauteuil ergonomique, la fibre et les salles de réunion incluses. Pour une personne ou une équipe de dix.</p><a class="lien" href="{u:location-bureaux-bordeaux}">Voir les bureaux</a></article>
      <article class="carte carte-photo"><div class="carte-visuel">{photo:coworking:Espace détente du coworking avec canapés et cabine vitrée}</div><h3><a class="carte-lien" href="{u:coworking-bordeaux-chartrons}">Coworking</a></h3><p>Sortez de chez vous, rejoignez une communauté d'indépendants, de start-up et de cabinets de conseil, et partagez les coûts d'un vrai bureau.</p><a class="lien" href="{u:coworking-bordeaux-chartrons}">Découvrir le coworking</a></article>
      <article class="carte carte-photo"><div class="carte-visuel">{photo:salle-box:Cabine de réunion vitrée avec une personne au travail}</div><h3><a class="carte-lien" href="{u:salles-de-reunion-bordeaux}">Salles de réunion</a></h3><p>Une grande salle de 16 à 20 places en mode conférence et huit salles de 6 à 8 places, équipées pour la présentation et l'audioconférence.</p><a class="lien" href="{u:salles-de-reunion-bordeaux}">Réserver une salle</a></article>
    </div>
    <div class="encadre" style="margin-top:2rem"><p><strong>Flex office à la demande.</strong> Besoin d'un poste pour une journée, une semaine ou quelques jours par mois, sans engagement ? Réservez un poste en open space quand vous en avez besoin, avec les mêmes services que les résidents. <a href="{u:coworking-bordeaux-chartrons}#flex-office">En savoir plus sur le flex office</a>.</p></div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur deux-colonnes">
    <div class="visuel">{v:L'open space de 700 m² au troisième étage:0}</div>
    <div>
      <span class="etiquette">Le lieu</span>
      <h2>Un open space de 700 m² au dernier étage, baigné de lumière</h2>
      <p>Le Chartrons Business Center occupe le troisième et dernier étage d'un immeuble d'architecte livré en 2007, au 9 rue André Darbon à Bordeaux. Il accueille un incubateur éco-créatif de jeunes entreprises du numérique, ainsi que des cabinets de conseil en ressources humaines, en droit et en gestion de patrimoine.</p>
      <ul class="liste-coches">
        <li>Parking couvert, local vélos et deux-roues, ascenseur</li>
        <li>Climatisation réversible et contrôle d'accès sécurisé</li>
        <li>Tram B (arrêt Chartrons) et tram C (arrêt Camille Godard) à quelques minutes à pied</li>
        <li>Écoles de commerce et d'informatique à proximité pour recruter stagiaires et alternants</li>
      </ul>
      <div class="btn-groupe"><a class="btn" href="{u:chartrons-business-center}">Découvrir le lieu et l'accès</a></div>
    </div>
  </div>
</section>

<section class="section section-nuit">
  <div class="conteneur">
    <div class="en-tete-section centre"><span class="etiquette">En chiffres</span><h2>Ce que vous trouvez au Chartrons Business Center</h2></div>
    <div class="chiffres">
      <div><strong>700 m²</strong><span>d'open space lumineux au dernier étage</span></div>
      <div><strong>3</strong><span>salles de réunion, de 6 à 20 personnes</span></div>
      <div><strong>350 €</strong><span>HT par mois pour le premier poste, tout inclus</span></div>
      <div><strong>2 lignes</strong><span>de tram (B et C) et 2 lignes de bus (4 et 15)</span></div>
    </div>
    <ul class="galerie" aria-label="Photos de l'espace">
      <li>{photo:cuisine:Cuisine de l'espace détente avec îlot central et deux personnes qui échangent}</li>
      <li>{photo:plafond-vert:Mur végétal suspendu au plafond de l'open space}</li>
      <li>{photo:lounge:Salon de l'espace détente avec fauteuils et panneaux acoustiques colorés}</li>
      <li>{photo:salle-1:Salle de réunion vitrée aux parois jaunes}</li>
    </ul>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="en-tete-section centre"><span class="etiquette">Services inclus</span><h2>Tout est compris dans le loyer, sans option cachée</h2><p class="intro">Le prix d'un poste couvre le mobilier, la connexion, les salles de réunion et l'espace de vie. Seuls le parking, la téléphonie fixe et les impressions sont facturés en plus, à l'usage.</p></div>
    <div class="grille grille-4">
      <div class="carte"><div class="icone">{fibre}</div><h3>Fibre optique illimitée</h3><p>Connexion très haut débit par fibre, doublée d'une ligne ADSL de secours et du Wi-Fi dans tout l'espace.</p></div>
      <div class="carte"><div class="icone">{reunion}</div><h3>Salles de réunion incluses</h3><p>Accès libre aux salles jusqu'à 8 personnes, équipées pour la présentation et l'audioconférence.</p></div>
      <div class="carte"><div class="icone">{impression}</div><h3>Impression et scan</h3><p>Imprimante haute définition partagée et scan vers e-mail gratuit. Impressions facturées à la page.</p></div>
      <div class="carte"><div class="icone">{cafe}</div><h3>Espace détente</h3><p>Salle de vie avec babyfoot, thé et café : l'endroit où l'on se croise, le midi et entre deux dossiers.</p></div>
    </div>
    <div class="btn-groupe" style="justify-content:center"><a class="btn btn-secondaire" href="{u:services}">Voir tous les services</a></div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section centre"><span class="etiquette">Tarifs</span><h2>Des tarifs simples et dégressifs</h2><p class="intro">Un seul tarif par poste de travail équipé en open space, dégressif à partir du deuxième poste. Pas de frais de dossier, pas de surprise.</p></div>
    <div class="grille grille-3">
      <div class="tarif"><h3>Premier poste</h3><p class="prix">350 € <small>HT</small></p><p class="unite">par mois, poste de travail équipé</p><ul class="liste-coches"><li>Bureau 160 × 80 cm et fauteuil ergonomique</li><li>Fibre, Wi-Fi, impression et scan</li><li>Salles de réunion et espace détente</li></ul><a class="btn" href="{u:contact}">Demander un devis</a></div>
      <div class="tarif mis-en-avant"><span class="badge">Équipes</span><h3>Postes supplémentaires</h3><p class="prix">300 € <small>HT</small></p><p class="unite">par mois et par poste, dès le deuxième</p><ul class="liste-coches"><li>Mêmes prestations que le premier poste</li><li>Postes regroupés pour votre équipe</li><li>Idéal de 2 à 10 collaborateurs</li></ul><a class="btn" href="{u:contact}">Installer mon équipe</a></div>
      <div class="tarif"><h3>Options à l'usage</h3><p class="prix">dès 10 € <small>HT</small></p><p class="unite">par mois, selon l'option</p><ul class="liste-coches"><li>Téléphone IP fixe : 10 € ou 20 € HT / mois</li><li>Parking en garage couvert : 130 € HT / mois</li><li>Impression : 0,04 € HT (noir) ou 0,12 € HT (couleur) la page</li></ul><a class="btn btn-secondaire" href="{u:tarifs}">Voir le détail des tarifs</a></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="en-tete-section centre"><span class="etiquette">Témoignages</span><h2>Ils travaillent aux Chartrons et en parlent</h2></div>
    <div class="grille grille-3">
      {temoignages:3}
    </div>
    <div class="btn-groupe" style="justify-content:center"><a class="btn btn-secondaire" href="{u:temoignages}">Lire tous les témoignages</a></div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section centre"><span class="etiquette">Questions fréquentes</span><h2>Avant de venir visiter</h2></div>
    <div class="faq">{faq:accueil}</div>
    <div class="btn-groupe" style="justify-content:center"><a class="btn btn-secondaire" href="{u:faq}">Toutes les questions fréquentes</a></div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="cta"><div><h2>Venez visiter l'open space</h2><p>Une visite de 30 minutes suffit pour se projeter. Appelez-nous ou laissez vos coordonnées, nous vous rappelons dans la journée.</p></div><div class="btn-groupe"><a class="btn btn-blanc" href="{u:contact}">Réserver une visite</a><a class="btn btn-blanc" href="tel:{tel_intl}">{tel}</a></div></div>
  </div>
</section>
""")

# ----- Bureaux
page(slug="location-bureaux-bordeaux", nav="Bureaux",
     title="Bureaux équipés à Bordeaux Chartrons dès 350 € HT",
     description="Poste de travail équipé aux Chartrons : bureau neuf, fauteuil ergonomique, fibre et salles de réunion incluses, de 1 à 10 personnes. Demandez un devis.",
     h1="Location de bureaux équipés à Bordeaux, aux Chartrons",
     chapo="Un poste de travail prêt à l'emploi dans un open space de 700 m², avec tout ce qu'il faut pour travailler dès le premier jour : mobilier neuf, fibre optique, salles de réunion et espace détente inclus. Tarifs 2026 : premier poste à 350 € HT par mois, postes suivants à 300 € HT.",
     corps="""
<section class="section">
  <div class="conteneur deux-colonnes">
    <div>
      <span class="etiquette">Le poste de travail</span>
      <h2>Qu'est-ce qui est compris dans un bureau équipé ?</h2>
      <p>Chaque poste de travail loué au Chartrons Business Center comprend un bureau neuf de 160 × 80 cm avec cloison de courtoisie, un fauteuil ergonomique synchrone réglable (dossier, assise, accoudoirs) et un emplacement dans l'open space lumineux du troisième étage. La connexion internet très haut débit, l'impression, le scan vers e-mail et l'accès aux salles de réunion sont inclus dans le loyer.</p>
      <ul class="liste-coches">
        <li>Bureau 160 × 80 cm neuf avec cloison de courtoisie</li>
        <li>Fauteuil ergonomique synchrone, dossier et accoudoirs réglables</li>
        <li>Internet illimité : fibre optique, ADSL de secours et Wi-Fi</li>
        <li>Impression haute définition et scan vers e-mail</li>
        <li>Salles de réunion jusqu'à 8 personnes en accès libre</li>
        <li>Salle de vie, local vélos et deux-roues</li>
      </ul>
    </div>
    <div class="visuel">{v:Poste de travail équipé dans l'open space:0}</div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Pour qui ?</span><h2>Un bureau pour une personne ou pour toute une équipe</h2></div>
    <div class="grille grille-3">
      <div class="carte"><div class="icone">{cowork}</div><h3>Indépendants et consultants</h3><p>Un poste fixe, une adresse professionnelle aux Chartrons et des voisins avec qui échanger. Vous louez un seul poste, sans engagement de surface.</p></div>
      <div class="carte"><div class="icone">{bureau}</div><h3>Start-up et petites équipes</h3><p>De 2 à 10 postes regroupés dans l'open space, à 300 € HT par mois le poste supplémentaire. Vous ajoutez un poste quand vous recrutez, sans changer de locaux.</p></div>
      <div class="carte"><div class="icone">{securite}</div><h3>Antennes régionales</h3><p>Une implantation à Bordeaux sans bail commercial ni travaux : vos collaborateurs disposent d'un bureau, d'une ligne fixe et de salles de réunion pour recevoir vos clients.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Bureau équipé ou bail classique ?</span><h2>Pourquoi louer un poste plutôt que des locaux ?</h2></div>
    <table>
      <caption>Comparaison entre un poste équipé au Chartrons Business Center et une location de bureaux classique</caption>
      <thead><tr><th scope="col">Critère</th><th scope="col">Poste équipé aux Chartrons</th><th scope="col">Bail commercial classique</th></tr></thead>
      <tbody>
        <tr><td data-label="Critère">Engagement</td><td data-label="Chartrons">Mensuel, un poste à la fois</td><td data-label="Bail">Bail 3-6-9 ans, dépôt de garantie</td></tr>
        <tr><td data-label="Critère">Mobilier et installation</td><td data-label="Chartrons">Inclus, prêt le jour de l'arrivée</td><td data-label="Bail">À acheter, à installer, à assurer</td></tr>
        <tr><td data-label="Critère">Internet et téléphonie</td><td data-label="Chartrons">Fibre incluse, ligne fixe en option</td><td data-label="Bail">Abonnement, délai de raccordement</td></tr>
        <tr><td data-label="Critère">Salles de réunion</td><td data-label="Chartrons">Neuf salles incluses</td><td data-label="Bail">Surface à louer et à équiper</td></tr>
        <tr><td data-label="Critère">Charges, ménage, énergie</td><td data-label="Chartrons">Comprises dans le loyer</td><td data-label="Bail">En plus du loyer</td></tr>
        <tr><td data-label="Critère">Évolution de l'équipe</td><td data-label="Chartrons">Un poste de plus en quelques jours</td><td data-label="Bail">Déménagement ou sous-location</td></tr>
      </tbody>
    </table>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Comment ça se passe</span><h2>S'installer en trois étapes</h2></div>
    <ol class="etapes">
      <li><h3>Visite de l'open space</h3><p>Vous découvrez l'espace, les salles et l'équipe en place. Comptez 30 minutes, sur rendez-vous.</p></li>
      <li><h3>Devis et contrat</h3><p>Nous vous envoyons un devis au nombre de postes, avec les options utiles (parking, ligne fixe). Le contrat est mensuel.</p></li>
      <li><h3>Installation</h3><p>Votre poste est prêt à votre arrivée : bureau, fauteuil, accès Wi-Fi et badge. Vous travaillez dès le premier matin.</p></li>
    </ol>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Questions fréquentes</span><h2>Louer un bureau aux Chartrons</h2></div>
    <div class="faq">{faq:bureaux}</div>
  </div>
</section>
{cta}
""")

# ----- Coworking
page(slug="coworking-bordeaux-chartrons", nav="Coworking",
     title="Coworking à Bordeaux Chartrons | 700 m², dès 350 € HT",
     description="Coworking aux Chartrons à Bordeaux : poste fixe dans un open space de 700 m², indépendants et start-up, fibre et salles incluses. Visitez.",
     h1="Coworking à Bordeaux, dans le quartier des Chartrons",
     chapo="Le coworking du Chartrons Business Center réunit indépendants, fondateurs de start-up et cabinets de conseil dans un open space de 700 m². On y partage les coûts d'un vrai bureau, un réseau professionnel et une salle de vie où l'on se croise le midi. Tarif 2026 : 350 € HT par mois le poste, tout compris.",
     corps="""
<section class="section">
  <div class="conteneur deux-colonnes">
    <div class="visuel">{v:La communauté de coworkers dans l'espace détente:1}</div>
    <div>
      <span class="etiquette">Le principe</span>
      <h2>Qu'est-ce que le coworking, concrètement ?</h2>
      <p>Le coworking consiste à partager un espace de travail entre professionnels qui n'appartiennent pas à la même entreprise. Au Chartrons Business Center, chaque coworker dispose d'un poste fixe et équipé dans l'open space, et met en commun le reste : la connexion fibre, les salles de réunion, l'imprimante, la salle de vie et le parking.</p>
      <p>L'intérêt dépasse la simple économie. Les indépendants sortent de leur domicile, retrouvent un cadre de travail et une frontière entre vie pro et vie perso. Les fondateurs de jeunes entreprises trouvent des voisins avec des métiers complémentaires : développeurs, juristes, consultants RH, graphistes, gestionnaires de patrimoine.</p>
    </div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Ce qui change</span><h2>Pourquoi rejoindre un coworking plutôt que travailler chez soi ?</h2></div>
    <div class="grille grille-3">
      <div class="carte"><div class="icone">{cowork}</div><h3>Un réseau qui travaille pour vous</h3><p>Les coworkers s'échangent des contacts, des clients et des coups de main. Un juriste à deux bureaux du vôtre, un développeur en face : les questions se règlent au café.</p></div>
      <div class="carte"><div class="icone">{bureau}</div><h3>Un cadre professionnel</h3><p>Une adresse aux Chartrons, une salle de réunion pour recevoir un client, une ligne fixe : vous présentez une structure solide, même en solo.</p></div>
      <div class="carte"><div class="icone">{cafe}</div><h3>Une vraie coupure</h3><p>Le midi, on se retrouve dans la salle de vie autour d'un café ou du babyfoot. Le soir, on rentre chez soi et on ferme vraiment la journée.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur deux-colonnes inverse">
    <div class="visuel">{v:Postes de travail en open space, vue générale:0}</div>
    <div>
      <span class="etiquette">Qui est là ?</span>
      <h2>Une communauté de métiers complémentaires</h2>
      <p>L'immeuble abrite un incubateur éco-créatif dédié aux jeunes entreprises du numérique, et l'open space accueille des profils variés : éditeurs de logiciels, agences web et marketing, consultants en ressources humaines, avocats, gestionnaires de patrimoine, graphistes indépendants, acteurs du vin et de l'agroalimentaire.</p>
      <p>Des entreprises comme Azendoo, Alumn Force, Oenopia, Fimco ou le Studio Malette Graphique y ont installé leurs équipes. Leurs retours sont à lire sur la page <a href="{u:temoignages}">témoignages</a>.</p>
      <div class="btn-groupe"><a class="btn" href="{u:contact}">Réserver une visite</a></div>
    </div>
  </div>
</section>

<section class="section" id="flex-office">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Flex office</span><h2>Le flex office à la demande : un poste quand vous en avez besoin</h2><p class="intro">Vous travaillez surtout chez vous ou en déplacement, mais vous avez besoin d'un vrai bureau de temps en temps ? Le flex office à la demande vous donne accès à un poste équipé en open space, à la journée ou à la demi-journée, sans engagement de durée.</p></div>
    <div class="grille grille-3">
      <div class="carte"><div class="icone">{bureau}</div><h3>Un poste prêt à l'emploi</h3><p>Vous arrivez avec votre ordinateur, vous repartez le soir. Bureau, fauteuil ergonomique, fibre et Wi-Fi, impression et espace détente : tout est là.</p></div>
      <div class="carte"><div class="icone">{cowork}</div><h3>Sans engagement</h3><p>Pas de bail, pas de mois minimum. Vous réservez une journée, une semaine ou quelques jours par mois, selon votre activité du moment.</p></div>
      <div class="carte"><div class="icone">{cafe}</div><h3>Pour qui ?</h3><p>Indépendants en télétravail, consultants de passage à Bordeaux, salariés en déplacement, équipes qui se retrouvent un jour par semaine. Le flex office complète le poste fixe, il ne le remplace pas.</p></div>
    </div>
    <p style="margin-top:2rem">Les tarifs du flex office sont communiqués sur demande, selon le nombre de jours. <a href="{u:contact}">Demandez vos dates</a> et nous vous confirmons la disponibilité dans la journée.</p>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Tarif</span><h2>Combien coûte un poste en coworking aux Chartrons ?</h2><p class="intro">Le poste de coworking est facturé 350 € HT par mois, charges, fibre, salles de réunion et espace détente compris. À partir du deuxième poste, chaque poste supplémentaire revient à 300 € HT par mois. Une place de parking couvert s'ajoute en option pour 130 € HT par mois.</p></div>
    <div class="btn-groupe"><a class="btn" href="{u:tarifs}">Voir tous les tarifs</a><a class="btn btn-secondaire" href="{u:location-bureaux-bordeaux}">Voir les bureaux pour les équipes</a></div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Questions fréquentes</span><h2>Le coworking aux Chartrons</h2></div>
    <div class="faq">{faq:coworking}</div>
  </div>
</section>
{cta}
""")

# ----- Salles de réunion
page(slug="salles-de-reunion-bordeaux", nav="Salles de réunion",
     title="Salles de réunion à Bordeaux Chartrons, 6 à 20 personnes",
     description="Neuf salles de réunion aux Chartrons à Bordeaux, de 6 à 20 personnes, écran et audioconférence. Incluses pour les résidents, sur devis pour les autres.",
     h1="Salles de réunion à Bordeaux, aux Chartrons",
     chapo="Le Chartrons Business Center dispose de neuf salles de réunion : une grande salle de 16 à 20 personnes en configuration conférence, et des salles de 6 à 8 personnes équipées pour la présentation et l'audioconférence. Les résidents y accèdent librement ; les entreprises extérieures peuvent les réserver sur demande.",
     corps="""
<section class="section">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Neuf salles</span><h2>Quelle salle de réunion pour quel usage ?</h2></div>
    <div class="grille grille-3">
      <article class="carte"><div class="visuel" style="margin-bottom:1.2rem">{v:Grande salle de conférence:2}</div><h3>Grande salle de conférence</h3><p><strong>16 à 20 personnes</strong> en configuration conférence. Pour une formation, un comité, une présentation client ou une assemblée.</p><ul class="liste-coches"><li>Écran de présentation</li><li>Audioconférence</li><li>Lumière naturelle, climatisation</li></ul></article>
      <article class="carte"><div class="visuel" style="margin-bottom:1.2rem">{v:Salle de réunion de 6 à 8 places:1}</div><h3>Salles de réunion de 6 à 8 places</h3><p><strong>6 à 8 personnes</strong> autour d'une table. Pour un point d'équipe, un entretien de recrutement ou un rendez-vous client.</p><ul class="liste-coches"><li>Écran et présentation sans fil</li><li>Audioconférence</li><li>Incluse pour les résidents</li></ul></article>
      <article class="carte"><div class="visuel" style="margin-bottom:1.2rem">{v:Seconde salle de réunion de 6 à 8 places:1}</div><h3>Salles pour les rendez-vous courts</h3><p><strong>6 à 8 personnes</strong>, même équipement. Avec neuf salles, personne n'attend la sienne, même en fin de matinée.</p><ul class="liste-coches"><li>Écran et présentation sans fil</li><li>Audioconférence</li><li>Incluse pour les résidents</li></ul></article>
    </div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur deux-colonnes">
    <div>
      <span class="etiquette">Fonctionnement</span>
      <h2>Comment réserver une salle de réunion ?</h2>
      <p><strong>Vous êtes résident</strong> (poste de bureau ou coworking) : les salles jusqu'à 8 personnes sont incluses dans votre loyer et se réservent sur le planning partagé, sans frais.</p>
      <p>Avant de réserver, parcourez notre <a href="{u:guide-louer-salle-de-reunion-bordeaux}">check-list pour louer une salle de réunion à Bordeaux</a>.</p>
      <p><strong>Vous n'êtes pas résident</strong> : contactez-nous par téléphone au <a href="tel:{tel_intl}">{tel}</a> ou via le <a href="{u:contact}">formulaire</a> en précisant la date, la durée et le nombre de participants. Nous vous confirmons la disponibilité et le tarif dans la journée.</p>
      <ul class="liste-coches">
        <li>Accès au bâtiment sécurisé, ascenseur et accès PMR</li>
        <li>Parking couvert sur demande pour vos participants</li>
        <li>Tram B et C et bus 4 et 15 à quelques minutes</li>
        <li>Thé et café dans la salle de vie</li>
      </ul>
    </div>
    <div class="visuel">{v:Salle de réunion en configuration présentation:2}</div>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Questions fréquentes</span><h2>Les salles de réunion</h2></div>
    <div class="faq">{faq:salles}</div>
  </div>
</section>
{cta}
""")

# ----- Services
page(slug="services", nav="Services",
     title="Services inclus dans votre bureau à Bordeaux Chartrons",
     description="Tout ce que comprend votre bureau aux Chartrons : fibre, salles de réunion, impression, espace détente, local vélos, accès PMR. Parking en option.",
     h1="Les services inclus dans votre bureau aux Chartrons",
     chapo="Au Chartrons Business Center, le loyer d'un poste couvre l'essentiel : mobilier, connexion fibre, salles de réunion, impression et espace de vie. Le parking, la téléphonie fixe et les impressions sont les seules options facturées, à l'usage.",
     corps="""
<section class="section">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Au quotidien</span><h2>Dix services compris ou en option</h2></div>
    <div class="grille grille-2">
      <div class="carte"><div class="icone">{bureau}</div><h3>Open space de 700 m² aux Chartrons</h3><p>Des bureaux équipés au troisième et dernier étage, avec de la lumière naturelle toute la journée. Chaque poste comprend un bureau neuf de 160 × 80 cm avec cloison de courtoisie et un fauteuil ergonomique synchrone.</p></div>
      <div class="carte"><div class="icone">{reunion}</div><h3>Neuf salles de réunion</h3><p>Une grande salle de 16 à 20 places en mode conférence et des salles de 6 à 8 places, équipées pour la présentation et l'audioconférence. Les salles jusqu'à 8 personnes sont incluses pour les résidents.</p><a class="lien" href="{u:salles-de-reunion-bordeaux}">Voir les salles</a></div>
      <div class="carte"><div class="icone">{fibre}</div><h3>Fibre optique illimitée</h3><p>Connexion très haut débit par fibre optique, illimitée, avec une ligne ADSL de secours et le Wi-Fi dans tout l'espace. Le téléchargement illégal et le pair-à-pair sont interdits par le règlement intérieur.</p></div>
      <div class="carte"><div class="icone">{telico}</div><h3>Téléphonie fixe et fax</h3><p>Une ligne fixe dédiée par poste, en option : téléphone IP avec appels illimités vers les fixes en France, aux États-Unis et dans de nombreux pays d'Europe (10 € HT / mois), ou vers les fixes et mobiles (20 € HT / mois). Fax disponible.</p></div>
      <div class="carte"><div class="icone">{impression}</div><h3>Impression et scan</h3><p>Imprimante haute définition partagée, scan vers e-mail gratuit. Les impressions sont facturées à la page : 0,04 € HT en noir et blanc, 0,12 € HT en couleur.</p></div>
      <div class="carte"><div class="icone">{cafe}</div><h3>Espace détente</h3><p>Une salle de vie avec babyfoot, thé et café, où les résidents se retrouvent le midi. C'est là que naissent la plupart des collaborations entre voisins de bureau.</p></div>
      <div class="carte"><div class="icone">{tram}</div><h3>Proche du tramway</h3><p>Tram B à l'arrêt Chartrons, tram C à l'arrêt Camille Godard, bus 4 et 15 à l'arrêt Picard. La gare Saint-Jean est à 20 minutes en tram.</p><a class="lien" href="{u:chartrons-business-center}">Voir l'accès</a></div>
      <div class="carte"><div class="icone">{parking}</div><h3>Parking, vélos et deux-roues</h3><p>Place de parking en garage couvert en option (130 € HT par mois). Local sécurisé pour les vélos, scooters et motos, inclus.</p></div>
      <div class="carte"><div class="icone">{pmr}</div><h3>Accès handicapés et PMR</h3><p>L'immeuble dispose d'un ascenseur desservant l'open space au troisième étage et de circulations adaptées aux personnes à mobilité réduite.</p></div>
      <div class="carte"><div class="icone">{clim}</div><h3>Climatisation et sécurité</h3><p>Climatisation réversible dans tout l'espace, contrôle d'accès et systèmes de sécurité modernes dans un immeuble d'architecte livré en 2007.</p></div>
    </div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Inclus ou en option ?</span><h2>Ce que couvre le loyer, et ce qui s'ajoute</h2></div>
    <table>
      <caption>Prestations incluses dans le loyer d'un poste et options facturées à l'usage</caption>
      <thead><tr><th scope="col">Prestation</th><th scope="col">Statut</th><th scope="col" class="prix">Tarif</th></tr></thead>
      <tbody>
        <tr><td data-label="Prestation">Bureau 160 × 80 cm et fauteuil ergonomique</td><td data-label="Statut">Inclus</td><td data-label="Tarif" class="prix">0 €</td></tr>
        <tr><td data-label="Prestation">Fibre optique, ADSL de secours, Wi-Fi</td><td data-label="Statut">Inclus</td><td data-label="Tarif" class="prix">0 €</td></tr>
        <tr><td data-label="Prestation">Salles de réunion jusqu'à 8 personnes</td><td data-label="Statut">Inclus</td><td data-label="Tarif" class="prix">0 €</td></tr>
        <tr><td data-label="Prestation">Scan vers e-mail, espace détente, local vélos</td><td data-label="Statut">Inclus</td><td data-label="Tarif" class="prix">0 €</td></tr>
        <tr><td data-label="Prestation">Téléphone IP, appels illimités vers les fixes</td><td data-label="Statut">Option</td><td data-label="Tarif" class="prix">10 € HT / mois</td></tr>
        <tr><td data-label="Prestation">Téléphone IP, appels illimités fixes et mobiles</td><td data-label="Statut">Option</td><td data-label="Tarif" class="prix">20 € HT / mois</td></tr>
        <tr><td data-label="Prestation">Place de parking en garage couvert</td><td data-label="Statut">Option</td><td data-label="Tarif" class="prix">130 € HT / mois</td></tr>
        <tr><td data-label="Prestation">Impression noir et blanc / couleur</td><td data-label="Statut">À l'usage</td><td data-label="Tarif" class="prix">0,04 € / 0,12 € HT la page</td></tr>
      </tbody>
    </table>
    <div class="btn-groupe"><a class="btn" href="{u:tarifs}">Voir la page tarifs</a></div>
  </div>
</section>
{cta}
""")

# ----- Tarifs
page(slug="tarifs", nav="Tarifs",
     title="Tarifs bureaux et coworking à Bordeaux dès 350 € HT",
     description="Premier poste équipé 350 € HT par mois, postes suivants 300 € HT, parking 130 € HT, téléphonie dès 10 € HT. Sans frais de dossier. Demandez un devis.",
     h1="Tarifs des bureaux et du coworking aux Chartrons",
     chapo="Un seul tarif par poste de travail équipé en open space, dégressif dès le deuxième poste. Le loyer comprend le mobilier, la fibre, les salles de réunion et l'espace détente. Les prix sont indiqués hors taxes.",
     corps="""
<section class="section">
  <div class="conteneur">
    <div class="deux-colonnes" style="margin-bottom:3rem"><div class="visuel">{v:Poste de travail équipé dans l'open space:0}</div><div><span class="etiquette">Ce que vous louez</span><h2>Un poste équipé, tout compris</h2><p>Chaque poste comprend un bureau neuf de 160 × 80 cm, un fauteuil ergonomique, la fibre, l'impression, l'accès aux salles de réunion jusqu'à 8 personnes et à l'espace détente. Les tarifs ci-dessous sont ceux en vigueur en 2026.</p></div></div>
    <div class="grille grille-3">
      <div class="tarif"><h2 class="h3">Premier poste</h2><p class="prix">350 € <small>HT</small></p><p class="unite">par mois, poste de travail équipé en open space</p><ul class="liste-coches"><li>Bureau neuf 160 × 80 cm, cloison de courtoisie</li><li>Fauteuil ergonomique synchrone réglable</li><li>Fibre, ADSL de secours et Wi-Fi illimités</li><li>Impression HD et scan vers e-mail</li><li>Salles de réunion jusqu'à 8 personnes</li><li>Espace détente, local vélos et deux-roues</li></ul><a class="btn" href="{u:contact}">Demander un devis</a></div>
      <div class="tarif mis-en-avant"><span class="badge">Équipes</span><h2 class="h3">Postes supplémentaires</h2><p class="prix">300 € <small>HT</small></p><p class="unite">par mois et par poste, à partir du deuxième</p><ul class="liste-coches"><li>Mêmes prestations que le premier poste</li><li>Postes regroupés dans l'open space</li><li>Ajout d'un poste en quelques jours</li><li>Exemple : 3 postes = 950 € HT / mois</li><li>Exemple : 5 postes = 1 550 € HT / mois</li></ul><a class="btn" href="{u:contact}">Installer mon équipe</a></div>
      <div class="tarif"><h2 class="h3">Salle de réunion</h2><p class="prix">Sur devis</p><p class="unite">pour les entreprises non résidentes</p><ul class="liste-coches"><li>Grande salle 16 à 20 personnes</li><li>Huit salles de 6 à 8 personnes</li><li>Écran, audioconférence, Wi-Fi</li><li>Incluse pour les résidents jusqu'à 8 personnes</li></ul><a class="btn btn-secondaire" href="{u:salles-de-reunion-bordeaux}">Voir les salles</a></div>
    </div>
    <div class="encadre" style="margin-top:2rem"><p><strong>Flex office à la demande.</strong> Un poste équipé en open space à la journée ou à la demi-journée, sans engagement, pour les indépendants et les salariés de passage. Tarif sur demande selon le nombre de jours : <a href="{u:contact}">indiquez-nous vos dates</a>.</p></div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Options</span><h2>Options et consommations, facturées à l'usage</h2></div>
    <table>
      <caption>Options disponibles en plus du loyer d'un poste (prix hors taxes sauf mention contraire)</caption>
      <thead><tr><th scope="col">Option</th><th scope="col">Détail</th><th scope="col" class="prix">Prix</th></tr></thead>
      <tbody>
        <tr><td data-label="Option">Téléphone IP, formule fixes</td><td data-label="Détail">Poste Thomson ST2030, appels illimités vers les fixes en France, aux États-Unis et dans de nombreux pays d'Europe, conférence téléphonique</td><td data-label="Prix" class="prix">10 € HT / mois</td></tr>
        <tr><td data-label="Option">Téléphone IP, formule fixes et mobiles</td><td data-label="Détail">Appels illimités vers les fixes et les mobiles en France, aux États-Unis et dans de nombreux pays d'Europe</td><td data-label="Prix" class="prix">20 € HT / mois</td></tr>
        <tr><td data-label="Option">Place de parking</td><td data-label="Détail">Garage couvert et sécurisé dans l'immeuble</td><td data-label="Prix" class="prix">130 € HT / mois</td></tr>
        <tr><td data-label="Option">Impression noir et blanc</td><td data-label="Détail">Imprimante haute définition partagée</td><td data-label="Prix" class="prix">0,04 € HT la page</td></tr>
        <tr><td data-label="Option">Impression couleur</td><td data-label="Détail">Imprimante haute définition partagée</td><td data-label="Prix" class="prix">0,12 € HT la page</td></tr>
      </tbody>
    </table>
    <p class="meta">Tarifs en vigueur au {date_fr}. Les prix sont exprimés hors taxes, TVA de 20 % en sus. Devis personnalisé sur demande pour les équipes de plus de cinq postes et pour la location ponctuelle de salles. Pour comparer un prix au poste et un loyer au m², lisez <a href="{u:guide-prix-bureau-bordeaux}">Combien coûte un bureau à Bordeaux ?</a></p>
  </div>
</section>

<section class="section">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Questions fréquentes</span><h2>Tarifs et conditions</h2></div>
    <div class="faq">{faq:tarifs}</div>
  </div>
</section>
{cta}
""")

# ----- Le lieu
page(slug="chartrons-business-center", nav="Le lieu",
     title="Le lieu et l'accès | Chartrons Business Center, Bordeaux",
     description="Immeuble d'architecte, 9 rue André Darbon, Bordeaux Chartrons : open space de 700 m², parking couvert, ascenseur, tram B et C. Plan d'accès.",
     h1="Le Chartrons Business Center, à Bordeaux",
     chapo="Le Chartrons Business Center est situé au 9 rue André Darbon, à Bordeaux, dans le quartier des Chartrons, à deux pas des Bassins à flot. L'immeuble, conçu par un architecte et livré en 2007, appartient à Shared Values et abrite un incubateur éco-créatif de jeunes entreprises du numérique.",
     corps="""
<section class="section">
  <div class="conteneur deux-colonnes">
    <div>
      <span class="etiquette">L'immeuble</span>
      <h2>Un immeuble d'architecte, pensé pour le travail</h2>
      <p>Livré en 2007, l'immeuble réunit sur quatre niveaux des entreprises du numérique, des cabinets de conseil en ressources humaines, des avocats et des gestionnaires de patrimoine. L'open space du Chartrons Business Center occupe le troisième et dernier étage, le plus lumineux, sur 700 m².</p>
      <ul class="liste-coches">
        <li>Parking couvert en sous-sol, local vélos, scooters et motos</li>
        <li>Ascenseur et accès adapté aux personnes à mobilité réduite</li>
        <li>Climatisation réversible dans tous les espaces</li>
        <li>Contrôle d'accès et systèmes de sécurité modernes</li>
        <li>Incubateur éco-créatif au sein du bâtiment</li>
      </ul>
    </div>
    <div class="visuel">{v:Façade de l'immeuble rue André Darbon:2}</div>
  </div>
</section>

<section class="section section-gris">
  <div class="conteneur">
    <div class="en-tete-section"><span class="etiquette">Accès</span><h2>Comment venir au 9 rue André Darbon ?</h2></div>
    <div class="grille grille-3">
      <div class="carte"><div class="icone">{tram}</div><h3>En tramway et en bus</h3><ul><li><strong>Tram B</strong>, arrêt Chartrons</li><li><strong>Tram C</strong>, arrêt Camille Godard</li><li><strong>Bus 4 et 15</strong>, arrêt Picard</li></ul><p>Depuis la gare Saint-Jean, comptez une vingtaine de minutes en tram C direction Bassins à flot (horaires sur <a href="https://www.infotbm.com/" rel="noopener">infotbm.com</a>).</p></div>
      <div class="carte"><div class="icone">{parking}</div><h3>En voiture</h3><p>Accès par les boulevards ou par les quais (quai de Bacalan). Place de parking en garage couvert sur abonnement (130 € HT par mois) et stationnement visiteurs possible dans le quartier.</p></div>
      <div class="carte"><div class="icone">{pin}</div><h3>À vélo</h3><p>Pistes cyclables sur les quais jusqu'aux Bassins à flot, local vélos sécurisé dans l'immeuble, stations V³ à proximité.</p></div>
    </div>
    <div style="margin-top:2rem">
      <h3>Adresse</h3>
      <address class="prose">{nom}<br>{adresse}<br>{cp} {ville}<br>Téléphone : <a href="tel:{tel_intl}">{tel}</a></address>
      <div class="carte-plan" id="plan"><button class="btn" type="button" id="charger-plan" style="margin:2rem">Afficher le plan Google Maps</button></div>
      <p class="meta">Le plan est chargé à la demande pour respecter votre vie privée et accélérer la page. <a href="https://www.google.com/maps/search/?api=1&amp;query=9+rue+Andr%C3%A9+Darbon+33300+Bordeaux" rel="noopener" target="_blank">Ouvrir l'itinéraire dans Google Maps</a> (nouvelle fenêtre).</p>
    </div>
  </div>
</section>

<section class="section">
  <div class="conteneur deux-colonnes inverse">
    <div class="visuel">{v:Le quartier des Chartrons et les Bassins à flot:1}</div>
    <div>
      <span class="etiquette">Le quartier</span>
      <h2>Pourquoi s'installer aux Chartrons ?</h2>
      <p>Les Chartrons sont l'ancien quartier des négociants en vin de Bordeaux, entre le centre historique et les Bassins à flot (où se trouve la <a href="https://www.laciteduvin.com/" rel="noopener">Cité du Vin</a>). Le quartier a gardé ses échoppes et ses antiquaires, et accueille aujourd'hui des agences, des start-up et des écoles. Les restaurants et commerces de la rue Notre-Dame et des quais sont à quelques minutes à pied.</p>
      <p>Pour une entreprise, c'est une adresse reconnue à Bordeaux, bien desservie, avec des écoles de commerce et d'informatique à proximité qui facilitent le recrutement de stagiaires et d'alternants.</p>
      <div class="btn-groupe"><a class="btn" href="{u:contact}">Organiser une visite</a><a class="btn btn-secondaire" href="{u:guide-quartier-chartrons-entreprise}">Lire notre guide du quartier</a></div>
    </div>
  </div>
</section>
""")

# ----- Témoignages
page(slug="temoignages", nav="Témoignages",
     title="Avis des entreprises installées aux Chartrons, Bordeaux",
     description="Avis des indépendants et entreprises installés aux Chartrons à Bordeaux : lumière, cadre de vie, échanges entre métiers, salle de repos. Venez visiter.",
     h1="Ils travaillent aux Chartrons et en parlent",
     chapo="Indépendants, fondateurs de start-up, dirigeants de PME : voici ce que les résidents du Chartrons Business Center retiennent de leur installation à Bordeaux.",
     corps="""
<section class="section">
  <div class="conteneur">
    <div class="visuel" style="margin-bottom:2.5rem">{v:La communauté de coworkers dans l'espace détente:1}</div>
    <h2 class="visually-hidden">Les témoignages</h2>
    <div class="grille grille-3">{temoignages:7}</div>
  </div>
</section>
<section class="section section-gris">
  <div class="conteneur centre">
    <span class="etiquette">Ils nous font confiance</span>
    <h2>Des entreprises de tous les secteurs</h2>
    <ul class="logos">{logos}</ul>
  </div>
</section>
{cta}
""")

# ----- FAQ
page(slug="faq", nav="FAQ",
     title="FAQ location de bureaux et coworking à Bordeaux Chartrons",
     description="Tarifs, engagement, salles de réunion, parking, accès, horaires, domiciliation : les réponses sur la location de bureaux et le coworking aux Chartrons.",
     h1="Questions fréquentes sur la location de bureaux aux Chartrons",
     chapo="Tout ce que l'on nous demande avant une visite : prix, engagement, salles, accès et vie dans l'open space. Si votre question n'y figure pas, appelez-nous au " + TEL + ".",
     corps="""
<section class="section">
  <div class="conteneur">
    <h2 class="visually-hidden">Toutes les questions</h2>
    <div class="faq">{faq:toutes}</div>
  </div>
</section>
{cta}
""")

# ----- Guide (hub)
page(slug="guide", nav="Guide",
     title="Guide : choisir et louer un bureau à Bordeaux",
     description="Coworking ou bureau fermé, prix au poste, quartier, domiciliation, équipe hybride : nos guides pour choisir un espace de travail à Bordeaux.",
     h1="Le guide pour bien choisir son bureau à Bordeaux",
     chapo="Des articles de fond pour comparer les solutions, comprendre les prix et choisir le bon quartier avant de vous installer.",
     corps="""
<section class="section">
  <div class="conteneur">
    <h2 class="visually-hidden">Les articles du guide</h2>
    <div class="grille grille-3">{articles}</div>
  </div>
</section>
{cta}
""")

ARTICLES = [
 dict(slug="guide-coworking-ou-bureau-ferme-bordeaux", date="2026-10-27", temps="6 min",
      title="Coworking ou bureau fermé à Bordeaux : lequel choisir ?",
      description="Coworking, poste en open space ou bureau fermé à Bordeaux : coûts, engagement et profils concernés. Un comparatif pour choisir selon votre équipe.",
      h1="Coworking ou bureau fermé à Bordeaux : lequel choisir ?",
      chapo="Un indépendant, une start-up de quatre personnes et un cabinet de dix collaborateurs n'ont pas les mêmes besoins. Voici comment trancher entre coworking, poste en open space et bureau fermé, avec les ordres de grandeur de prix à Bordeaux.",
      corps="""
<h2>Les trois solutions en une phrase</h2>
<p><strong>Le coworking</strong> est un poste dans un espace partagé entre professionnels de structures différentes, loué au mois. <strong>Le poste en open space pour équipe</strong> regroupe plusieurs postes d'une même entreprise dans un espace partagé, avec des services communs. <strong>Le bureau fermé</strong> est une pièce privative, louée en bail commercial ou dans un centre d'affaires.</p>
<h2>Combien ça coûte à Bordeaux ?</h2>
<p>Au Chartrons Business Center, <a href="{u:tarifs}">un poste équipé en open space</a> coûte 350 € HT par mois pour le premier poste et 300 € HT par mois pour chacun des suivants, charges, fibre et salles de réunion comprises. À titre de comparaison, un bail commercial classique suppose un loyer au mètre carré, auquel s'ajoutent les charges, l'énergie, le ménage, l'abonnement internet, le mobilier et un dépôt de garantie, pour un engagement de trois ans minimum.</p>
<div class="encadre"><p>Pour une équipe de quatre personnes, le coût mensuel d'un espace partagé aux Chartrons se calcule simplement : 350 € + 3 × 300 € = 1 250 € HT par mois, sans investissement de départ.</p></div>
<h2>Quel profil pour quelle solution ?</h2>
<h3>Vous êtes indépendant ou consultant</h3>
<p>Le coworking répond à trois besoins : sortir de chez soi, disposer d'une adresse et d'une salle pour recevoir des clients, et rencontrer d'autres professionnels. Un poste fixe suffit, sans engagement de surface.</p>
<h3>Vous lancez une start-up ou une petite agence</h3>
<p>L'open space pour équipe permet d'ajouter un poste à chaque recrutement sans déménager. Les salles de réunion incluses évitent de louer une surface que l'on n'utilise que deux heures par semaine.</p>
<h3>Vous avez besoin de confidentialité</h3>
<p>Un cabinet qui reçoit des clients pour des entretiens sensibles ou une équipe qui passe sa journée au téléphone sera plus à l'aise avec un bureau fermé ou une organisation mixte : postes en open space et salle réservée pour les échanges confidentiels. Les salles de 6 à 8 personnes du Chartrons Business Center servent souvent à cela.</p>
<h2>Les questions à se poser avant de choisir</h2>
<ul>
  <li>Combien de personnes seront présentes au bureau en même temps, dans six mois ?</li>
  <li>Combien de rendez-vous clients recevez-vous par semaine sur place ?</li>
  <li>Vos collaborateurs viennent-ils en voiture, en tram ou à vélo ?</li>
  <li>Avez-vous besoin d'une ligne fixe et d'une adresse pour votre siège social ?</li>
  <li>Quel engagement pouvez-vous prendre : un mois, un an, trois ans ?</li>
</ul>
<h2>Notre conseil</h2>
<p>Commencez par le plus léger. Un poste en coworking ou en open space se transforme en plusieurs postes en quelques jours ; un bail commercial se renégocie difficilement. Et venez visiter : la lumière, le bruit et l'ambiance d'un espace ne se devinent pas sur une fiche.</p>
"""),
 dict(slug="guide-quartier-chartrons-entreprise", date="2026-10-27", temps="5 min",
      title="S'installer aux Chartrons : le quartier pour une entreprise",
      description="Pourquoi s'installer aux Chartrons à Bordeaux : accès en tram, Bassins à flot, écoles, restaurants, image de marque. Repères pour une entreprise.",
      h1="S'installer aux Chartrons : le quartier vu par une entreprise",
      chapo="Les Chartrons attirent agences, start-up et cabinets de conseil depuis une quinzaine d'années. Voici ce que le quartier offre à une entreprise qui cherche des bureaux à Bordeaux, et ce qu'il faut savoir avant d'y poser ses cartons.",
      corps="""
<h2>Où sont les Chartrons ?</h2>
<p>Le quartier des Chartrons s'étend au nord du centre historique de Bordeaux, le long de la Garonne, entre le quai des Chartrons et le cours du Médoc, jusqu'aux Bassins à flot. C'est l'ancien quartier des négociants en vin, dont les chais ont été transformés en logements, en bureaux et en lieux culturels.</p>
<h2>Un quartier très bien desservi</h2>
<p>Deux lignes de tram traversent le secteur : la ligne B (arrêt Chartrons) et la ligne C (arrêt Camille Godard), complétées par les bus 4 et 15 (plan du <a href="https://www.infotbm.com/" rel="noopener">réseau TBM</a>). Depuis la gare Saint-Jean, le tram C rejoint les Bassins à flot en une vingtaine de minutes. Les quais aménagés offrent une piste cyclable continue jusqu'au centre-ville.</p>
<h2>Ce que l'on y trouve autour du bureau</h2>
<ul>
  <li>Les restaurants et cafés de la rue Notre-Dame et du quai des Chartrons pour les déjeuners d'équipe</li>
  <li>Les Bassins à flot et la Cité du Vin pour recevoir un client ou organiser un séminaire</li>
  <li>Les Halles de Bacalan et les commerces de bouche</li>
  <li>Des écoles de commerce, d'informatique et de design à proximité, sources de stagiaires et d'alternants</li>
</ul>
<h2>Une image de marque pour votre entreprise</h2>
<p>Une adresse aux Chartrons dit quelque chose de votre entreprise : un quartier créatif, central, reconnu des Bordelais, sans être le quartier d'affaires standardisé. C'est l'une des raisons pour lesquelles des éditeurs de logiciels, des agences et des cabinets de conseil ont choisi le Chartrons Business Center, au 9 rue André Darbon, qui héberge aussi un incubateur éco-créatif.</p>
<h2>Les points de vigilance</h2>
<p>Le stationnement en voirie est limité, comme partout dans le centre de Bordeaux : un parking couvert dans l'immeuble change la vie des collaborateurs qui viennent en voiture. Les loyers des bureaux fermés y sont plus élevés qu'en périphérie, ce qui plaide pour les formules partagées quand l'équipe est petite ou évolutive.</p>
<div class="encadre"><p>Au Chartrons Business Center, la place de parking en garage couvert coûte 130 € HT par mois, et le local vélos et deux-roues est inclus.</p></div>
"""),
 dict(slug="guide-prix-bureau-bordeaux", date="2026-10-27", temps="5 min",
      title="Combien coûte un bureau à Bordeaux ? Prix au poste, au m²",
      description="Prix d'un bureau à Bordeaux : loyer au poste en coworking, loyer au m² en bail commercial, coûts cachés. Méthode et exemple chiffré pour une équipe.",
      h1="Combien coûte un bureau à Bordeaux ? Comprendre les prix",
      chapo="Comparer un prix au poste et un prix au mètre carré est le premier piège quand on cherche des bureaux. Voici comment lire les offres, ce que cache un loyer, et un exemple de calcul pour une équipe de cinq personnes à Bordeaux.",
      corps="""
<h2>Deux façons d'afficher un prix</h2>
<p><strong>Le prix au poste</strong> est utilisé par les espaces de coworking et les centres d'affaires : un montant mensuel par personne, en général tout compris. Au Chartrons Business Center, il est de 350 € HT par mois pour le premier poste et de 300 € HT pour chaque poste supplémentaire.</p>
<p><strong>Le prix au mètre carré</strong> est utilisé pour les baux commerciaux : un loyer annuel hors taxes et hors charges par m², à multiplier par la surface louée. Il faut ensuite ajouter tout ce qui n'est pas dans le loyer.</p>
<h2>Ce qu'un loyer au m² ne comprend pas</h2>
<ul>
  <li>Les charges de l'immeuble (entretien, gardiennage, ascenseur) et la taxe foncière souvent refacturée</li>
  <li>L'énergie, le chauffage et la climatisation</li>
  <li>Le ménage et les consommables</li>
  <li>L'abonnement internet et la téléphonie, avec un délai de raccordement</li>
  <li>Le mobilier, l'aménagement et parfois des travaux</li>
  <li>Le dépôt de garantie et les honoraires d'agence</li>
  <li>L'assurance des locaux</li>
</ul>
<h2>Exemple de calcul pour une équipe de cinq personnes</h2>
<p>En <a href="{u:location-bureaux-bordeaux}">espace partagé aux Chartrons</a> : 350 € + 4 × 300 € = <strong>1 550 € HT par mois</strong>, mobilier, fibre, salles de réunion et charges compris, avec un engagement mensuel. Ajoutez 130 € HT par place de parking si besoin.</p>
<p>En bail commercial, il faut compter environ 10 à 12 m² par poste, soit 50 à 60 m² pour cinq personnes, plus une salle de réunion. Le loyer n'est que la première ligne : une fois les charges, l'énergie, internet, le ménage et l'amortissement du mobilier ajoutés, le coût réel par poste est souvent plus élevé que le prix affiché, pour un engagement de trois ans minimum.</p>
<div class="encadre"><p>La bonne question n'est pas « quel est le loyer ? » mais « combien me coûte chaque poste, tout compris, chaque mois, et pour quelle durée d'engagement ? ».</p></div>
<h2>Quand le bail classique redevient pertinent</h2>
<p>À partir d'une quinzaine de collaborateurs stables, ou si votre activité exige des locaux spécifiques (atelier, stockage, accueil du public), un bail commercial retrouve son intérêt. En dessous, une formule au poste est presque toujours plus souple et plus prévisible.</p>
<p>Pour vérifier avec vos chiffres, <a href="{u:contact}">demandez un devis</a> : nous vous répondons dans la journée avec un montant mensuel ferme.</p>
"""),
 dict(slug="guide-louer-salle-de-reunion-bordeaux", date="2026-10-27", temps="4 min",
      title="Louer une salle de réunion à Bordeaux : la check-list",
      description="Capacité, équipement, accès en tram, parking, pauses : les 8 points à vérifier avant de réserver une salle de réunion à Bordeaux. Check-list pratique.",
      h1="Louer une salle de réunion à Bordeaux : la check-list avant de réserver",
      chapo="Une réunion ratée commence souvent par une salle mal choisie : trop petite, sans écran, introuvable en tram. Voici les huit points à vérifier avant de réserver, et ce que proposent les salles du Chartrons Business Center.",
      corps="""
<h2>1. La capacité réelle, selon la configuration</h2>
<p>Une salle annoncée pour 20 personnes en mode conférence (rangées face à l'écran) n'en accueille que 10 à 12 autour d'une table. Précisez toujours le format : conférence, table en U, réunion autour d'une table. Aux Chartrons, la grande salle accueille 16 à 20 personnes en conférence, et les deux petites salles 6 à 8 personnes autour d'une table.</p>
<h2>2. L'équipement de présentation</h2>
<p>Un écran, une connexion sans fil ou un câble pour votre ordinateur, l'audioconférence pour les participants à distance, et une connexion fibre stable : ce sont les quatre indispensables. Vérifiez aussi la présence d'un paperboard ou d'un tableau blanc si vous animez un atelier.</p>
<h2>3. L'accès pour vos participants</h2>
<p>À Bordeaux, l'accès en tram est décisif : vos participants arrivent de la gare Saint-Jean, du centre ou de l'aéroport. Le Chartrons Business Center est desservi par le tram B (arrêt Chartrons), le tram C (arrêt Camille Godard) et les bus 4 et 15. Pour ceux qui viennent en voiture, demandez s'il existe un parking dans l'immeuble.</p>
<h2>4. L'accessibilité PMR</h2>
<p>Ascenseur, largeur des portes, sanitaires adaptés : posez la question avant de réserver, surtout pour une formation ouverte au public. L'immeuble des Chartrons dispose d'un ascenseur jusqu'au troisième étage.</p>
<h2>5. La lumière et le confort</h2>
<p>Une salle aveugle fatigue vite. Privilégiez la lumière naturelle et une climatisation réversible pour les journées d'été comme d'hiver.</p>
<h2>6. Les pauses et le déjeuner</h2>
<p>Thé, café, et un espace où sortir de la salle font la différence sur une journée complète. Aux Chartrons, la salle de vie est à disposition et les restaurants de la rue Notre-Dame et des quais sont à quelques minutes à pied.</p>
<h2>7. La durée et la souplesse de réservation</h2>
<p>Demi-journée, journée, soirée : vérifiez les créneaux proposés et la possibilité de prolonger si la réunion déborde. Les résidents du Chartrons Business Center réservent les petites salles librement sur le planning partagé.</p>
<h2>8. Le prix, tout compris ?</h2>
<p>Comparez des devis qui incluent la même chose : équipement, Wi-Fi, boissons, accueil. Au Chartrons Business Center, les salles jusqu'à 8 personnes sont incluses dans le loyer des résidents ; pour une entreprise extérieure, un devis est envoyé dans la journée.</p>
<div class="encadre"><p>Pour réserver : appelez le """ + TEL + """ ou utilisez le <a href="{u:contact}">formulaire de contact</a> en précisant la date, la durée, le nombre de participants et le format souhaité.</p></div>
"""),
 dict(slug="guide-domiciliation-entreprise-bordeaux", date="2026-10-27", temps="5 min",
      title="Domicilier son entreprise à Bordeaux : quelle option ?",
      description="Domiciliation à Bordeaux : adresse seule, bureau loué ou siège social, justificatifs à fournir, intérêt d'une adresse aux Chartrons.",
      h1="Domicilier son entreprise à Bordeaux : adresse, bureau ou siège ?",
      chapo="Le siège social d'une entreprise doit être une adresse réelle. À Bordeaux, trois options s'offrent au créateur : son domicile, une société de domiciliation ou un espace de bureaux. Voici comment les comparer.",
      corps="""
<h2>Ce que dit la règle</h2>
<p>Toute société doit déclarer un siège social, qui figure sur le Kbis, les factures et les contrats. Cette adresse détermine le greffe compétent et le lieu de réception des courriers officiels. Elle doit correspondre à un lieu où l'entreprise a le droit de s'installer : un domicile sous conditions, un local loué ou un contrat de domiciliation.</p>
<h2>Option 1 : domicilier chez soi</h2>
<p>C'est gratuit et simple au démarrage, mais l'adresse personnelle apparaît sur tous les documents publics, et certains baux d'habitation ou règlements de copropriété limitent l'activité à domicile. Pour un indépendant qui ne reçoit pas de clients, cela peut suffire les premiers mois.</p>
<h2>Option 2 : une société de domiciliation</h2>
<p>Une adresse commerciale et la réception du courrier, sans bureau. L'avantage est le prix ; la limite est l'absence de lieu de travail et de salle pour recevoir. Le contrat de domiciliation et l'agrément préfectoral du domiciliataire sont demandés par le greffe.</p>
<h2>Option 3 : louer un poste et domicilier dans ses bureaux</h2>
<p>En louant <a href="{u:location-bureaux-bordeaux}">un poste dans un espace de bureaux</a>, l'entreprise dispose d'une adresse, d'un lieu de travail et de salles de réunion, et peut, sous conditions, y fixer son siège social. Au Chartrons Business Center, la domiciliation du siège peut être étudiée pour les résidents qui louent un poste : parlez-en lors de la visite pour connaître les conditions et les justificatifs à fournir.</p>
<h2>Les justificatifs habituellement demandés</h2>
<ul>
  <li>Le contrat de location ou de domiciliation au nom de la société</li>
  <li>Une attestation de l'occupant ou du propriétaire des locaux</li>
  <li>Pour un domicile, un justificatif et l'absence d'interdiction dans le bail</li>
</ul>
<h2>Pourquoi une adresse aux Chartrons compte</h2>
<p>L'adresse est le premier signal envoyé à un client ou à un recruteur. Un siège au 9 rue André Darbon, dans un quartier reconnu de Bordeaux, dans un immeuble qui abrite un incubateur et des cabinets de conseil, pose une structure crédible dès la première facture, pour le prix d'un poste de travail.</p>
<div class="encadre"><p>Cet article donne des repères généraux. Pour votre situation, vérifiez les conditions auprès du greffe du tribunal de commerce de Bordeaux ou de votre expert-comptable, et consultez la fiche officielle sur <a href="https://entreprendre.service-public.fr/vosdroits/F2160" rel="noopener">la domiciliation d'une entreprise (service-public.fr)</a>.</p></div>
"""),
 dict(slug="guide-equipe-hybride-coworking-bordeaux", date="2026-10-27", temps="5 min",
      title="Équipe hybride à Bordeaux : télétravail et bureau",
      description="Dimensionner des bureaux pour une équipe en télétravail partiel à Bordeaux : postes, jours de présence, salles, et l'intérêt de l'espace partagé.",
      h1="Télétravail et bureau partagé : organiser une équipe hybride à Bordeaux",
      chapo="Depuis que le télétravail s'est installé, la question n'est plus « faut-il des bureaux ? » mais « combien de postes, pour quels jours, et pour quoi faire ? ». Voici une méthode simple pour dimensionner l'espace d'une équipe hybride, et ce que change un espace partagé.",
      corps="""
<h2>Partir des jours de présence, pas des effectifs</h2>
<p>Une équipe de huit personnes présentes deux jours par semaine n'a pas besoin de huit postes. Listez les jours de présence de chacun, repérez le jour de pointe, et dimensionnez sur ce jour. Souvent, cinq ou six postes suffisent pour huit collaborateurs, à condition de fixer un ou deux jours communs.</p>
<h2>Fixer des jours d'équipe</h2>
<p>Le bureau hybride sert d'abord à se voir. Décidez d'un ou deux jours où toute l'équipe est sur place, et réservez ces jours aux réunions, aux ateliers et aux arrivées de nouveaux collaborateurs. Les autres jours, le bureau devient un lieu de concentration pour ceux qui ne peuvent pas travailler chez eux.</p>
<h2>Prévoir les salles plutôt que les mètres carrés</h2>
<p>En mode hybride, les réunions mélangent présents et distants. Une salle équipée pour l'audioconférence et la présentation vaut plus que des mètres carrés d'open space en plus. Au Chartrons Business Center, des salles de 6 à 8 personnes sont incluses pour les résidents, et une grande salle de 16 à 20 personnes accueille les journées d'équipe.</p>
<h2>Pourquoi l'espace partagé convient à l'hybride</h2>
<ul>
  <li>Vous louez le nombre de postes du jour de pointe, pas un local dimensionné pour tout le monde</li>
  <li>Vous ajoutez ou retirez un poste au mois, quand l'organisation change</li>
  <li>La fibre, les salles et l'imprimante sont déjà là, sans projet d'aménagement</li>
  <li>Les collaborateurs isolés en télétravail retrouvent des collègues et des voisins d'autres métiers</li>
</ul>
<h2>Exemple</h2>
<p>Une agence de huit personnes fixe le mardi et le jeudi comme jours d'équipe, avec six postes loués aux Chartrons : 350 € + 5 × 300 € = 1 850 € HT par mois. Les salles de réunion incluses accueillent les points clients, la grande salle est réservée pour le séminaire trimestriel.</p>
<h2>Les règles à écrire noir sur blanc</h2>
<p>Qui vient quel jour, comment on réserve un poste ou une salle, ce qu'on laisse ou non sur le bureau le soir : trois règles simples évitent la plupart des frictions. Un poste fixe par personne présente plus de deux jours par semaine, et des postes partagés pour les autres, est souvent le bon compromis.</p>
<div class="encadre"><p>Pour chiffrer votre configuration, <a href="{u:contact}">demandez un devis</a> en indiquant le nombre de postes au jour de pointe. Nous répondons dans la journée.</p></div>
"""),
]

for _a in ARTICLES:
    _a["temps"] = f"{max(2, round(len(re.sub(r'<[^>]+>', ' ', _a['corps']).split()) / 220))} min"

# ----- Contact
page(slug="contact", nav="Contact",
     title="Contact et visite | Chartrons Business Center, Bordeaux",
     description="Demandez une visite ou un devis pour un bureau, un poste de coworking ou une salle de réunion aux Chartrons, Bordeaux. Réponse dans la journée.",
     h1="Contact : demander une visite ou un devis",
     chapo="Appelez-nous, ou laissez vos coordonnées et le nombre de postes souhaité : nous vous rappelons dans la journée pour fixer une visite ou vous envoyer un devis.",
     corps="""
<section class="section">
  <div class="conteneur mise-en-page">
    <div>
      <h2>Votre demande</h2>
      <form class="formulaire" action="#" method="post" novalidate>
        <p class="meta">Les champs marqués d'un <span class="obligatoire" aria-hidden="true">*</span> astérisque sont obligatoires.</p>
        <div class="ligne">
          <div><label for="nom">Nom et prénom <span class="obligatoire" aria-hidden="true">*</span></label><input id="nom" name="nom" type="text" autocomplete="name" required aria-required="true"></div>
          <div><label for="societe">Entreprise</label><input id="societe" name="societe" type="text" autocomplete="organization"></div>
        </div>
        <div class="ligne">
          <div><label for="email">E-mail <span class="obligatoire" aria-hidden="true">*</span></label><input id="email" name="email" type="email" autocomplete="email" required aria-required="true" aria-describedby="aide-email"><p class="aide" id="aide-email">Pour vous envoyer le devis.</p></div>
          <div><label for="telephone">Téléphone</label><input id="telephone" name="telephone" type="tel" autocomplete="tel" aria-describedby="aide-tel"><p class="aide" id="aide-tel">Pour vous rappeler plus vite.</p></div>
        </div>
        <div class="ligne">
          <div><label for="besoin">Votre besoin <span class="obligatoire" aria-hidden="true">*</span></label><select id="besoin" name="besoin" required aria-required="true"><option value="">Choisir</option><option>Un poste en coworking</option><option>Des bureaux pour une équipe</option><option>Une salle de réunion</option><option>Une visite, sans engagement</option><option>Autre demande</option></select></div>
          <div><label for="postes">Nombre de postes</label><input id="postes" name="postes" type="number" min="1" max="50" inputmode="numeric"></div>
        </div>
        <div><label for="message">Message</label><textarea id="message" name="message" rows="5" placeholder="Date d'arrivée souhaitée, options utiles (parking, ligne fixe), questions"></textarea></div>
        <label class="consentement"><input type="checkbox" name="consentement" required aria-required="true"><span>J'accepte que mes informations soient utilisées pour traiter ma demande, conformément à la <a href="{u:politique-de-confidentialite}">politique de confidentialité</a>. <span class="obligatoire" aria-hidden="true">*</span></span></label>
        <div><button class="btn" type="submit">Envoyer ma demande</button></div>
      </form>
    </div>
    <aside class="aside" aria-label="Coordonnées">
      <div class="carte">
        <h2 style="font-size:1.2rem">Nous joindre</h2>
        <ul class="coordonnees">
          <li>{telico}<span><strong>Téléphone</strong><br><a href="tel:{tel_intl}">{tel}</a></span></li>
          <li>{mail_ico}<span><strong>E-mail</strong><br><a href="mailto:{email}">{email}</a></span></li>
          <li>{pin_ico}<address style="font-style:normal"><strong>Adresse</strong><br>{nom}<br>{adresse}<br>{cp} {ville}</address></li>
          <li>{horloge_ico}<span><strong>Visites</strong><br>Du lundi au vendredi, sur rendez-vous. L'open space est accessible aux résidents 7 jours sur 7.</span></li>
        </ul>
      </div>
      <div class="carte">
        <h3>Venir en transports</h3>
        <ul><li>Tram B, arrêt Chartrons</li><li>Tram C, arrêt Camille Godard</li><li>Bus 4 et 15, arrêt Picard</li></ul>
        <p style="margin-top:.8rem"><a href="{u:chartrons-business-center}">Plan d'accès et parking</a></p>
      </div>
    </aside>
  </div>
</section>
""")

# ----- Pages légales
page(slug="mentions-legales", nav=None,
     title="Mentions légales | Chartrons Business Center",
     description="Mentions légales du site location-bureau-bordeaux.fr, édité par Shared Values, Bordeaux.",
     h1="Mentions légales", chapo="",
     corps="""
<section class="section"><div class="conteneur prose">
<h2>Éditeur du site</h2>
<p>Le site location-bureau-bordeaux.fr est édité par <strong>Shared Values</strong>, société à responsabilité limitée au capital de 52 384 €, dont le siège est situé {adresse}, {cp} {ville}, France.<br>RCS Bordeaux 751 479 585. SIREN : 751 479 585. Numéro de TVA intracommunautaire : FR75751479585. Code APE : 6420Z.<br>Téléphone : <a href="tel:{tel_intl}">{tel}</a>. E-mail : <a href="mailto:{email}">{email}</a>.</p>
<h2>Directeur de la publication</h2>
<p>Romain Jannekeyn-Vauquier, en qualité de gérant.</p>
<h2>Hébergement</h2>
<p>OVH SAS, 2 rue Kellermann, 59100 Roubaix, France.</p>
<h2>Conception et réalisation</h2>
<p>Shared Values, {adresse}, {cp} {ville}.</p>
<h2>Propriété intellectuelle</h2>
<p>L'ensemble des contenus du site (textes, visuels, logos, structure) est protégé par le droit d'auteur. Toute reproduction, même partielle, sans autorisation écrite de l'éditeur est interdite.</p>
<h2>Données personnelles et cookies</h2>
<p>Les données collectées via le formulaire de contact servent uniquement à traiter votre demande. Le détail de leur traitement, de vos droits et de l'usage des cookies figure dans la <a href="{u:politique-de-confidentialite}">politique de confidentialité</a>.</p>
<h2>Droit applicable</h2>
<p>Le présent site est soumis au droit français. En cas de litige, et à défaut d'accord amiable, les tribunaux de Bordeaux sont seuls compétents.</p>
</div></section>
""")
page(slug="politique-de-confidentialite", nav=None,
     title="Politique de confidentialité | Chartrons Business Center",
     description="Politique de confidentialité et gestion des cookies du site location-bureau-bordeaux.fr.",
     h1="Politique de confidentialité", chapo="",
     corps="""
<section class="section"><div class="conteneur prose">
<p class="meta">Dernière mise à jour : {date_fr}.</p>
<h2>Responsable du traitement</h2>
<p>Shared Values, {adresse}, {cp} {ville}. Contact : <a href="mailto:{email}">{email}</a>.</p>
<h2>Données collectées</h2>
<p>Lorsque vous utilisez le formulaire de contact, nous collectons votre nom, votre adresse e-mail, et, si vous les renseignez, le nom de votre entreprise, votre numéro de téléphone et le contenu de votre message. Ces données servent uniquement à répondre à votre demande de visite, de devis ou d'information. La base légale est votre consentement, recueilli par la case à cocher du formulaire.</p>
<h2>Durée de conservation</h2>
<p>Les demandes de contact sont conservées au maximum trois ans à compter du dernier échange, puis supprimées.</p>
<h2>Destinataires</h2>
<p>Vos données sont traitées par l'équipe du Chartrons Business Center. Elles ne sont ni vendues ni cédées à des tiers. L'hébergeur du site (OVH, France) y a accès techniquement dans le cadre de sa prestation.</p>
<h2>Vos droits</h2>
<p>Vous disposez d'un droit d'accès, de rectification, d'effacement, de limitation, d'opposition et de portabilité de vos données. Pour l'exercer, écrivez à <a href="mailto:{email}">{email}</a>. Vous pouvez aussi saisir la CNIL (cnil.fr) si vous estimez que vos droits ne sont pas respectés.</p>
<h2>Cookies</h2>
<p>Ce site ne dépose aucun cookie de suivi sans votre accord. Le plan Google Maps de la page d'accès n'est chargé qu'après un clic de votre part. Si un outil de mesure d'audience est activé, il vous est proposé via un bandeau de consentement et vous pouvez le refuser sans que la navigation en soit affectée.</p>
</div></section>
""")
page(slug="plan-du-site", nav=None,
     title="Plan du site | Chartrons Business Center",
     description="Toutes les pages du site location-bureau-bordeaux.fr : bureaux, coworking, salles de réunion, services, tarifs, lieu, témoignages, FAQ, guide et contact.",
     h1="Plan du site", chapo="",
     corps="""<section class="section"><div class="conteneur prose">{plan}</div></section>""")

# ---------------------------------------------------------------- FAQ et témoignages
FAQ = [
 ("tarifs toutes", "Combien coûte un bureau au Chartrons Business Center ?", "Un poste de travail équipé en open space coûte 350 € HT par mois pour le premier poste, puis 300 € HT par mois pour chaque poste supplémentaire. Le loyer comprend le mobilier, la fibre, l'impression, les salles de réunion jusqu'à 8 personnes et l'espace détente."),
 ("tarifs toutes", "Quel est l'engagement minimum ?", "Le contrat est mensuel. Vous pouvez louer un poste pour quelques mois ou pour plusieurs années, et ajouter ou retirer des postes au fil de l'évolution de votre équipe. Les conditions précises figurent sur le devis."),
 ("lieu toutes", "Où se trouve le Chartrons Business Center ?", "Au 9 rue André Darbon, 33300 Bordeaux, dans le quartier des Chartrons, près des Bassins à flot. Le tram B (arrêt Chartrons), le tram C (arrêt Camille Godard) et les bus 4 et 15 (arrêt Picard) desservent l'immeuble."),
 ("salles toutes", "Les salles de réunion sont-elles incluses ?", "Oui pour les résidents : les salles de 6 à 8 personnes sont en accès libre, sur réservation dans le planning partagé. La grande salle de 16 à 20 personnes et la location par des entreprises extérieures se font sur demande."),
 ("bureaux toutes", "Puis-je domicilier mon entreprise à cette adresse ?", "La domiciliation du siège social au 9 rue André Darbon peut être étudiée pour les résidents qui louent un poste. Parlez-en lors de la visite, nous vous indiquerons les conditions et les justificatifs nécessaires (voir notre guide pour domicilier son entreprise à Bordeaux)."),
 ("tarifs toutes", "Y a-t-il des frais de dossier ou un dépôt de garantie ?", "Il n'y a pas de frais de dossier. Les modalités de dépôt de garantie, s'il y en a, sont précisées sur le devis en fonction du nombre de postes."),
 ("coworking toutes", "À quelles heures l'open space est-il accessible ?", "Les résidents disposent d'un accès sécurisé et peuvent venir travailler en dehors des horaires de bureau, y compris le week-end, dans le respect du règlement intérieur. Les visites se font du lundi au vendredi sur rendez-vous."),
 ("coworking toutes", "Qui travaille dans l'open space ?", "Des indépendants, des fondateurs de start-up du numérique, des agences, des consultants en ressources humaines, des avocats et des gestionnaires de patrimoine. L'immeuble abrite aussi un incubateur éco-créatif de jeunes entreprises."),
 ("salles toutes", "Les salles sont-elles équipées pour la visioconférence ?", "Les salles disposent d'un écran de présentation, de l'audioconférence et de la fibre. Vous pouvez y brancher votre ordinateur pour une visioconférence avec votre propre outil."),
 ("salles toutes", "Peut-on louer une salle sans être résident ?", "Oui, sur demande. Indiquez-nous la date, la durée et le nombre de participants par téléphone ou via le formulaire de contact, et nous vous confirmons la disponibilité et le tarif dans la journée."),
 ("tarifs toutes", "Les prix sont-ils hors taxes ?", "Oui, tous les tarifs sont indiqués hors taxes, la TVA de 20 % s'ajoute sur la facture."),
 ("bureaux toutes", "Le parking est-il compris ?", "Le local vélos, scooters et motos est inclus. La place de parking voiture en garage couvert est une option à 130 € HT par mois."),
 ("accueil lieu toutes", "L'immeuble est-il accessible aux personnes à mobilité réduite ?", "Oui. L'immeuble dispose d'un ascenseur desservant l'open space au troisième étage et de circulations adaptées aux personnes à mobilité réduite."),
 ("accueil toutes", "Peut-on visiter avant de s'engager ?", "Oui, et nous le recommandons. Une visite dure environ 30 minutes, du lundi au vendredi sur rendez-vous. Appelez le " + TEL + " ou utilisez le formulaire de contact."),
]
FAQ += [
 ("accueil toutes", "Coworking, bureau pour une équipe ou salle de réunion : que louer aux Chartrons ?", "Un indépendant loue un poste de coworking à 350 € HT par mois. Une équipe de 2 à 10 personnes regroupe ses postes dans l'open space, à 300 € HT le poste supplémentaire. Une entreprise extérieure réserve une salle de réunion à la demi-journée ou à la journée."),
 ("accueil toutes", "Combien de temps faut-il pour s'installer ?", "Quelques jours : après la visite, nous envoyons un devis au nombre de postes, puis votre bureau, votre fauteuil, votre accès Wi-Fi et votre badge sont prêts à votre arrivée."),
 ("bureaux toutes", "Quelle est la taille d'un poste de travail ?", "Chaque poste comprend un bureau neuf de 160 × 80 cm avec cloison de courtoisie et un fauteuil ergonomique synchrone réglable, dans l'open space de 700 m²."),
 ("bureaux toutes", "Combien de postes une équipe peut-elle regrouper ?", "De 2 à 10 postes regroupés dans l'open space, à 300 € HT par mois le poste supplémentaire ; un poste de plus s'ajoute en quelques jours quand vous recrutez."),
 ("coworking toutes", "Puis-je louer un poste de coworking pour un seul mois ?", "Oui, le contrat est mensuel : un indépendant peut louer un poste pour un mois, une saison ou plusieurs années, sans engagement de surface."),
 ("coworking toutes", "Proposez-vous du flex office à la demande ?", "Oui. Le flex office à la demande permet de réserver un poste équipé en open space pour une journée, une demi-journée ou quelques jours par mois, sans engagement. Vous disposez des mêmes services que les résidents : fibre, Wi-Fi, impression, espace détente. Le tarif dépend du nombre de jours ; contactez-nous avec vos dates."),
 ("coworking toutes", "Le coworking comprend-il les salles de réunion ?", "Oui, les salles de 6 à 8 personnes sont incluses pour les coworkers, sur réservation dans le planning partagé, pour recevoir un client ou passer un appel au calme."),
]
TEMOIGNAGES = [
 ("Julien Pellegrain", "Les Horaires", "Ces bureaux modernes, spacieux et lumineux sont idéaux pour les travailleurs indépendants."),
 ("Sophie Pallas", "Oenopia", "Un peu réticente par principe aux espaces ouverts et à la cohabitation, j'ai pourtant essayé le coworking au Chartrons Business Center. Et j'y suis restée."),
 ("Christian Perron", "CRC, entrepreneur", "Plus qu'un bureau, c'est un vrai cadre de vie digne d'une start-up qui s'offre à vous."),
 ("Mariette Brenier", "Studio Malette Graphique", "J'apprécie notamment la salle de repos qui permet d'échanger autour d'un thé ou d'un café."),
 ("Benoît Droulin", "Azendoo", "Le Chartrons Business Center a su nous offrir des conditions idéales pour accueillir notre start-up."),
 ("Robert Gough", "Mevia, Alumn Force", "Le midi on voit du monde, ça permet de s'aérer la tête et de rencontrer des gens."),
 ("Sophie Brillaud", "Fimco", "C'est toute l'énergie que ça diffuse, l'échange avec des personnes qui ont des métiers complètement différents."),
]
LOGOS = ["Azendoo", "Alumn Force", "Oenopia", "Fimco", "Studio Malette Graphique", "Les Horaires", "Bergamotte", "Solaris Gestion", "Trafficlabs", "Cedrus Partners", "LeMagIT", "Clément Sélection", "Mouton Volé"]

# ---------------------------------------------------------------- rendu
def faq_html(cle):
    items = [f for f in FAQ if cle in f[0].split()]
    if cle in ("accueil", "bureaux", "coworking"): items = items[:4]
    out = []
    for i, (_, q, r) in enumerate(items):
        out.append(f'<div class="faq-item"><h3><button type="button" aria-expanded="true" aria-controls="faq-{cle}-{i}">{q}</button></h3><div class="reponse" id="faq-{cle}-{i}"><p>{r}</p></div></div>')
    return "".join(out), items

def temoignages_html(n):
    out = []
    for nom, soc, txt in TEMOIGNAGES[:n]:
        ini = "".join(p[0] for p in nom.split()[:2])
        out.append(f'<figure class="temoignage"><blockquote><p>{txt}</p></blockquote><figcaption><span class="avatar" aria-hidden="true">{ini}</span><span><strong>{nom}</strong><span>{soc}</span></span></figcaption></figure>')
    return "".join(out)

def date_fr(iso):
    y, m, d = iso.split("-")
    mois = ["janvier","février","mars","avril","mai","juin","juillet","août","septembre","octobre","novembre","décembre"][int(m)-1]
    return f"{int(d)} {mois} {y}"

def rendre(mode):
    """mode = 'preview' (liens relatifs slug.html) ou 'prod' (liens /slug/)."""
    dist = os.path.join(SRC, "dist", mode)
    if os.path.exists(dist): shutil.rmtree(dist)
    os.makedirs(os.path.join(dist, "assets"))
    # Les sources CSS sont découpées par rôle dans src/css/ et concaténées en une seule feuille (une seule requête)
    shutil.copytree(os.path.join(SRC, "src", "img"), os.path.join(dist, "assets", "img"))
    css_dir = os.path.join(SRC, "src", "css")
    css = "\n".join(open(os.path.join(css_dir, f), encoding="utf-8").read() for f in sorted(os.listdir(css_dir)) if f.endswith(".css"))
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S); css = re.sub(r"\n\s*\n", "\n", css)
    if mode == "preview": css = css.replace('url("/assets/fonts/', 'url("fonts/')
    import hashlib
    CSS_NOM = "style." + hashlib.md5(css.encode()).hexdigest()[:8] + ".css"
    open(os.path.join(dist, "assets", CSS_NOM), "w", encoding="utf-8").write(css)
    shutil.copytree(os.path.join(SRC, "src", "fonts"), os.path.join(dist, "assets", "fonts"))

    def u(slug):
        if mode == "preview": return (slug + ".html") if slug else "index.html"
        return "/" + (slug + "/" if slug else "")
    def abs_url(p): return DOMAINE + "/" + p
    A = "assets/" if mode == "preview" else "/assets/"
    global PHOTO_PREFIX_ACTIF; PHOTO_PREFIX_ACTIF = A + "img/photos/"
    def canon(slug): return DOMAINE + "/" + (slug + "/" if slug else "")

    toutes = PAGES + [dict(a, nav=None, est_article=True) for a in ARTICLES]
    nav_pages = [p for p in PAGES if p.get("nav")]

    PRINCIPAL = [("location-bureaux-bordeaux", "Bureaux"), ("coworking-bordeaux-chartrons", "Coworking"), ("salles-de-reunion-bordeaux", "Salles de réunion"), ("tarifs", "Tarifs"), ("chartrons-business-center", "Le lieu")]
    SECONDAIRE = [("services", "Services inclus"), ("temoignages", "Témoignages"), ("faq", "FAQ"), ("guide", "Guide"), ("contact", "Contact")]
    def nav_html(cur):
        li = []
        for sl, lab in PRINCIPAL:
            cur_attr = ' aria-current="page"' if sl == cur else ""
            li.append(f'<li><a href="{u(sl)}"{cur_attr}>{lab}</a></li>')
        sec = "".join(f'<li><a href="{u(sl)}"{" aria-current=\"page\"" if sl == cur else ""}>{lab}</a></li>' for sl, lab in SECONDAIRE)
        return "".join(li) + f'<li class="nav-secondaire"><ul>{sec}</ul></li><li class="nav-mobile-cta"><a class="tel-cta" href="tel:{TEL_INTL}">{ICONES["telico"]}<span>{TEL}</span></a><a class="btn" href="{u("contact")}">Réserver une visite</a></li>'

    def fil(p):
        items = [("Accueil", u(""))]
        if p.get("est_article"): items.append(("Guide", u("guide")))
        items.append((p["h1"] if len(p["h1"]) < 60 else p.get("nav") or p["h1"], None))
        lis = []
        for i, (lab, href) in enumerate(items):
            lis.append(f'<li><a href="{href}">{lab}</a></li>' if href else f'<li><span aria-current="page">{lab}</span></li>')
        ld = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
            {"@type": "ListItem", "position": i+1, "name": lab, "item": canon(p["slug"]) if href is None else (canon("") if lab == "Accueil" else canon("guide"))} for i, (lab, href) in enumerate(items)]}
        return f'<nav class="fil" aria-label="Fil d\'Ariane"><ol>{"".join(lis)}</ol></nav>', ld

    plan_html = "<ul>" + "".join(f'<li><a href="{u(p["slug"])}">{p["h1"]}</a></li>' for p in PAGES) + "</ul><h2>Guide</h2><ul>" + "".join(f'<li><a href="{u(a["slug"])}">{a["h1"]}</a></li>' for a in ARTICLES) + "</ul>"
    articles_html = "".join(
        f'<article class="carte article-carte"><div class="illustration">{visuel(a["h1"], i, "16/9")}</div><time datetime="{a["date"]}">{date_fr(a["date"])} · {a["temps"]} de lecture</time><h3><a href="{u(a["slug"])}">{a["h1"]}</a></h3><p>{a["description"]}</p><a class="lien" href="{u(a["slug"])}">Lire l\'article</a></article>'
        for i, a in enumerate(ARTICLES))
    cta_html = f'<section class="section"><div class="conteneur"><div class="cta"><div><h2>Envie de voir l\'open space ?</h2><p>Visite de 30 minutes, du lundi au vendredi sur rendez-vous. Devis au nombre de postes envoyé dans la journée.</p></div><div class="btn-groupe"><a class="btn btn-blanc" href="{u("contact")}">Réserver une visite</a><a class="btn btn-blanc" href="tel:{TEL_INTL}">{TEL}</a></div></div></div></section>'

    sitemap = []
    for p in toutes:
        slug = p["slug"]; corps = p["corps"]; PHOTO_COMPTEUR[0] = 0
        faq_items = []
        # substitutions
        def sub_u(m): return u(m.group(1))
        corps = re.sub(r"\{u:([a-z0-9-]+)\}", sub_u, corps)
        def sub_v(m): return visuel(m.group(1), int(m.group(2)))
        corps = re.sub(r"\{v:([^:}]+):(\d)\}", sub_v, corps)
        def sub_faq(m):
            h, items = faq_html(m.group(1)); faq_items.extend(items); return h
        corps = re.sub(r"\{faq:([a-z]+)\}", sub_faq, corps)
        corps = re.sub(r"\{photo:([a-z0-9-]+):([^}]+)\}", lambda m: photo(m.group(1), m.group(2), sizes="(max-width: 620px) 100vw, (max-width: 960px) 50vw, 370px"), corps)
        corps = re.sub(r"\{temoignages:(\d)\}", lambda m: temoignages_html(int(m.group(1))), corps)
        corps = corps.replace("{logos}", "".join(f"<li>{l}</li>" for l in LOGOS))
        corps = corps.replace("{articles}", articles_html).replace("{plan}", plan_html).replace("{cta}", cta_html)
        for k, v in ICONES.items(): corps = corps.replace("{" + k + "}", v).replace("{" + k + "_ico}", v)
        corps = corps.replace("{tel}", TEL).replace("{tel_intl}", TEL_INTL).replace("{email}", EMAIL).replace("{nom}", NOM).replace("{adresse}", ADRESSE).replace("{cp}", CP).replace("{ville}", VILLE).replace("{date_fr}", date_fr(DATE_MAJ))

        fil_html, fil_ld = fil(p)
        og_image = abs_url("assets/img/og.jpg")
        for k_titre, (k_cle, k_alt) in PHOTOS.items():
            if k_titre == p["h1"] or ("{v:" + k_titre) in p["corps"]:
                og_image = abs_url(f"assets/img/photos/{k_cle}-1600.webp"); break
        ld = [jsonld_org(abs_url), {"@context": "https://schema.org", "@type": "WebSite", "@id": DOMAINE + "/#site", "url": DOMAINE + "/", "name": MARQUE, "inLanguage": "fr-FR", "publisher": {"@id": DOMAINE + "/#organisation"}}] if slug == "" else [fil_ld]
        if faq_items:
            ld.append({"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for _, q, r in faq_items]})
        if p.get("est_article"):
            ld.append({"@context": "https://schema.org", "@type": "Article", "headline": p["h1"], "description": p["description"], "datePublished": p["date"], "dateModified": p["date"], "inLanguage": "fr-FR", "mainEntityOfPage": canon(slug), "author": {"@type": "Organization", "name": NOM, "@id": DOMAINE + "/#organisation"}, "publisher": {"@id": DOMAINE + "/#organisation"}})
        if slug in ("location-bureaux-bordeaux", "coworking-bordeaux-chartrons", "salles-de-reunion-bordeaux"):
            nom_service = {"location-bureaux-bordeaux": "Location de bureaux équipés", "coworking-bordeaux-chartrons": "Coworking", "salles-de-reunion-bordeaux": "Location de salles de réunion"}[slug]
            ld.append({"@context": "https://schema.org", "@type": "Service", "name": nom_service, "serviceType": nom_service, "provider": {"@id": DOMAINE + "/#organisation"}, "areaServed": {"@type": "City", "name": "Bordeaux"}, "url": canon(slug), "description": p["description"], "offers": jsonld_org(abs_url)["makesOffer"][:2] if slug != "salles-de-reunion-bordeaux" else {"@type": "Offer", "name": "Salle de réunion de 6 à 20 personnes", "priceCurrency": "EUR", "availability": "https://schema.org/InStock", "description": "Incluse pour les résidents jusqu'à 8 personnes ; sur devis pour les entreprises extérieures"}})
        if slug == "temoignages":
            ld.append({"@context": "https://schema.org", "@type": "Organization", "@id": DOMAINE + "/#organisation", "review": [{"@type": "Review", "author": {"@type": "Person", "name": n}, "reviewBody": t, "itemReviewed": {"@id": DOMAINE + "/#organisation"}} for n, soc, t in TEMOIGNAGES]})
        ld_html = "".join(f'<script type="application/ld+json">{json.dumps(x, ensure_ascii=False)}</script>' for x in ld)

        if slug == "":
            entete_page = f"""
<section class="heros"><div class="conteneur">
  <div><span class="etiquette">Bordeaux · Chartrons</span><h1>Location de bureaux et <em>coworking</em> à Bordeaux, quartier des Chartrons</h1><p class="intro">{p["chapo"]}</p>
  <div class="btn-groupe"><a class="btn" href="{u("contact")}">Réserver une visite</a><a class="btn btn-secondaire" href="{u("tarifs")}">Voir les tarifs</a></div>
  <ul class="points-cles"><li><strong>700 m²</strong><span>d'open space</span></li><li><strong>350 € HT</strong><span>par mois, 1er poste</span></li><li><strong>9 salles</strong><span>de réunion</span></li><li><strong>Tram B et C</strong><span>à 5 minutes</span></li></ul></div>
  <div class="heros-visuel"><div class="cadre"></div><figure>{visuel("L'open space lumineux du Chartrons Business Center", 0)}<figcaption>Open space de 700 m² au troisième étage, 9 rue André Darbon, Bordeaux.</figcaption></figure></div>
</div></section>"""
        elif p.get("est_article"):
            entete_page = f"""<header class="bandeau"><div class="conteneur">{fil_html}<h1>{p["h1"]}</h1><p class="intro">{p["chapo"]}</p><p class="meta" style="color:#c6c9dd">Publié le <time datetime="{p["date"]}">{date_fr(p["date"])}</time> · {p["temps"]} de lecture · par l'équipe du {NOM}</p></div></header>"""
            autres = "".join('<li><a href="%s">%s</a></li>' % (u(a["slug"]), a["h1"]) for a in ARTICLES if a["slug"] != slug)
            corps = f'<section class="section"><div class="conteneur mise-en-page"><article class="prose"><div class="visuel" style="margin-bottom:2rem">{visuel(p["h1"], 0)}</div>{corps}</article><aside class="aside" aria-label="Pour aller plus loin"><div class="carte"><h3>Nos espaces</h3><ul><li><a href="{u("location-bureaux-bordeaux")}">Bureaux équipés</a></li><li><a href="{u("coworking-bordeaux-chartrons")}">Coworking</a></li><li><a href="{u("salles-de-reunion-bordeaux")}">Salles de réunion</a></li><li><a href="{u("tarifs")}">Tarifs</a></li></ul></div><div class="carte"><h3>Autres articles</h3><ul>{autres}</ul></div></aside></div></section>{cta_html}'
        else:
            chapo = f'<p class="intro">{p["chapo"]}</p>' if p["chapo"] else ""
            entete_page = f"""<header class="bandeau"><div class="conteneur">{fil_html}<h1>{p["h1"]}</h1>{chapo}</div></header>"""

        doc = f"""<!DOCTYPE html>
<html lang="fr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html.escape(p["title"])}</title>
<meta name="description" content="{html.escape(p["description"])}">
<link rel="canonical" href="{canon(slug)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta property="og:type" content="{'article' if p.get('est_article') else 'website'}">
<meta property="og:locale" content="fr_FR">
<meta property="og:site_name" content="{NOM}">
<meta property="og:title" content="{html.escape(p["title"])}">
<meta property="og:description" content="{html.escape(p["description"])}">
<meta property="og:url" content="{canon(slug)}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#111111">
<link rel="icon" href="{A}favicon.svg" type="image/svg+xml">
<link rel="icon" href="{'' if mode=='preview' else '/'}favicon.ico" sizes="32x32">
<link rel="preload" href="{A}fonts/montserrat-latin-900-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{A}{CSS_NOM}">
{ld_html}
</head>
<body>
<a class="skip" href="#contenu">Aller au contenu</a>
<header class="entete"><div class="conteneur">
  <a class="logo" href="{u("")}"><img class="logo-img" src="{A}img/logo.webp" width="200" height="64" alt="Coworking Bordeaux Chartrons, location de bureaux"></a>
  <nav class="nav" id="menu-principal" aria-label="Navigation principale"><ul>{nav_html(slug)}</ul></nav>
  <div class="entete-actions">
    <a class="tel-cta" href="tel:{TEL_INTL}" aria-label="Appeler le {TEL}">{ICONES["telico"]}<span><small>Appelez-nous</small>{TEL}</span></a>
    <a class="btn btn-cta" href="{u("contact")}">Réserver une visite</a>
    <a class="tel-mobile" href="tel:{TEL_INTL}" aria-label="Appeler le {TEL}">{ICONES["telico"]}</a>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu-principal"><span class="burger" aria-hidden="true"></span>Menu</button>
  </div>
</div></header>
<main id="contenu">
{entete_page}
{corps}
</main>
<footer class="pied"><div class="conteneur">
  <div class="grille">
    <div><a class="logo" href="{u("")}"><img class="logo-img" src="{A}img/logo-blanc.webp" width="200" height="64" alt="Coworking Bordeaux Chartrons, retour à l'accueil"></a><p>Location de bureaux équipés, coworking et salles de réunion dans un open space de 700 m² au cœur des Chartrons, à Bordeaux. Un espace Shared Values.</p></div>
    <div><p class="titre-pied">Nos espaces</p><ul><li><a href="{u("location-bureaux-bordeaux")}">Bureaux équipés</a></li><li><a href="{u("coworking-bordeaux-chartrons")}">Coworking</a></li><li><a href="{u("salles-de-reunion-bordeaux")}">Salles de réunion</a></li><li><a href="{u("services")}">Services inclus</a></li><li><a href="{u("tarifs")}">Tarifs</a></li></ul></div>
    <div><p class="titre-pied">Informations</p><ul><li><a href="{u("chartrons-business-center")}">Le lieu et l'accès</a></li><li><a href="{u("temoignages")}">Témoignages</a></li><li><a href="{u("faq")}">Questions fréquentes</a></li><li><a href="{u("guide")}">Guide</a></li><li><a href="{u("contact")}">Contact et visite</a></li></ul></div>
    <div><p class="titre-pied">Contact</p><address>{NOM}<br>{ADRESSE}<br>{CP} {VILLE}<br><a href="tel:{TEL_INTL}">{TEL}</a><br><a href="mailto:{EMAIL}">{EMAIL}</a></address></div>
  </div>
  <div class="pied-bas"><p>© {DATE_MAJ[:4]} Shared Values. Tous droits réservés.</p><ul><li><a href="{u("mentions-legales")}">Mentions légales</a></li><li><a href="{u("politique-de-confidentialite")}">Confidentialité</a></li><li><a href="{u("plan-du-site")}">Plan du site</a></li></ul></div>
</div></footer>
<script>
(function(){{
  var b=document.querySelector('.menu-btn'),n=document.getElementById('menu-principal');
  if(b){{b.addEventListener('click',function(){{var o=n.classList.toggle('ouvert');b.setAttribute('aria-expanded',o?'true':'false');}});}}
  document.querySelectorAll('.faq-item button').forEach(function(bt,i){{
    var r=document.getElementById(bt.getAttribute('aria-controls'));
    if(i>0){{r.hidden=true;bt.setAttribute('aria-expanded','false');}}
    bt.addEventListener('click',function(){{var ouvert=bt.getAttribute('aria-expanded')==='true';bt.setAttribute('aria-expanded',ouvert?'false':'true');r.hidden=ouvert;}});
  }});
  var cp=document.getElementById('charger-plan');
  if(cp){{cp.addEventListener('click',function(){{var f=document.createElement('iframe');f.src='https://www.google.com/maps?q=9+rue+Andr%C3%A9+Darbon+33300+Bordeaux&output=embed';f.title='Plan Google Maps du 9 rue André Darbon à Bordeaux';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';cp.parentNode.replaceChild(f,cp);}});}}
}})();
</script>
</body>
</html>
"""
        if mode == "preview":
            chemin = os.path.join(dist, (slug or "index") + ".html")
        else:
            d = os.path.join(dist, slug) if slug else dist
            os.makedirs(d, exist_ok=True); chemin = os.path.join(d, "index.html")
        open(chemin, "w", encoding="utf-8").write(doc)
        prio = "1.0" if slug == "" else ("0.9" if slug in ("location-bureaux-bordeaux", "coworking-bordeaux-chartrons", "salles-de-reunion-bordeaux", "tarifs") else ("0.3" if slug in ("mentions-legales", "politique-de-confidentialite", "plan-du-site") else "0.7"))
        sitemap.append((canon(slug), prio, p.get("date", DATE_MAJ)))

    # assets
    from PIL import Image
    Image.open(os.path.join(SRC, "src", "img", "logo.png")).convert("RGBA").crop((0, 0, 120, 120)).resize((32, 32)).save(os.path.join(dist, "favicon.ico"), sizes=[(32, 32)])
    for f in ("logo.png", "logo-blanc.png"): os.remove(os.path.join(dist, "assets", "img", f))
    placeholders = [f for f in __import__("glob").glob(os.path.join(dist, "**", "*.html"), recursive=True) if "[à compléter]" in open(f, encoding="utf-8").read()]
    if placeholders: print("ATTENTION : champs « [à compléter] » dans", [os.path.relpath(f, dist) for f in placeholders])
    open(os.path.join(dist, "assets", "favicon.svg"), "w").write(LOGO_SVG.replace("aria-hidden='true'", "xmlns='http://www.w3.org/2000/svg'"))
    open(os.path.join(dist, "assets", "logo.svg"), "w").write(LOGO_SVG.replace("aria-hidden='true'", "xmlns='http://www.w3.org/2000/svg'"))
    og = f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 1200 630' width='1200' height='630'><rect width='1200' height='630' fill='#010514'/><rect x='0' y='0' width='1200' height='14' fill='#111111'/><text x='80' y='250' font-family='Montserrat,system-ui,sans-serif' font-size='64' font-weight='800' fill='#fff'>Location de bureaux et coworking</text><text x='80' y='330' font-family='Montserrat,system-ui,sans-serif' font-size='64' font-weight='800' fill='#8f94ff'>Bordeaux Chartrons</text><text x='80' y='420' font-family='system-ui,sans-serif' font-size='30' fill='#c6c9dd'>Open space de 700 m² · dès 350 € HT par mois · {ADRESSE}</text></svg>"
    open(os.path.join(dist, "assets", "og.svg"), "w").write(og)

    if mode == "prod":
        open(os.path.join(dist, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"  <url><loc>{l}</loc><lastmod>{d}</lastmod><priority>{pr}</priority></url>\n" for l, pr, d in sitemap) + "</urlset>\n")
        open(os.path.join(dist, "robots.txt"), "w").write(f"""# Robots classiques
User-agent: *
Allow: /

# Robots des moteurs de réponse IA : accès autorisé volontairement (visibilité GEO)
User-agent: GPTBot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: ClaudeBot
User-agent: Claude-User
User-agent: Claude-SearchBot
User-agent: anthropic-ai
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Google-Extended
User-agent: Applebot-Extended
User-agent: Bingbot
Allow: /

Sitemap: {DOMAINE}/sitemap.xml
""")
        open(os.path.join(dist, "llms.txt"), "w").write(f"""# {NOM}

> Location de bureaux équipés, coworking, flex office à la demande et salles de réunion dans un open space de 700 m² au 9 rue André Darbon, quartier des Chartrons, à Bordeaux (France). Premier poste 350 € HT par mois, postes supplémentaires 300 € HT par mois, parking couvert 130 € HT par mois. Téléphone {TEL}.

## Pages principales
""" + "".join(f"- [{p['h1']}]({canon(p['slug'])}) : {p['description']}\n" for p in PAGES if p["slug"] not in ("mentions-legales", "politique-de-confidentialite", "plan-du-site")) + "\n## Guide\n" + "".join(f"- [{a['h1']}]({canon(a['slug'])}) : {a['description']}\n" for a in ARTICLES))
        open(os.path.join(dist, ".htaccess"), "w").write("""# URLs propres, cache et compression (Apache, hébergement OVH)
Options -Indexes
AddDefaultCharset UTF-8
DirectoryIndex index.html

RewriteEngine On
# Forcer HTTPS et le www
RewriteCond %{HTTPS} off [OR]
RewriteCond %{HTTP_HOST} !^www\\. [NC]
RewriteRule ^ https://www.location-bureau-bordeaux.fr%{REQUEST_URI} [L,R=301]
# Rediriger les anciennes URL du site WordPress
RewriteRule ^coworking/?$ /coworking-bordeaux-chartrons/ [R=301,L]
RewriteRule ^services-proposes/?$ /services/ [R=301,L]
RewriteRule ^temoignages/?$ /temoignages/ [R=301,L]
RewriteRule ^le-cadre/?$ /chartrons-business-center/ [R=301,L]
RewriteRule ^merci/?$ /contact/ [R=301,L]
RewriteRule ^category/la-presse/?$ /temoignages/ [R=301,L]
RewriteRule ^article-dans-elle-sur-notre-coworking/?$ /temoignages/ [R=301,L]
RewriteRule ^wp-content/.*$ / [R=301,L]
# Ajouter la barre finale aux dossiers
RewriteCond %{REQUEST_FILENAME} -d
RewriteRule ^(.*[^/])$ /$1/ [R=301,L]

ErrorDocument 404 /404.html

<IfModule mod_deflate.c>
  AddOutputFilterByType DEFLATE text/html text/css text/plain text/xml application/xml application/javascript application/json application/ld+json image/svg+xml
</IfModule>
<IfModule mod_expires.c>
  ExpiresActive On
  ExpiresByType text/css "access plus 1 year"
  ExpiresByType image/svg+xml "access plus 1 year"
  ExpiresByType image/webp "access plus 1 year"
  ExpiresByType image/avif "access plus 1 year"
  ExpiresByType font/woff2 "access plus 1 year"
  ExpiresByType image/jpeg "access plus 1 year"
  ExpiresByType image/png "access plus 1 year"
  ExpiresByType image/x-icon "access plus 1 year"
  ExpiresByType text/html "access plus 1 hour"
</IfModule>
<IfModule mod_headers.c>
  Header always set X-Content-Type-Options "nosniff"
  Header always set X-Frame-Options "SAMEORIGIN"
  Header always set Referrer-Policy "strict-origin-when-cross-origin"
  Header always set Permissions-Policy "camera=(), microphone=(), geolocation=()"
  Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains"
</IfModule>
""")
        p404 = open(os.path.join(dist, "faq", "index.html"), encoding="utf-8").read()
        p404 = re.sub(r"<main id=\"contenu\">.*?</main>", f'<main id="contenu"><header class="bandeau"><div class="conteneur"><h1>Page introuvable</h1><p class="intro">La page demandée n\'existe pas ou a été déplacée. Les pages les plus utiles sont listées ci-dessous.</p></div></header><section class="section"><div class="conteneur prose">{plan_html}</div></section></main>', p404, flags=re.S)
        p404 = re.sub(r"<title>.*?</title>", "<title>Page introuvable | " + NOM + "</title>", p404).replace('<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">', '<meta name="robots" content="noindex">')
        p404 = re.sub(r'<link rel="canonical"[^>]*>\n', "", p404)
        p404 = re.sub(r'(<meta name="description" content=")[^"]*', r"\1Cette page n'existe pas ou a été déplacée. Retrouvez les bureaux, le coworking, les salles de réunion et les tarifs du " + NOM + ".", p404)
        p404 = re.sub(r'(<meta property="og:title" content=")[^"]*', r"\1Page introuvable", p404)
        p404 = re.sub(r'(<meta property="og:description" content=")[^"]*', r"\1Page introuvable sur le site du " + NOM + ".", p404)
        p404 = re.sub(r'(<meta property="og:url" content=")[^"]*', r"\1" + DOMAINE + "/404.html", p404)
        p404 = p404.replace(' aria-current="page"', "")
        p404 = re.sub(r'<script type="application/ld\+json">.*?</script>', "", p404, flags=re.S)
        open(os.path.join(dist, "404.html"), "w", encoding="utf-8").write(p404)
    print(mode, len(toutes), "pages")

if __name__ == "__main__":
    rendre("preview"); rendre("prod")
