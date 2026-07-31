# Ti kreyon espwa — website

Single-page site for the Haitian NGO **Ti kreyon espwa** (Carrefour, Haiti).
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
| Contact form endpoint | `<form id="contactForm" action=...>` | `https://formspree.io/f/YOUR_FORM_ID` |
| PayPal donation link | Support section, "Give with PayPal" | `paypal.com/paypalme/REPLACE-ME` |
| Bank details | Support section, `.bank` list | Bank, account no., SWIFT |
| Donation phone line | Support section + `tel:` link | `+509 0000 0000` / `tel:+50900000000` |
| Email | Contact block, footer, JS fallback message | `contact@tikreyonespwa.org` |
| Phone / WhatsApp | Contact block, footer, socials | `+509 0000 0000`, `wa.me/50900000000` |
| Facebook / Instagram | `.socials` | `REPLACE-ME` |
| Exact address | Contact block | `Carrefour, Ouest, Haiti` |

Impact counters and testimonials are **not** placeholders any more — they were removed, see §2.

**Formspree setup:** create a free form on [formspree.io](https://formspree.io), copy the endpoint
(`https://formspree.io/f/xxxxxxx`) into the form's `action`. Nothing else to do — the JS posts with
`fetch` and shows the result inline, so the visitor never leaves the page. Until you paste a real
endpoint, the form politely tells the visitor to email instead. The honeypot field (`_gotcha`) is
already wired for spam.

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

## 3. Images

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

## 4. Translation

The header language menu writes the `googtrans` cookie and drives the hidden Google widget
(`en, ht, fr, es`). The chosen language is remembered in `localStorage`.

Two things to know:

- **It needs a real HTTP origin.** Opening `index.html` with `file://` loads the page fine but the
  translator will not run. Test with a local server (below) or once deployed.
- Brand names — *Ti kreyon espwa*, *Sak Lekòl*, *Vant Plen*, the Creole motto, phone numbers, bank
  details — carry `translate="no"` / `class="notranslate"` so Google leaves them intact.

Everything else on the page works normally if the Google script is blocked or fails.

---

## 5. Run locally

```bash
cd ~/dev/ti-kreyon-espwa
python3 -m http.server 8080
# then open http://localhost:8080
```

## 6. Deploy — Vercel + Namecheap

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

## 7. Possible next steps

- **Real multilingual content** instead of machine translation: hand-written EN / HT / FR versions
  (`/index.html`, `/ht/`, `/fr/`) with `hreflang` tags. Better for SEO and for the Creole nuance
  Google gets wrong. The Cloud Translation API (paid, needs a key) is *not* a good fit here — a key
  in static HTML is public; it would require a small server proxy.
- A **stories blog** — one page per child's drawing or letter; that is the emotional engine of the site.
- **Annual report page** with the financial breakdown (strong trust signal for corporate partners).
- **Recurring donations** (PayPal subscription button or Stripe payment link) for the sponsorship program.
- Local payment rails (MonCash / NatCash) for donors inside Haiti.
- Basic analytics (Plausible or Umami — privacy-friendly, no cookie banner needed).
