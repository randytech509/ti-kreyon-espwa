# Ti kreyon espwa — website

Single-page site for the Haitian NGO **Ti kreyon espwa** (Haiti).
Motto: *« Chak timoun gen yon bèl istwa pou l ekri. »* — Every child has a beautiful story to write.

```
index.html          the whole site (HTML + CSS + JS, no build step, no dependency)
robots.txt          crawling rules + sitemap pointer
sitemap.xml         single URL, update <lastmod> when the content changes
IMAGE-PROMPTS.md    5 prompts to generate the illustrations with an AI image generator
assets/img/         drop the images here (see filenames below)
```

Source language is **English**; visitors switch to **Kreyòl / Français / Español** from the header
via the Google Website Translator (free, no API key, no billing).

---

## 1. Values to replace before going live

Search `index.html` for `REPLACE` — every placeholder is flagged with a comment.

| What | Where | Current placeholder |
|---|---|---|
| ~~Contact form~~ | done — POST vers `/api/contact`, voir §3 | — |
| PayPal donation link | Support section, "Give with PayPal" | `paypal.com/paypalme/REPLACE-ME` |
| Bank details | Support section, `.bank` list | Bank, account no., SWIFT |
| ~~Donation phone line~~ | done — `+1 407 664 0650` (donation line, contact block, WhatsApp, JSON-LD) | — |
| ~~Email~~ | done — `administration@tikreyonespwa.org` (Namecheap PrivateEmail) | — |
| Facebook / Instagram | `.socials` | `REPLACE-ME` |
| Exact address | Contact block, footer, JSON-LD | `Haiti` — add a city or street only if you want it public |

Impact counters and testimonials are **not** placeholders any more — they were removed, see §2.

Le formulaire de contact n'utilise plus de service tiers : il poste sur `/api/contact`,
une fonction Vercel qui envoie l'e-mail via Resend (§3).

---

## 2. Editorial integrity — read before changing the content

The site says out loud that its images are **AI-generated illustrations**, and explains why: a
photograph of a child in need follows that child for life. This is not a disclaimer bolted on, it is
part of the argument — the gallery lead, the `.ai-note` line under the grid, the *"Why you will not
see their faces"* card and the contact block all say the same thing. If you ever add real photos,
change all four together, and only with **written, specific, revocable** consent from the family
(the standard applied in Haiti under the Convention on the Rights of the Child, art. 16; parental
silence is not consent). Burkina Faso went further in July 2026 and banned NGO images of vulnerable
people shown next to the aid they receive — a good indication of where the norm is heading.

Three things were removed for the same reason and must not come back invented:

- **Impact counters** (120 children / 3500 meals / 45 workshops / 18 volunteers) → replaced by four
  commitments. The markup to restore real counters is kept in an HTML comment inside `#impact`, and
  the JS still animates any `.stat__num` it finds. Publish only figures you can prove on request.
- **Two testimonials** attributed to named people → replaced by the transparency cards. Real quotes
  need written permission, first name only, and no school, street or health detail.
- **"100% of donations go to programs"** → replaced by *"Every gift is tracked. Ask us what yours
  paid for."* Restore a percentage only if your accounts back it.

---

## 3. Formulaire de contact — `/api/contact`

