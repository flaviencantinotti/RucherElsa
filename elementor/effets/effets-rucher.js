(function(){
  /* Dans l'editeur, trois calques fixes couvriraient le canevas. */
  if(document.body.classList.contains('elementor-editor-active'))return;
  if(window.__rdlTorche)return;
  window.__rdlTorche=1;
  /* L'ecoute est posee sur le conteneur, pas sur le lien : selon la
     version, Elementor rend le bouton en <a> ou en <button>. */
  var burger=document.querySelector('.rdl-burger'),
      entete=document.querySelector('.rdl-nav');
  if(burger&&entete){
    var cible=burger.querySelector('a,button')||burger;
    cible.setAttribute('aria-label','Ouvrir le menu');
    burger.addEventListener('click',function(e){
      e.preventDefault();
      entete.classList.toggle('rdl-ouvert');
    });
    /* Refermer apres avoir choisi une destination. */
    entete.querySelectorAll('.rdl-menu a').forEach(function(a){
      a.addEventListener('click',function(){
        entete.classList.remove('rdl-ouvert');
      });
    });
  }
  /* Le halo n'a de sens qu'avec un pointeur ; le burger, lui, sert
     precisement la ou il n'y en a pas. */
  if(window.matchMedia('(hover:hover)').matches){
    document.addEventListener('mousemove',function(e){
      var r=document.documentElement.style;
      r.setProperty('--rdl-x',e.clientX+'px');
      r.setProperty('--rdl-y',e.clientY+'px');
    });
  }
})();
