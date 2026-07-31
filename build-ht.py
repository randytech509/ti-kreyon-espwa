#!/usr/bin/env python3
"""Génère ht/index.html à partir de index.html + translations_ht.csv.

Les deux pages ne doivent jamais diverger : on ne modifie que index.html,
puis on relance `python3 build-ht.py`.

    python3 build-ht.py

Le script signale tout segment traduit qui n'a pas été retrouvé dans la page
anglaise — c'est le signal qu'une phrase a changé côté source et qu'il faut
mettre à jour translations_ht.csv.
"""
import html
import io
import os
import re
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "index.html")
CSV = os.path.join(ROOT, "translations_ht.csv")
OUT_DIR = os.path.join(ROOT, "ht")
OUT = os.path.join(OUT_DIR, "index.html")

SCRIPT_RE = re.compile(r"<script\b.*?</script>", re.S | re.I)

# Trois phrases contiennent une balise inline (montants en gras, coeur SVG).
# On les traduit par morceaux pour conserver le balisage.
SPLIT_BY_MARKUP = {
    "107": [
        ("A school kit costs about", "Yon sak lekòl koute anviwon"),
        (". A month of hot meals for one child, about", ". Yon mwa repa cho pou yon timoun, anviwon"),
        (". Whatever you give lands directly in a child's hands in Haiti.",
         ". Nenpòt sa ou bay rive dirèk nan men yon timoun an Ayiti."),
    ],
    "139": [
        ("We never share your details. Fields marked", "Nou pa janm pataje enfòmasyon ou. Jaden ki make"),
        ("are required.", "obligatwa."),
    ],
    "152": [
        ('<span class="made">Made with', '<span class="made">Fèt ak'),
        ('<span class="sr-only">love</span> in Haiti',
         '<span class="sr-only">lanmou</span> an Ayiti'),
    ],
}


def load_pairs():
    pairs = []
    with io.open(CSV, encoding="utf-8") as fh:
        for line in fh:
            line = line.rstrip("\n")
            if not line or line.startswith("num|"):
                continue
            num, en, ht = line.split("|", 2)
            pairs.append((num, en, ht))
    return pairs


def protect_scripts(doc):
    """Sort les <script> du document : ni entités ni traduction ne s'y appliquent."""
    blocks = []

    def stash(m):
        blocks.append(m.group(0))
        return "\x00SCRIPT%d\x00" % (len(blocks) - 1)

    return SCRIPT_RE.sub(stash, doc), blocks


def restore_scripts(doc, blocks):
    for i, block in enumerate(blocks):
        doc = doc.replace("\x00SCRIPT%d\x00" % i, block)
    return doc


LANG_MENU_HT = """        <ul class="lang__menu" id="langMenu" role="menu" aria-labelledby="langToggle">
          <li role="none"><a role="menuitem" href="/" hreflang="en" lang="en">English <span class="lang__native">English</span>
            <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg></a></li>
          <li role="none"><a role="menuitem" href="/ht/" hreflang="ht" lang="ht" aria-current="true">Kreyòl ayisyen <span class="lang__native">Kreyòl</span>
            <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg></a></li>
          <li role="none"><a role="menuitem" href="/?lang=fr" hreflang="fr" lang="fr">Fransè <span class="lang__native">Français</span>
            <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg></a></li>
          <li role="none"><a role="menuitem" href="/?lang=es" hreflang="es" lang="es">Panyòl <span class="lang__native">Español</span>
            <svg class="check" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M20 6L9 17l-5-5"/></svg></a></li>
        </ul>"""

# Sur /ht/ il n'y a pas de widget Google : le menu n'a plus qu'à s'ouvrir et se fermer.
LANG_JS_HT = """  /* ============================================================
     Language switcher — plain links: Kreyòl is a hand-written page,
     French and Spanish go back to the English page and let Google run there
     ============================================================ */
  var langToggle = document.getElementById("langToggle");
  var langMenu = document.getElementById("langMenu");
  var langLinks = Array.prototype.slice.call(langMenu.querySelectorAll("a[role=menuitem]"));

  var closeLangMenu = function (refocus) {
    if (!langMenu.classList.contains("is-open")) return;
    langMenu.classList.remove("is-open");
    langToggle.setAttribute("aria-expanded", "false");
    if (refocus) langToggle.focus();
  };
  var openLangMenu = function (focusIndex) {
    langMenu.classList.add("is-open");
    langToggle.setAttribute("aria-expanded", "true");
    if (typeof focusIndex === "number" && langLinks[focusIndex]) langLinks[focusIndex].focus();
  };

  langToggle.addEventListener("click", function (e) {
    e.stopPropagation();
    if (langMenu.classList.contains("is-open")) closeLangMenu(false); else openLangMenu();
  });
  langToggle.addEventListener("keydown", function (e) {
    if (e.key === "ArrowDown") { e.preventDefault(); openLangMenu(0); }
    else if (e.key === "ArrowUp") { e.preventDefault(); openLangMenu(langLinks.length - 1); }
  });
  langMenu.addEventListener("keydown", function (e) {
    var idx = langLinks.indexOf(document.activeElement);
    if (idx === -1) return;
    if (e.key === "ArrowDown") { e.preventDefault(); langLinks[(idx + 1) % langLinks.length].focus(); }
    else if (e.key === "ArrowUp") { e.preventDefault(); langLinks[(idx - 1 + langLinks.length) % langLinks.length].focus(); }
    else if (e.key === "Home") { e.preventDefault(); langLinks[0].focus(); }
    else if (e.key === "End") { e.preventDefault(); langLinks[langLinks.length - 1].focus(); }
    else if (e.key === "Tab") closeLangMenu(false);
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".lang")) closeLangMenu(false);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") closeLangMenu(true);
  });

  // Le visiteur qui arrive ici a choisi le kreyòl : on efface un éventuel
  // cookie Google laissé par une visite précédente sur la page anglaise.
  document.cookie = "googtrans=/en/en; path=/; max-age=" + (60 * 60 * 24 * 365);
  try { localStorage.setItem("tk2e-lang", "ht"); } catch (err) { /* private mode */ }
"""


