# Image prompts — Ti kreyon espwa

Five prompts for an AI image generator (Antigravity, Midjourney, DALL·E, Firefly…).
Style across the whole set: **warm documentary photography**, natural light, vivid but true colours,
real texture, no plastic "stock photo" gloss.

## Rules that apply to all five

- **Dignity, never misery.** Children are actors of their own story: standing, engaged, doing something.
  No dirt-as-decoration, no pity framing, no adult saviour towering over a child.
- **Real Haiti.** Caribbean light, tropical vegetation, tin roofs, coloured walls, Haitian dust —
  not a generic "Africa" backdrop.
- Colour palette should echo the brand: azure `#0077B6`, sun yellow `#FFB703`, leaf green `#2A9D8F`.
- Add to any generator that supports negatives:
  `--no text, watermark, logo, distorted hands, extra fingers, deformed faces, oversaturated HDR, plastic skin`
- Reference aspect ratios: Midjourney `--ar 16:9` / `--ar 4:3` / `--ar 1:1`; Antigravity or DALL·E: state the ratio in words.
- If you use **real photos of real children instead**, that is always better — with written consent from the family.

---

## 1. Hero — `assets/img/hero.jpg` (16:9, wide, used as a full-bleed background)

> Warm documentary photograph of a Haitian child, around 8 years old, smiling openly while holding a
> yellow pencil above an open notebook. Bright natural morning light, shallow depth of field. Behind them,
> softly blurred, a sunlit Caribbean street in Haiti: pastel painted walls, green foliage, blue sky.
> The child looks directly at the camera with confidence and joy. Vivid azure blue and sunny yellow tones,
> photojournalistic style, 50mm lens, natural skin texture, no studio lighting.
> `--ar 16:9`

Framing note: the site darkens this image with a blue gradient and puts the headline on the **left**,
so keep the child slightly **right of centre** and leave the left third visually calm.

---

## 2. Education — `assets/img/education.jpg` (4:3)

> Warm documentary photograph of three Haitian schoolchildren in uniform sitting side by side, opening
> brand-new school bags full of notebooks, pencils and coloured supplies. They look excited and focused.
> Simple classroom or community room, wooden bench, sunlight coming through a window, a small shelf of
> books behind them. Natural colours, blue and yellow accents, photojournalism, 35mm lens, no flash.
> `--ar 4:3`

---

## 3. Creativity — `assets/img/creativity.jpg` (4:3)

> Warm documentary photograph seen slightly from above: a circle of six Haitian children, ages 6 to 12,
> sitting on a bright mat, drawing and painting on large sheets of paper. Colourful crayons, paint pots
> and finished drawings scattered around them. One child proudly lifts up their drawing. Afternoon light,
> joyful and concentrated faces, warm yellows and greens, authentic reportage style, wide angle.
> `--ar 4:3`

---

## 4. Nutrition — `assets/img/nutrition.jpg` (4:3)

> Warm documentary photograph of a Haitian woman volunteer serving a steaming plate of rice and beans to a
> smiling child holding out their plate, at a simple community canteen. Other children eating together at a
> long table in the background, gently blurred. Steam visible above the food, natural daylight from a doorway,
> hopeful and dignified atmosphere, green and warm-yellow tones, 35mm reportage photography.
> `--ar 4:3`

---

## 5. Hope / community — `assets/img/gallery-5.jpg` (16:9 or 1:1 for the gallery grid)

> Warm documentary photograph of a group of about twelve Haitian children of different ages walking together
> along a dirt road, laughing, school bags on their shoulders, arms around each other. Behind them the green
> Haitian hills and a wide sky at golden hour, backlit by low warm sunlight. Sense of community,
> forward movement and hope. Vivid natural colours, slight lens flare, photojournalistic, 50mm.
> `--ar 16:9`

---

## Other gallery slots

`gallery-1.jpg` … `gallery-6.jpg` are square (1:1) tiles. Reuse variations of prompts 2–5, or crop your
own event photos. Their captions in `index.html` are, in order:
school kit distribution, painting workshop, meal service, reading corner, team and children, first day of school.

## After generating

1. Save each file under `assets/img/` with **exactly** the filename listed above.
2. Compress before publishing (target < 300 KB each; [squoosh.app](https://squoosh.app) or `sips` on macOS).
   The hero can go up to ~500 KB since it is full-bleed.
3. Nothing else to change in the code — each image slot already exists and falls back to an illustration
   until the file is present.