`api/contact.js` reçoit le formulaire des deux pages et envoie le message à l'ONG via
[Resend](https://resend.com). Aucune dépendance npm : `fetch` est natif sur le runtime Node de Vercel.

**Variables d'environnement** (Vercel → Settings → Environment Variables) :

| Variable | Obligatoire | Rôle |
|---|---|---|
| `RESEND_API_KEY` | oui | clé API Resend (`re_…`). Sans elle l'endpoint répond `503 not_configured` et le site invite le visiteur à écrire directement. |
| `CONTACT_TO` | non | destinataire, défaut `administration@tikreyonespwa.org` |
| `RESEND_FROM` | non | expéditeur, défaut `Ti kreyon espwa <onboarding@resend.dev>` |

**Séquence de mise en service :**

1. Créer un compte sur resend.com, générer une clé API, la coller dans `RESEND_API_KEY`.
2. Tant que le domaine n'est pas vérifié chez Resend, `onboarding@resend.dev` **n'accepte comme
   destinataire que l'adresse du compte Resend** : mettre cette adresse dans `CONTACT_TO` pour
   tester tout de suite.
3. Une fois `tikreyonespwa.org` pointé sur Vercel, ajouter le domaine dans resend.com/domains,
   poser les enregistrements DNS chez Namecheap, puis passer `RESEND_FROM` à
   `Ti kreyon espwa <sit@tikreyonespwa.org>` et `CONTACT_TO` à `administration@tikreyonespwa.org`.

**Ce que fait l'endpoint** : refuse tout sauf POST ; répond `200` sans rien envoyer si le champ
piège `_gotcha` est rempli (le robot croit avoir réussi) ; valide nom, e-mail et longueur du
message ; rejette au-delà de deux liens ; limite à 4 envois par IP toutes les 10 minutes ; échappe
le HTML du message ; met le visiteur en `reply_to`, si bien qu'un simple « Répondre » lui écrit
directement. Le champ caché `lang` indique si le message vient de la page anglaise ou kreyòle.

La limite par IP est en mémoire : Vercel peut faire tourner plusieurs instances et les recycler,
elle freine un robot bavard mais ne remplace pas un compteur partagé. Si le spam passe, l'étape
suivante est Cloudflare Turnstile.

---

## 4. Images

The 10 images are **already in place** in `assets/img/` (generated with `IMAGE-PROMPTS.md`):

```
hero.jpg (1920×1071)   education.jpg / creativity.jpg / nutrition.jpg (1080×806)
gallery-1…4,6.jpg (800×800)   gallery-5.jpg (1080×602)
```

**Logo** — dérivé du fichier fourni, fond blanc rendu transparent :

```
logo.png (460px, complet + devise)   → carte blanche du footer
logo-mark.png (165×220, enfant+crayon) → badge du header
favicon.png (96×96)   apple-touch-icon.png (180×180)
```

Pour régénérer une variante depuis un nouveau fichier logo :
`magick source.jpg -fuzz 6% -transparent white -trim +repage -resize 460x -colors 128 assets/img/logo.png`

To replace one — a real photo of the children, for instance — just overwrite the file, keeping the
same name and roughly the same ratio. Nothing to change in the code.

If a file is missing, its slot falls back to a coloured brand illustration and the `<img>` is removed
from the DOM by an `onerror` handler, so no broken-image icon ever appears.

The hero crop is tuned for this photo (`background-position:70% 32%` desktop, `72% 22%` mobile) with a
gradient veil that is dense on the left, behind the headline, and light on the right, over the child.
Swap in a photo framed differently and you will want to adjust those two values in the `.hero__photo`
rules.

---

## 5. Translation

**Le kreyòl est une vraie page**, `/ht`, écrite à la main par le fondateur et générée par
`build-ht.py` depuis `index.html` + `translations_ht.csv` :

```bash
python3 build-ht.py     # regénère ht/index.html
```

Le script échoue en nommant le segment fautif si une phrase anglaise a changé sans que le CSV
suive — les deux pages ne peuvent pas diverger en silence. **Toute modification de contenu se fait
dans `index.html`, jamais dans `ht/index.html`**, qui est un fichier généré.

Français et espagnol passent encore par le widget Google (`en, fr, es`), piloté par le cookie
`googtrans` ; le choix est mémorisé en `localStorage`. Depuis `/ht`, les entrées « Fransè » et
« Panyòl » renvoient sur `/?lang=fr|es` : Google traduit donc toujours depuis l'anglais, sa
meilleure source, jamais depuis le kreyòl.

Deux choses à savoir :

- **Le widget exige une vraie origine HTTP.** Ouvrir `index.html` en `file://` affiche la page mais
  la traduction ne tourne pas. Tester via un serveur local (plus bas) ou une fois déployé.
- Brand names — *Ti kreyon espwa*, *Sak Lekòl*, *Vant Plen*, the Creole motto, phone numbers, bank
  details — carry `translate="no"` / `class="notranslate"` so Google leaves them intact.

Everything else on the page works normally if the Google script is blocked or fails.

---

## 6. Run locally

```bash
cd ~/dev/ti-kreyon-espwa
python3 -m http.server 8080
# then open http://localhost:8080
```

## 7. Deploy — Vercel + Namecheap

There is no backend and no build step: Vercel serves the folder as-is (`vercel.json` sets a long
cache on `assets/` and no cache on the HTML, so a content fix is live immediately).

```bash
npx vercel        # preview deployment
npx vercel --prod # production
```

Or connect the GitHub repo once in the Vercel dashboard — every push to `main` then deploys itself.
Framework preset: **Other**. Build command: none. Output directory: the repository root.

**Domain (`tikreyonespwa.org`, registered at Namecheap):** add the domain *and* its `www` variant in
Vercel → Settings → Domains, then copy the records Vercel displays into Namecheap → *Advanced DNS*
(not the default BasicDNS host records screen). Vercel has changed its apex IP in the past — always
copy the values it shows you rather than any address written down here. HTTPS is issued automatically
once the records resolve, usually within the hour.

Other static hosts work too (GitHub Pages, Hostinger `public_html/`) — it is plain HTML.

---

## 8. Possible next steps

- **Une version française écrite à la main**, sur le modèle de `/ht` : traduire
  `translations_ht.csv` en `translations_fr.csv`, dupliquer `build-ht.py`. Google resterait alors
  pour l'espagnol seulement. Le kreyòl est déjà fait — c'était le plus urgent, Google le traduit mal.
- A **stories blog** — one page per child's drawing or letter; that is the emotional engine of the site.
- **Annual report page** with the financial breakdown (strong trust signal for corporate partners).
- **Recurring donations** (PayPal subscription button or Stripe payment link) for the sponsorship program.
- Local payment rails (MonCash / NatCash) for donors inside Haiti.
- Basic analytics (Plausible or Umami — privacy-friendly, no cookie banner needed).
