(function(){
  var d=document;
  window.addEventListener('load',function(){setTimeout(function(){d.body.classList.remove('is-preload');},100);});

  /* Animations au défilement, uniquement sous la ligne de flottaison au chargement (rien ne clignote) :
     blocs en fondu montant décalé, titres mot par mot sortant d'un masque, photos qui se posent, chiffres qui défilent */
  if('IntersectionObserver' in window&&!matchMedia('(prefers-reduced-motion: reduce)').matches){
    var hauteur=window.innerHeight;
    var sousLaLigne=function(liste){var h=liste.map(function(el){return el.getBoundingClientRect().top;});return liste.filter(function(el,i){return h[i]>=hauteur;});};
    var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('vu');io.unobserve(e.target);if(e.target.compteur)e.target.compteur();}});},{rootMargin:'0px 0px -10% 0px'});
    var blocs=sousLaLigne([].slice.call(d.querySelectorAll('.en-tete-section>:not(h2),.grille>*,.deux-colonnes>div:not(.visuel),.galerie li,.etapes li,.faq-item,.faq-intro>p,.cta>*,.encadre,.pied-haut>*,.pied-nav>div,.table-scroll,.prose>p,.prose>ul,.formulaire>*,.chiffres>div')));
    var images=sousLaLigne([].slice.call(d.querySelectorAll('.deux-colonnes .visuel,.carte-visuel,.galerie li')));
    var titres=sousLaLigne([].slice.call(d.querySelectorAll('main h2,.pied-titre')));
    blocs.forEach(function(el){el.style.transitionDelay=Math.min([].indexOf.call(el.parentNode.children,el),4)*100+'ms';el.classList.add('reveal');io.observe(el);});
    images.forEach(function(el){el.classList.add('reveal-image');io.observe(el);});
    titres.forEach(function(t){
      if(t.children.length)return;
      var mots=t.textContent.trim().split(/ +/);
      t.textContent='';
      mots.forEach(function(m,i){var s=d.createElement('span'),c=d.createElement('span');s.className='mot';c.textContent=m;c.style.transitionDelay=Math.min(i,12)*45+'ms';s.appendChild(c);t.appendChild(s);if(i<mots.length-1)t.appendChild(d.createTextNode(' '));});
      t.classList.add('titre-anime');io.observe(t);
    });
    /* Chiffres clés : défilent de 0 à leur valeur ; le texte final reste dans le HTML */
    sousLaLigne([].slice.call(d.querySelectorAll('.chiffres strong'))).forEach(function(el){
      var m=el.textContent.match(/^(\d+)(.*)$/);if(!m)return;
      var fin=parseInt(m[1].replace(/\D/g,''),10),suite=m[2],bloc=el.closest('.chiffres>div')||el;
      bloc.compteur=function(){var t0=null,dur=1400;var pas=function(t){if(!t0)t0=t;var k=Math.min((t-t0)/dur,1),v=Math.round(fin*(1-Math.pow(1-k,3)));el.textContent=v+suite;if(k<1)requestAnimationFrame(pas);};requestAnimationFrame(pas);};
      el.textContent='0'+suite;
    });
  }

  /* Sliders de photos : boutons, points, flèches du clavier ; le défilement reste natif (glisser au doigt) */
  d.querySelectorAll('.slider').forEach(function(sl){
    var piste=sl.querySelector('.slider-piste'),slides=piste.children,prec=sl.querySelector('.slider-prec'),suiv=sl.querySelector('.slider-suiv'),points=sl.querySelectorAll('.slider-points button'),n=slides.length,courant=0,attente=0;
    var aller=function(i){i=Math.max(0,Math.min(n-1,i));piste.scrollTo({left:i*piste.clientWidth,behavior:matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});};
    var maj=function(){courant=Math.round(piste.scrollLeft/piste.clientWidth);prec.disabled=courant<=0;suiv.disabled=courant>=n-1;points.forEach(function(p,i){if(i===courant)p.setAttribute('aria-current','true');else p.removeAttribute('aria-current');});};
    prec.addEventListener('click',function(){aller(courant-1);});
    suiv.addEventListener('click',function(){aller(courant+1);});
    points.forEach(function(p,i){p.addEventListener('click',function(){aller(i);});});
    piste.addEventListener('scroll',function(){cancelAnimationFrame(attente);attente=requestAnimationFrame(maj);},{passive:true});
    piste.addEventListener('keydown',function(e){if(e.key==='ArrowRight'){e.preventDefault();aller(courant+1);}else if(e.key==='ArrowLeft'){e.preventDefault();aller(courant-1);}});
    window.addEventListener('resize',function(){aller(courant);});
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

  /* Plan Google Maps : chargé automatiquement juste avant d'arriver à l'écran ; le bouton reste en secours */
  var cp=d.getElementById('charger-plan');
  if(cp){
    var texte=cp.textContent,lance=false;
    var charger=function(){
      if(lance)return;lance=true;
      var charge=false,f=d.createElement('iframe');
      cp.disabled=true;cp.textContent='Chargement du plan\u2026';
      f.title='Plan Google Maps du 9 rue Andr\u00e9 Darbon \u00e0 Bordeaux';f.width='800';f.height='600';f.referrerPolicy='no-referrer-when-downgrade';f.allowFullscreen=true;f.style.display='none';
      f.addEventListener('load',function(){charge=true;f.style.display='';if(cp.parentNode)cp.parentNode.removeChild(cp);});
      cp.parentNode.appendChild(f);f.src='https://www.google.com/maps?q=9+rue+Andr%C3%A9+Darbon+33300+Bordeaux&output=embed';
      setTimeout(function(){if(!charge){if(f.parentNode)f.parentNode.removeChild(f);cp.disabled=false;cp.textContent=texte;lance=false;}},10000);
    };
    cp.addEventListener('click',function(){charger();});
    if('IntersectionObserver' in window){
      var obs=new IntersectionObserver(function(es){if(es[0].isIntersecting){obs.disconnect();charger();}},{rootMargin:'600px 0px'});
      obs.observe(cp.parentNode);
    }else{charger();}
  }

  /* Formulaire : messages d'erreur rédigés, reliés au champ et annoncés */
  var fo=d.querySelector('form.formulaire');
  if(fo){
    fo.setAttribute('novalidate','');
    var msgs={nom:'Indiquez votre nom et votre prénom.',email:'Indiquez une adresse e-mail valide, par exemple nom@entreprise.fr.',telephone:'Indiquez un numéro de téléphone valide.',besoin:'Choisissez votre besoin dans la liste.',postes:'Indiquez un nombre de postes entre 1 et 30.',consentement:'Cochez cette case pour envoyer votre demande.'};
    var signaler=function(ch,actif){
      var id='err-'+ch.name,p=d.getElementById(id),liens=(ch.getAttribute('aria-describedby')||'').split(' ').filter(function(x){return x&&x!==id;});
      if(actif){
        if(!p){p=d.createElement('p');p.className='erreur';p.id=id;var apres=ch.type==='checkbox'?ch.closest('label'):ch;apres.parentNode.insertBefore(p,apres.nextSibling);}
        p.textContent=msgs[ch.name]||'Ce champ est à vérifier.';ch.setAttribute('aria-invalid','true');liens.push(id);
      }else{if(p)p.parentNode.removeChild(p);ch.removeAttribute('aria-invalid');}
      if(liens.length)ch.setAttribute('aria-describedby',liens.join(' '));else ch.removeAttribute('aria-describedby');
    };
    fo.addEventListener('submit',function(e){
      var premier=null;
      [].forEach.call(fo.elements,function(ch){if(!ch.name||ch.name==='website'||!ch.willValidate)return;var ok=ch.checkValidity();signaler(ch,!ok);if(!ok&&!premier)premier=ch;});
      if(premier){e.preventDefault();premier.focus();}
    });
    fo.addEventListener('change',function(e){var ch=e.target;if(ch.getAttribute('aria-invalid')==='true'&&ch.checkValidity())signaler(ch,false);});
  }
})();
