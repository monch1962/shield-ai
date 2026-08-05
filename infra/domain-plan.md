# SHIELD-AI — Domain & DNS Deployment Plan

**Status:** Ready to execute (domains not yet registered)
**Scope:** `shield-ai.ai` (brand front), `shield-ai.dev` (technical alias)
**Decision excluded by trademark review:** `shield-ai.consulting` — skip (see §7)

---

## 1. Architecture

```
                        ┌─────────────────────────────┐
                        │   Cloudflare Pages project   │
                        │   "shield-ai-site" (static)  │
                        │   *.pages.dev origin         │
                        └──────────────┬──────────────┘
               custom domains on same project
        ┌──────────────────┴───────────────────┐
        │                                      │
   shield-ai.ai  ── canonical, serves content  │
   www.shield-ai.ai ── 301 → apex              │
        │                                      │
        └──────────────────────────────────────┘
   shield-ai.dev  ── 301 → https://shield-ai.ai/
   www.shield-ai.dev ── 301 → https://shield-ai.ai/
```

**Canonical domain: `https://shield-ai.ai/`** — single SEO footprint, brand front.
**`shield-ai.dev`** is a 301 alias: cheap, HSTS-preloaded by registry mandate (Google's
`.dev` TLD is on the browser HSTS preload list), keeps the brand off squatters, and
gives a technical-looking alternative URL that always resolves to the same site.

> **Decision point (default: redirect).** If you prefer `.dev` as a *full content
> mirror* instead of a redirect, serve the same build on both and add
> `<link rel="canonical" href="https://shield-ai.ai/...">` on every page. Benefit:
> redundancy. Cost: duplicate-content management. For a solo practice, the 301 is
> simpler and avoids any duplicate-content question.

---

## 2. DNS records

DNS for both zones at Cloudflare (proxied/orange-cloud), after adding each domain
as a custom domain on the Pages project. Pages will ask for a verification CNAME
(`_cloudflare-pages-<hash>` → `<hash>.pages.dev`) — add it, then it can be removed.

### Zone: `shield-ai.ai`

| Type | Name | Value | Proxy | Purpose |
|------|------|-------|-------|---------|
| CNAME | `@` | `shield-ai-site.pages.dev` | ✅ | Apex → site (CF flattens apex CNAME) |
| CNAME | `www` | `shield-ai-site.pages.dev` | ✅ | www → same project (301 rule below) |
| MX | `@` | `0 .` | — | Null MX (RFC 7505): no email accepted |
| TXT | `@` | `v=spf1 -all` | — | Declare: domain sends no mail |
| TXT | `_dmarc` | `v=DMARC1; p=reject; adkim=s; aspf=s;` | — | Hard-fail spoofed mail |
| TXT | `_cloudflare-pages-<hash>` | `<hash>.pages.dev` | — | Pages verification (temp) |

### Zone: `shield-ai.dev`

| Type | Name | Value | Proxy | Purpose |
|------|------|-------|-------|---------|
| CNAME | `@` | `shield-ai-site.pages.dev` | ✅ | Apex → site (301 rule below) |
| CNAME | `www` | `shield-ai-site.pages.dev` | ✅ | www → same project |
| MX | `@` | `0 .` | — | Null MX |
| TXT | `@` | `v=spf1 -all` | — | No senders |
| TXT | `_dmarc` | `v=DMARC1; p=reject; adkim=s; aspf=s;` | — | Hard-fail |
| TXT | `_cloudflare-pages-<hash>` | `<hash>.pages.dev` | — | Pages verification (temp) |

> The null MX + SPF `-all` + DMARC `p=reject` trio is the hardened "this domain
> does not send email" posture — nobody can spoof mail from your domain, and you
> don't need to run an inbox. If you ever want `david@shield-ai.ai`, add a real MX
> + SPF include instead.

---

## 3. Redirect rules

Cloudflare **Bulk Redirects** (or Pages Redirect Rules). Source = wildcard path
preservation unless noted.

| From | To | Status | Match |
|------|----|--------|-------|
| `http://shield-ai.ai/*` | `https://shield-ai.ai/$1` | 301 | Scheme only (Pages does this automatically) |
| `https://www.shield-ai.ai/*` | `https://shield-ai.ai/$1` | 301 | Hostname |
| `https://shield-ai.dev/*` | `https://shield-ai.ai/$1` | 301 | Whole domain |
| `https://www.shield-ai.dev/*` | `https://shield-ai.ai/$1` | 301 | Whole domain |
| `/docs/framework/` | `/docs/framework/` (canonical) | — | Ensure trailing-slash normalization at build time |

