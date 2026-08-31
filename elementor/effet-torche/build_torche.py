#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genere le module optionnel de l'effet lampe torche, en un widget HTML.

Le suivi de la souris demande quatre lignes de JavaScript : aucun reglage
du panneau Elementor ne sait le produire. On l'isole donc dans un seul
widget dedie, place en fin de page, plutot que d'eparpiller du code dans
les conteneurs de contenu.

Usage : python3 build_torche.py
Sortie : torche.json
"""

import json
import os

MIEL = "#DC9F2E"

# La feuille et le script sont repris de index.html. Deux ajouts :
# - une garde qui neutralise l'effet dans l'editeur Elementor, ou des
#   calques fixes couvriraient le canevas et empecheraient de cliquer ;
# - une garde qui l'inhibe sur appareil tactile, ou il n'y a pas de
#   pointeur a suivre et ou le halo resterait fige au centre.
EFFET = """<style>
#rdl-hexfield,#rdl-vignette,#rdl-glow{
  position:fixed;inset:0;pointer-events:none;
}
#rdl-hexfield{
  z-index:1;opacity:.5;
  background-image:url("REMPLACER_PAR_URL_DE_LA_TRAME");
  background-repeat:repeat;background-size:52px 90px;
}
#rdl-vignette{
  z-index:1;
  background:radial-gradient(circle 460px at var(--rdl-x,50%) var(--rdl-y,50%),
    transparent 0%, rgba(0,0,0,.35) 75%);
}
#rdl-glow{
  z-index:3;mix-blend-mode:screen;transition:opacity .4s ease;
  background:radial-gradient(circle 380px at var(--rdl-x,50%) var(--rdl-y,50%),
    rgba(220,159,46,.45), rgba(220,159,46,.10) 40%, transparent 70%);
}
@media (hover:none){#rdl-glow,#rdl-vignette{display:none}}
</style>
<div id="rdl-hexfield"></div>
<div id="rdl-vignette"></div>
<div id="rdl-glow"></div>
<script>
(function(){
  if(document.body.classList.contains('elementor-editor-active')) return;
  if(!window.matchMedia('(hover:hover)').matches) return;
  if(window.__rdlTorche) return;
  window.__rdlTorche = true;
  document.addEventListener('mousemove', function(e){
    var r = document.documentElement.style;
    r.setProperty('--rdl-x', e.clientX + 'px');
    r.setProperty('--rdl-y', e.clientY + 'px');
  });
})();
</script>"""


def construire():
    return {
        "content": [{
            "id": "torche01",
            "elType": "container",
            "settings": {
                "content_width": "full",
                "width": {"unit": "%", "size": 100, "sizes": []},
                "padding": {"unit": "px", "top": "0", "right": "0",
                            "bottom": "0", "left": "0", "isLinked": True},
                "min_height": {"unit": "px", "size": 0, "sizes": []},
            },
            "elements": [{
                "id": "torche02",
                "elType": "widget",
                "widgetType": "html",
                "settings": {"html": EFFET},
                "elements": [],
            }],
            "isInner": False,
        }],
        "page_settings": [],
        "version": "0.4",
        "title": "Rucher d'Elsa — effet lampe torche",
        "type": "container",
    }


if __name__ == "__main__":
    ici = os.path.dirname(os.path.abspath(__file__))
    sortie = os.path.join(ici, "torche.json")
    with open(sortie, "w", encoding="utf-8") as f:
        json.dump(construire(), f, ensure_ascii=False, separators=(",", ":"))
        f.write("\n")
    print("torche.json généré — %.1f Ko" % (os.path.getsize(sortie) / 1024))
    print("Pensez à remplacer REMPLACER_PAR_URL_DE_LA_TRAME par l'URL de")
    print("trame-hexagones.svg une fois envoyée dans la médiathèque.")
