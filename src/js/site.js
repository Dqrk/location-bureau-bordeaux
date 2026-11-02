(function(){
  var d=document;
  window.addEventListener('load',function(){setTimeout(function(){d.body.classList.remove('is-preload');},100);});

  /* Pas d'animation au défilement : le contenu est visible tout de suite (brief du 28/10, audit du 02/11).
     Seuls restent les filets du titre qui se tracent et une entrée courte du haut de page (CSS). */

  /* Sliders de photos : boutons, points, flèches du clavier ; le défilement reste natif (glisser au doigt).
     Les boutons ne sont jamais désactivés (aria-disabled) : le focus ne se perd pas en bout de série. */
  d.querySelectorAll('.slider').forEach(function(sl){
    var piste=sl.querySelector('.slider-piste'),slides=piste.children,prec=sl.querySelector('.slider-prec'),suiv=sl.querySelector('.slider-suiv'),points=sl.querySelectorAll('.slider-points button'),etat=sl.querySelector('.slider-etat'),n=slides.length,courant=0,attente=0;
    var aller=function(i){i=Math.max(0,Math.min(n-1,i));piste.scrollTo({left:i*piste.clientWidth,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});};
    var maj=function(){
      var c=Math.round(piste.scrollLeft/piste.clientWidth);
      prec.setAttribute('aria-disabled',c<=0?'true':'false');suiv.setAttribute('aria-disabled',c>=n-1?'true':'false');
      points.forEach(function(p,i){if(i===c)p.setAttribute('aria-current','true');else p.removeAttribute('aria-current');});
      if(etat&&c!==courant)etat.textContent='Photo '+(c+1)+' sur '+n;
      courant=c;
    };
    prec.addEventListener('click',function(){aller(courant-1);});
    suiv.addEventListener('click',function(){aller(courant+1);});
    points.forEach(function(p,i){p.addEventListener('click',function(){aller(i);});});
    piste.addEventListener('scroll',function(){cancelAnimationFrame(attente);attente=requestAnimationFrame(maj);},{passive:true});
    piste.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();aller(courant+1);}else if(e.key==='ArrowLeft'){e.preventDefault();aller(courant-1);}});
    window.addEventListener('resize',function(){aller(courant);});
    maj();
  });

  /* Menu mobile : focus sur le premier lien, Échap pour fermer, fermeture en sortie de menu ou en passant en grand écran */
  var b=d.querySelector('.menu-btn'),n=d.getElementById('menu-principal');
  if(b&&n){
    var fermer=function(rendreFocus){n.classList.remove('ouvert');b.setAttribute('aria-expanded','false');if(rendreFocus)b.focus();};
    b.addEventListener('click',function(){var o=n.classList.toggle('ouvert');b.setAttribute('aria-expanded',o?'true':'false');if(o){var l=n.querySelector('a');if(l)l.focus();}});
    d.addEventListener('keydown',function(e){if(e.key==='Escape'&&n.classList.contains('ouvert'))fermer(true);});
    n.addEventListener('focusout',function(e){var c=e.relatedTarget;if(n.classList.contains('ouvert')&&c&&c!==b&&!n.contains(c))fermer(false);});
    var mq=matchMedia('(min-width: 1101px)');if(mq.addEventListener)mq.addEventListener('change',function(m){if(m.matches)fermer(false);});
  }

  /* FAQ : première réponse ouverte, les autres repliées (tout reste lisible sans JavaScript) */
  d.querySelectorAll('.faq-item button').forEach(function(bt,i){
    var r=d.getElementById(bt.getAttribute('aria-controls'));
    if(i>0){r.hidden=true;bt.setAttribute('aria-expanded','false');}
    bt.addEventListener('click',function(){var ouvert=bt.getAttribute('aria-expanded')==='true';bt.setAttribute('aria-expanded',ouvert?'false':'true');r.hidden=ouvert;});
  });

  /* Plan Google Maps : chargé uniquement au clic (rien n'est envoyé à Google sans action du visiteur).
     Le lien d'itinéraire sous le plan reste disponible si la carte ne s'affiche pas. */
  var cp=d.getElementById('charger-plan');
  if(cp){
    cp.addEventListener('click',function(){
      var zone=cp.closest('.carte-plan'),f=d.createElement('iframe');
      f.title='Plan Google Maps du 9 rue André Darbon à Bordeaux';f.width='800';f.height='600';f.referrerPolicy='strict-origin-when-cross-origin';f.allowFullscreen=true;
      f.src='https://www.google.com/maps?q=9+rue+Andr%C3%A9+Darbon+33300+Bordeaux&output=embed';
      zone.innerHTML='';zone.appendChild(f);f.focus();
    });
  }

  /* Formulaire */
  var fo=d.querySelector('form.formulaire');
  if(fo){
    fo.setAttribute('novalidate','');
    var sel=fo.querySelector('#besoin'),lblPostes=d.getElementById('label-postes'),postes=fo.querySelector('#postes'),msg=fo.querySelector('#message'),etat=fo.querySelector('.envoi-etat'),bouton=fo.querySelector('[type=submit]');

    /* Besoin présélectionné selon le bouton cliqué (?besoin=visite, salle, equipe, flex, coworking), libellés adaptés */
    var aides={
      salle:['Nombre de participants','Date souhaitée, demi-journée ou journée, besoins (écran, visio)'],
      flex:['Nombre de postes','Dates souhaitées ou nombre de jours par mois'],
      visite:['Nombre de postes','Deux créneaux qui vous arrangent, du lundi au vendredi'],
      equipe:['Nombre de postes','Date d’arrivée souhaitée, options utiles (parking, ligne fixe), questions']
    };
    var defaut=[lblPostes?lblPostes.textContent:'',msg?msg.placeholder:''];
    var adapter=function(){
      var o=sel.options[sel.selectedIndex],a=aides[o&&o.getAttribute('data-cle')]||defaut;
      if(lblPostes)lblPostes.textContent=a[0];if(msg)msg.placeholder=a[1];
    };
    var cle=(location.search.match(/[?&]besoin=([a-z]+)/)||[])[1];
    if(cle){[].forEach.call(sel.options,function(o){if(o.getAttribute('data-cle')===cle)sel.value=o.value||o.text;});}
    sel.addEventListener('change',adapter);adapter();

    /* Messages d'erreur rédigés, reliés au champ et annoncés */
    var msgs={nom:'Indiquez votre nom et votre prénom.',email:'Indiquez une adresse e-mail valide, par exemple nom@entreprise.fr.',telephone:'Indiquez un numéro de téléphone valide.',besoin:'Choisissez votre besoin dans la liste.',postes:'Indiquez un nombre entre 1 et 30.',consentement:'Cochez cette case pour envoyer votre demande.'};
    var signaler=function(ch,actif){
      var id='err-'+ch.name,p=d.getElementById(id),liens=(ch.getAttribute('aria-describedby')||'').split(' ').filter(function(x){return x&&x!==id;});
      if(actif){
        if(!p){p=d.createElement('p');p.className='erreur';p.id=id;var apres=ch.type==='checkbox'?ch.closest('label'):ch;apres.parentNode.insertBefore(p,apres.nextSibling);}
        p.textContent=msgs[ch.name]||'Ce champ est à vérifier.';ch.setAttribute('aria-invalid','true');liens.push(id);
      }else{if(p)p.parentNode.removeChild(p);ch.removeAttribute('aria-invalid');}
      if(liens.length)ch.setAttribute('aria-describedby',liens.join(' '));else ch.removeAttribute('aria-describedby');
    };
    var envoiEnCours=false,libelle=bouton.textContent;
    var echec=function(){
      envoiEnCours=false;bouton.disabled=false;bouton.textContent=libelle;
      etat.className='envoi-etat envoi-erreur';
      etat.innerHTML='Votre demande n’a pas pu partir (connexion ou serveur indisponible). Vos informations sont conservées dans le formulaire : réessayez dans un instant, ou contactez-nous directement au <a href="tel:'+fo.getAttribute('data-tel-intl')+'">'+fo.getAttribute('data-tel')+'</a> ou par e-mail à <a href="mailto:'+fo.getAttribute('data-email')+'">'+fo.getAttribute('data-email')+'</a>.';
      etat.setAttribute('tabindex','-1');etat.focus();
    };
    fo.addEventListener('submit',function(e){
      var premier=null;
      [].forEach.call(fo.elements,function(ch){if(!ch.name||ch.name==='website'||!ch.willValidate)return;var ok=ch.checkValidity();signaler(ch,!ok);if(!ok&&!premier)premier=ch;});
      e.preventDefault();
      if(premier){premier.focus();return;}
      if(envoiEnCours)return;
      if(!window.fetch||!window.URLSearchParams){fo.submit();return;}
      /* Envoi en arrière-plan : si l'outil de formulaire ne répond pas, le visiteur reste sur la page avec un message et un recours */
      envoiEnCours=true;bouton.disabled=true;bouton.textContent='Envoi en cours…';etat.className='envoi-etat';etat.textContent='';
      var donnees=new URLSearchParams();[].forEach.call(fo.elements,function(ch){if(ch.name&&!(ch.type==='checkbox'&&!ch.checked))donnees.append(ch.name,ch.value);});
      var ctrl=window.AbortController?new AbortController():null,minuterie=setTimeout(function(){if(ctrl)ctrl.abort();},15000);
      fetch(fo.action,{method:'POST',mode:'no-cors',body:donnees,signal:ctrl?ctrl.signal:undefined})
        .then(function(){clearTimeout(minuterie);location.href=fo.getAttribute('data-merci');})
        .catch(function(){clearTimeout(minuterie);echec();});
    });
    fo.addEventListener('change',function(e){var ch=e.target;if(ch.getAttribute('aria-invalid')==='true'&&ch.checkValidity())signaler(ch,false);});
  }
})();