def main():
    doc = io.open(SRC, encoding="utf-8").read()
    doc, scripts = protect_scripts(doc)

    # Les entités du HTML source (&mdash;, &amp;…) deviennent des caractères
    # littéraux pour que les phrases correspondent au CSV telles qu'extraites.
    doc = html.unescape(doc)

    # Traduction : les segments les plus longs d'abord, sinon un mot isolé
    # ("Education") viendrait amputer une phrase qui le contient.
    pairs = load_pairs()
    missing = []

    for num, en, ht in sorted(pairs, key=lambda p: -len(p[1])):
        if num in SPLIT_BY_MARKUP:
            # Phrase coupée par une balise inline (<b>, <svg>) : on traduit
            # morceau par morceau pour ne pas effacer la mise en forme.
            for en_part, ht_part in SPLIT_BY_MARKUP[num]:
                rx = re.compile(r"\s+".join(map(re.escape, en_part.split())))
                if not rx.search(doc):
                    missing.append((num, en_part[:60]))
                    continue
                doc = rx.sub(lambda m, t=ht_part: t, doc, count=1)
            continue
        # Le HTML coupe les longues phrases sur plusieurs lignes : on tolère
        # n'importe quelle suite d'espaces là où le CSV a un espace simple.
        rx = re.compile(r"\s+".join(map(re.escape, en.split())))
        if not rx.search(doc):
            missing.append((num, en[:60]))
            continue
        doc = rx.sub(lambda m, t=ht: t, doc)

    # ---- ajustements structurels de la page kreyòl -------------------------
    edits = [
        ('<html lang="en">', '<html lang="ht">'),
        ('<link rel="canonical" href="https://tikreyonespwa.org/">',
         '<link rel="canonical" href="https://tikreyonespwa.org/ht/">'),
        ('<meta property="og:url" content="https://tikreyonespwa.org/">',
         '<meta property="og:url" content="https://tikreyonespwa.org/ht/">'),
        ('<meta property="og:locale" content="en_US">',
         '<meta property="og:locale" content="ht_HT">'),
        ('value="New message from tikreyonespwa.org"',
         'value="New message from tikreyonespwa.org (Kreyòl)"'),
        # Le widget Google ne tourne pas ici
        ('<div id="google_translate_element" inert aria-hidden="true"></div>\n', ''),
    ]
    for old, new in edits:
        if old not in doc:
            missing.append(("struct", old[:60]))
            continue
        doc = doc.replace(old, new, 1)

    # Le hero affiche la devise en kreyòl puis sa traduction : sur la page
    # kreyòle, cette deuxième ligne répéterait la première mot pour mot.
    motto_re = re.compile(r'\s*<p class="motto__en">.*?</p>', re.S)
    if not motto_re.search(doc):
        missing.append(("struct", "motto__en"))
    doc = motto_re.sub("", doc, count=1)

    # Menu de langue
    menu_re = re.compile(r'        <ul class="lang__menu".*?</ul>', re.S)
    if not menu_re.search(doc):
        missing.append(("struct", "lang__menu"))
    doc = menu_re.sub(lambda m: LANG_MENU_HT, doc, count=1)
    doc = doc.replace('<span id="langCurrent">EN</span>', '<span id="langCurrent">HT</span>', 1)

    # Chemins des assets : /ht/index.html est un cran plus bas
    doc = doc.replace('="assets/', '="/assets/').replace('url("assets/', 'url("/assets/')

    doc = restore_scripts(doc, scripts)

    # ---- ajustements dans les <script> (restaurés intacts) -----------------
    js_edits = [
        ('<script src="https://translate.google.com/translate_a/element.js?cb=googleTranslateElementInit" defer></script>\n', ''),
        ('"url": "https://tikreyonespwa.org/",', '"url": "https://tikreyonespwa.org/ht/",'),
        ('"slogan": "Every child has a beautiful story to write",',
         '"slogan": "Chak timoun gen yon bèl istwa pou l ekri",'),
    ]
    for old, new in js_edits:
        if old not in doc:
            missing.append(("json-ld", old[:50]))
            continue
        doc = doc.replace(old, new, 1)

    # Le bloc JS du sélecteur de langue est remplacé en entier
    start = doc.find("  /* ============================================================\n     Language switcher")
    end = doc.find("  /* ---------- Contact form", start)
    if start == -1 or end == -1:
        missing.append(("struct", "bloc JS Language switcher"))
    else:
        doc = doc[:start] + LANG_JS_HT + "\n" + doc[end:]

    os.makedirs(OUT_DIR, exist_ok=True)
    io.open(OUT, "w", encoding="utf-8").write(doc)

    print("ht/index.html écrit — %d segments" % len(pairs))
    if missing:
        print("\nNON APPLIQUÉ (%d) :" % len(missing))
        for kind, txt in missing:
            print("  [%s] %s" % (kind, txt))
        sys.exit(1)


if __name__ == "__main__":
    main()
