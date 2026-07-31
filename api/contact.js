/**
 * POST /api/contact — reçoit le formulaire du site et l'envoie par e-mail via Resend.
 *
 * Variables d'environnement (Vercel → Settings → Environment Variables) :
 *   RESEND_API_KEY   obligatoire, commence par re_
 *   CONTACT_TO       destinataire (défaut administration@tikreyonespwa.org)
 *   RESEND_FROM      expéditeur — doit appartenir à un domaine vérifié chez Resend.
 *                    Tant que tikreyonespwa.org ne l'est pas, garder onboarding@resend.dev,
 *                    qui n'accepte QUE l'adresse du compte Resend comme destinataire.
 *
 * Aucune dépendance npm : fetch est natif sur le runtime Node de Vercel.
 */

const TO = process.env.CONTACT_TO || "administration@tikreyonespwa.org";
const FROM = process.env.RESEND_FROM || "Ti kreyon espwa <onboarding@resend.dev>";
const MAX = { name: 80, email: 120, topic: 60, message: 2000 };

/**
 * Limite par IP. Best-effort : Vercel peut faire tourner plusieurs instances,
 * chacune avec sa propre mémoire, et les recycle. Ça freine un bot bavard,
 * ça ne remplace pas un vrai rate-limiter à état partagé.
 */
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 4;
const hits = new Map();

function tooMany(ip) {
  const now = Date.now();
  const seen = (hits.get(ip) || []).filter((t) => now - t < WINDOW_MS);
  seen.push(now);
  hits.set(ip, seen);
  if (hits.size > 500) {
    // Purge : on ne garde pas indéfiniment les IP inactives en mémoire
    for (const [key, times] of hits) {
      if (!times.some((t) => now - t < WINDOW_MS)) hits.delete(key);
    }
  }
  return seen.length > MAX_PER_WINDOW;
}

function readBody(req) {
  const b = req.body;
  if (!b) return {};
  if (typeof b === "string") {
    try {
      return JSON.parse(b);
    } catch (err) {
      return Object.fromEntries(new URLSearchParams(b));
    }
  }
  return b;
}

const clean = (v, max) => String(v == null ? "" : v).trim().slice(0, max);

const escapeHtml = (s) =>
  s.replace(/[&<>"']/g, (c) =>
    ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c])
  );

module.exports = async function handler(req, res) {
  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ ok: false, error: "method_not_allowed" });
  }

  const body = readBody(req);

  // Champ piège : invisible pour un humain, rempli par les robots.
  // On répond 200 pour que le bot croie avoir réussi et n'insiste pas.
  if (clean(body._gotcha, 100)) {
    return res.status(200).json({ ok: true });
  }

  const name = clean(body.name, MAX.name);
  const email = clean(body.email, MAX.email);
  const topic = clean(body.topic, MAX.topic) || "—";
  const message = clean(body.message, MAX.message);
  const lang = clean(body.lang, 5) === "ht" ? "ht" : "en";

  if (!name || !email || message.length < 10) {
    return res.status(400).json({ ok: false, error: "missing_fields" });
  }
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(email)) {
    return res.status(400).json({ ok: false, error: "bad_email" });
  }
  // Un message de contact légitime ne contient pas cinq liens.
  if ((message.match(/https?:\/\//gi) || []).length > 2) {
    return res.status(400).json({ ok: false, error: "looks_like_spam" });
  }

  const ip =
    (req.headers["x-forwarded-for"] || "").split(",")[0].trim() ||
    req.socket?.remoteAddress ||
    "unknown";
  if (tooMany(ip)) {
    return res.status(429).json({ ok: false, error: "too_many_requests" });
  }

  if (!process.env.RESEND_API_KEY) {
    console.error("RESEND_API_KEY manquante : impossible d'envoyer le message");
    return res.status(503).json({ ok: false, error: "not_configured" });
  }

  const when = new Date().toISOString().replace("T", " ").slice(0, 16) + " UTC";
  const text = [
    `Non / Name : ${name}`,
    `Imèl / Email : ${email}`,
    `Sijè / Topic : ${topic}`,
    `Paj / Page : ${lang === "ht" ? "kreyòl (/ht)" : "anglais (/)"}`,
    `Dat : ${when}`,
    "",
    message,
  ].join("\n");

  const html = `<div style="font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;line-height:1.6;color:#12303C">
  <h2 style="font-size:17px;margin:0 0 14px">Nouveau message depuis le site</h2>
  <table style="border-collapse:collapse;font-size:14px;margin-bottom:18px">
    <tr><td style="padding:3px 14px 3px 0;color:#5B7280">Nom</td><td><b>${escapeHtml(name)}</b></td></tr>
    <tr><td style="padding:3px 14px 3px 0;color:#5B7280">E-mail</td><td><a href="mailto:${escapeHtml(email)}">${escapeHtml(email)}</a></td></tr>
    <tr><td style="padding:3px 14px 3px 0;color:#5B7280">Sujet</td><td>${escapeHtml(topic)}</td></tr>
    <tr><td style="padding:3px 14px 3px 0;color:#5B7280">Page</td><td>${lang === "ht" ? "kreyòl (/ht)" : "anglais (/)"}</td></tr>
    <tr><td style="padding:3px 14px 3px 0;color:#5B7280">Date</td><td>${when}</td></tr>
  </table>
  <div style="white-space:pre-wrap;border-left:3px solid #FFB703;padding:2px 0 2px 14px">${escapeHtml(message)}</div>
  <p style="font-size:12px;color:#5B7280;margin-top:22px">Répondre à ce message écrit directement à ${escapeHtml(name)}.</p>
</div>`;

  try {
    const r = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${process.env.RESEND_API_KEY}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        from: FROM,
        to: [TO],
        reply_to: email, // répondre à l'e-mail va au visiteur, pas à Resend
        subject: `[Ti kreyon espwa] ${topic} — ${name}`,
        text,
        html,
      }),
    });

    if (!r.ok) {
      const detail = await r.text();
      console.error("Resend a refusé l'envoi", r.status, detail);
      return res.status(502).json({ ok: false, error: "send_failed" });
    }
    return res.status(200).json({ ok: true });
  } catch (err) {
    console.error("Appel Resend impossible", err);
    return res.status(502).json({ ok: false, error: "send_failed" });
  }
};