Rationale for 301 (permanent): search engines consolidate the alias onto the
canonical domain; HSTS applies at the destination regardless.

---

## 4. Security hardening

- **TLS:** automatic via Cloudflare edge certs (full strict). `.dev` is HTTPS-only
  by registry preload; `.ai` needs the header (below).
- **HSTS (`.ai` only):** Cloudflare → SSL/TLS → Edge Certificates → **HSTS: On**,
  `max-age=31536000`, include subdomains, **preload on**. After a week of live
  HSTS, submit `https://shield-ai.ai` to https://hstspreload.org.
- **`/.well-known/security.txt`** — a security consultancy should have one:
  `Contact: <your-email-or-contact-url>`, `Expires: <date>`, `Preferred-Languages: en`.
- **Security headers** on every page (Pages `_headers` file):
  ```
  /*
    X-Content-Type-Options: nosniff
    X-Frame-Options: DENY
    Referrer-Policy: strict-origin-when-cross-origin
    Permissions-Policy: geolocation=(), microphone=(), camera=()
    Content-Security-Policy: default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; frame-ancestors 'none'
  ```
  (Reveal.js decks may need `script-src 'self' 'unsafe-inline'` for inline handlers —
  verify with the decks in `presentations/`.)
- **Robots:** allow all except `/assets/` internals unless you want diagrams indexable.

---

## 5. Content → URL layout

Map of existing repo content to site paths:

| Repo path | Site URL | Notes |
|-----------|----------|-------|
| (landing page) | `https://shield-ai.ai/` | Overview + links to docs |
| `framework/*.md` + generated `.html` | `/docs/framework/` | Framework, gap analysis, deep review, implementation architecture — each with PDF/EPUB download |
| `framework/shield-ai-watchlist.md` | `/docs/watchlist/` | |
| `assessment-guide/` | `/docs/assessment-guide/` | |
| `presentations/` (Reveal.js) | `/presentations/business/`, `/technical/`, `/buyers-journey/` | Self-contained HTML |
| `policies/` (36 Rego stubs) | `/docs/policies/` or link to GitHub | Regenerate rendered view from schema |
| `assets/` | `/assets/` | Diagrams, control schema JSON, logos (docs reference these) |
| — | `/.well-known/security.txt` | §4 |

Build: reuse `tools/build_docs.sh` (pandoc → HTML) and assemble a static tree.
Add a GitHub Actions workflow on `main` that builds and deploys to the Pages
project (`wrangler pages deploy` with a `CLOUDFLARE_API_TOKEN` secret). No CI
exists in this repo yet — first workflow.

---

## 6. Post-registration verification checklist

```bash
curl -sI  https://shield-ai.ai/                      # expect 200
curl -sI  http://shield-ai.ai/                       # expect 301 → https
curl -sI  https://www.shield-ai.ai/                  # expect 301 → apex
curl -sI  https://shield-ai.dev/                     # expect 301 → https://shield-ai.ai/
curl -sI  https://shield-ai.ai/docs/framework/       # expect 200
dig +short MX shield-ai.ai                           # expect "0 ."
dig +short TXT _dmarc.shield-ai.ai                   # expect DMARC p=reject
curl -sI https://shield-ai.ai/ | grep -i strict-transport-security   # expect HSTS header
curl -s  https://shield-ai.ai/.well-known/security.txt              # expect 200
```

---

## 7. Why `shield-ai.consulting` is excluded

- The `.consulting` TLD signals paid consulting services — the exact commercial
  activity Shield AI Inc.'s pending AU mark 2601389 covers in class 42
  ("software development consulting in the field of AI … security").
- Highest UDRP bad-faith exposure of the three candidates, zero upside over `.ai`.
- If a practice-facing landing page is ever needed, a `/consulting` path or a
  distinct future brand domain covers it.

## 8. UDRP posture notes (apply at launch)

- **Publish real content on `shield-ai.ai` immediately** — no parking, no bare
  placeholder. A landing page + docs satisfies "active use" and defeats
  passive-holding bad-faith claims.
- **Preserve prior-use evidence:** the repo's git history (first commits of the
  framework docs) is your record. Snapshot `README.md` + framework docs at launch
  (archive.org + a dated PDF in repo) with timestamps.
- Never offer to sell/transfer the domain in any communication.
