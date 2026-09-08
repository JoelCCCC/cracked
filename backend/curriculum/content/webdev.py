TRACK = {
    "slug": "web",
    "name": "Web Development",
    "tagline": "HTTP, rendering strategies, and state that doesn't fight you.",
    "description": (
        "How the browser and the server actually talk, where to render, how to keep "
        "client state honest, and the performance and security basics every web engineer "
        "is expected to know cold."
    ),
    "icon": "◍",
    "accent": "#ff7a45",
    "order": 3,
    "required_xp": 900,
    "levels": [
        {
            "index": 1,
            "title": "HTTP and the request lifecycle",
            "summary": "Methods, status codes, caching headers, and why idempotency matters.",
            "xp_reward": 90,
            "lessons": [
                {
                    "title": "Status codes and methods, used correctly",
                    "minutes": 6,
                    "body": """The web is a contract. Break it and proxies, browsers and clients misbehave in ways you cannot patch.

**Methods**

| Method | Safe | Idempotent | Meaning |
| --- | --- | --- | --- |
| GET | yes | yes | read, cacheable, never mutate |
| POST | no | no | create / arbitrary action |
| PUT | no | yes | replace at a known URL |
| PATCH | no | no | partial update |
| DELETE | no | yes | remove |

*Idempotent* means the client can retry safely — the reason a flaky network is survivable at all. `POST /charge` retried twice charges twice; that's why payment APIs take an idempotency key.

**Status codes that matter**

- `200` ok · `201` created (send `Location`) · `204` no content
- `301` permanent (cached hard — be careful) · `302`/`307` temporary · `304` not modified
- `400` malformed · `401` not authenticated · `403` authenticated but not allowed · `404` missing · `409` conflict · `422` semantically invalid · `429` rate limited
- `500` you broke it · `502`/`503`/`504` upstream broke it

The 401 vs 403 distinction gets asked in interviews constantly: **401 = who are you, 403 = I know who you are and no**.""",
                },
                {
                    "title": "Caching without lying to users",
                    "minutes": 6,
                    "body": """Two independent questions: *may this be reused* and *is my copy still fresh*.

```
Cache-Control: public, max-age=31536000, immutable   # hashed asset
Cache-Control: private, no-cache                     # HTML: revalidate every time
Cache-Control: no-store                              # never touch this (auth pages)
ETag: "a1b2c3"                                       # cheap revalidation -> 304
```

The pattern that makes fast sites:

1. **Fingerprint** static assets (`app.4f2c.js`) and cache them for a year, `immutable`.
2. Serve **HTML with `no-cache`** so a deploy is visible immediately.
3. Let the HTML point at the new fingerprints. Nothing is ever stale, nothing is re-downloaded.

`no-cache` does **not** mean "don't cache" — it means "cache it, but revalidate before use". The one that means don't store is `no-store`. Getting these backwards is how private data ends up in a CDN.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "401 or 403",
                    "prompt": "A logged-in user with a valid session requests another user's invoice. What status should the API return?",
                    "hint": "Do we know who they are?",
                    "explanation": "They are authenticated, just not authorised: 403. Returning 401 would tell the client to re-authenticate, which will not help. (404 is a defensible alternative when you don't want to confirm the resource exists.)",
                    "xp": 20,
                    "config": {"options": ["401 Unauthorized", "403 Forbidden", "400 Bad Request", "500 Internal Server Error"]},
                    "solution": {"answer": 1},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Which are idempotent",
                    "prompt": "Which of these requests can a client safely retry after a network timeout, without risking a duplicate side effect?",
                    "hint": "Idempotent = same result whether applied once or five times.",
                    "explanation": "GET is safe, PUT replaces the same resource, DELETE leaves it deleted. POST creating a new order is the one that duplicates — hence idempotency keys on payment APIs.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "GET /orders/42",
                            "PUT /orders/42 with the full body",
                            "POST /orders creating a new order",
                            "DELETE /orders/42",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "Cache header for private HTML",
                    "prompt": "Which `Cache-Control` directive tells caches to never write the response to disk at all — the one you want on a page showing someone's bank balance?",
                    "hint": "It is not `no-cache`.",
                    "explanation": "`no-store` forbids storing the response anywhere. `no-cache` still stores it and merely revalidates before reuse.",
                    "xp": 25,
                    "config": {"placeholder": "a Cache-Control directive"},
                    "solution": {"regex": True, "accept": [r"no-?\s?store", r"cache-control:\s*no-?\s?store"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Classify a status code",
                    "prompt": "Write and export `classify(code)` returning one of `\"success\"`, `\"redirect\"`, `\"client-error\"`, `\"server-error\"`, or `\"other\"` for any integer status code.\n\n2xx success · 3xx redirect · 4xx client-error · 5xx server-error · anything else other.\n\nExport it: `module.exports = { classify };`",
                    "hint": "Integer-divide by 100 and switch on the result.",
                    "explanation": "The status class is the first digit — which is exactly why the ranges are defined that way: an intermediary that doesn't know code 418 still knows it's a client error.",
                    "xp": 35,
                    "config": {
                        "language": "javascript",
                        "starter": "function classify(code) {\n  // your code here\n}\n\nmodule.exports = { classify };\n",
                    },
                    "solution": {
                        "entrypoint": "classify",
                        "cases": [
                            {"args": [200], "expect": "success"},
                            {"args": [204], "expect": "success"},
                            {"args": [301], "expect": "redirect"},
                            {"args": [404], "expect": "client-error"},
                            {"args": [503], "expect": "server-error"},
                            {"args": [100], "expect": "other"},
                            {"args": [0], "expect": "other", "hidden": True},
                        ],
                    },
                },
            ],
        },
        {
            "index": 2,
            "title": "Rendering strategies",
            "summary": "CSR, SSR, SSG, ISR, streaming — and which one your page actually needs.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "Where the HTML comes from",
                    "minutes": 7,
                    "body": """Every strategy answers one question: *when does the HTML get built?*

| Strategy | Built | Best for | Cost |
| --- | --- | --- | --- |
| **CSR** | in the browser after JS loads | app dashboards behind login | blank first paint, bad SEO |
| **SSR** | per request on the server | personalised, always-fresh pages | server time on every hit |
| **SSG** | at build time | marketing, docs, blogs | rebuild to change |
| **ISR** | at build, refreshed in the background | big catalogues that change slowly | slightly stale window |
| **Streaming SSR** | per request, sent in chunks | pages with one slow section | more complex |

In the Next.js App Router these are per-route (and per-component) choices, not per-app:

```tsx
// server component: runs on the server, no JS shipped for it
export default async function Page() {
  const data = await getData();       // no useEffect, no loading flash
  return <Chart data={data} />;
}

export const revalidate = 60;         // ISR: rebuild at most once a minute
```

**Default to server components.** Add `"use client"` only where you need state, effects, or event handlers — every client component is JavaScript the user has to download.""",
                },
                {
                    "title": "Client state that stays honest",
                    "minutes": 6,
                    "body": """Most React bugs are one mistake: **storing derived data in state**.

```tsx
// wrong: two sources of truth, guaranteed to drift
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);

// right: derive it
const count = items.length;
```

Sort state into three buckets:

- **Server state** — anything the API owns. It needs caching, revalidation and staleness handling. Use a data library (React Query, SWR, or the framework's own fetching). Do not hand-roll it in `useEffect`.
- **URL state** — filters, tabs, pagination, the open item. Put it in the query string so links and the back button work.
- **UI state** — is this dropdown open. `useState`, as local as possible.

`useEffect` is for **synchronising with something outside React** (a subscription, a DOM measurement, a timer). Fetching in an effect on mount is the pattern that gives you race conditions, double-fetches in StrictMode, and loading flashes.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Pick the rendering strategy",
                    "prompt": "A 40,000-page product catalogue. Prices change a few times a day. SEO is critical and traffic is heavy.\n\nWhat fits best?",
                    "hint": "Full rebuilds are too slow; per-request rendering is wasteful at this traffic.",
                    "explanation": "ISR serves cached HTML (fast, indexable) and refreshes pages in the background on an interval, so you neither rebuild 40k pages nor render on every request.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "Pure client-side rendering",
                            "SSR on every request",
                            "Static generation with incremental revalidation (ISR)",
                            "Static generation, rebuilding the whole site on each price change",
                        ]
                    },
                    "solution": {"answer": 2},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Where does this state live?",
                    "prompt": "Which of these belong in the **URL** rather than in React state?",
                    "hint": "Ask: should a copy-pasted link reproduce this?",
                    "explanation": "Anything a user would expect to survive a refresh, a share, or the back button belongs in the URL. Transient UI (a hover, an open dropdown) does not.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "The active filter set on a search page",
                            "The current page number",
                            "Whether a tooltip is currently hovered",
                            "The selected tab on a settings page",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Opt into the client",
                    "prompt": "Which directive do you put at the top of a Next.js App Router file to make it a client component?",
                    "hint": "It is a string literal on the first line.",
                    "explanation": "`\"use client\"` marks the module — and everything it imports — as part of the client bundle. Keep it as deep in the tree as possible.",
                    "xp": 20,
                    "config": {"placeholder": "the directive"},
                    "solution": {"regex": True, "accept": [r"[\"'`]?use\s+client[\"'`]?;?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Build a query string",
                    "prompt": "Write and export `toQuery(params)` that turns an object into a query string, sorted by key for stable cache keys.\n\n- skip `null`, `undefined` and `\"\"` values\n- URL-encode keys and values\n- return `\"\"` for an empty result (no leading `?`)\n\n```\ntoQuery({ b: 2, a: 'x y', c: null }) -> \"a=x%20y&b=2\"\n```\n\nExport with `module.exports = { toQuery };`",
                    "hint": "`Object.entries`, `filter`, `sort`, then `encodeURIComponent` both halves.",
                    "explanation": "Sorting keys makes the string deterministic, which matters the moment you use it as a cache key or in a snapshot test. Note `encodeURIComponent` encodes a space as `%20`.",
                    "xp": 45,
                    "config": {
                        "language": "javascript",
                        "starter": "function toQuery(params) {\n  // your code here\n}\n\nmodule.exports = { toQuery };\n",
                    },
                    "solution": {
                        "entrypoint": "toQuery",
                        "cases": [
                            {"args": [{"b": 2, "a": "x y", "c": None}], "expect": "a=x%20y&b=2"},
                            {"args": [{}], "expect": ""},
                            {"args": [{"q": ""}], "expect": ""},
                            {"args": [{"tag": "a&b"}], "expect": "tag=a%26b"},
                            {"args": [{"z": 1, "a": 1}], "expect": "a=1&z=1", "hidden": True},
                        ],
                    },
                },
            ],
        },
        {
            "index": 3,
            "title": "Performance and security basics",
            "summary": "Core Web Vitals, bundle discipline, and the OWASP hits you must know.",
            "xp_reward": 110,
            "lessons": [
                {
                    "title": "The three numbers users feel",
                    "minutes": 6,
                    "body": """Core Web Vitals are proxies for "does this site feel broken":

- **LCP** (Largest Contentful Paint) — when the main thing appears. Target **< 2.5s**. Usually fixed by preloading the hero image, sizing it properly, and not blocking on render-blocking CSS/JS.
- **INP** (Interaction to Next Paint) — how long the UI takes to respond to a tap. Target **< 200ms**. Long main-thread tasks are the cause; break them up or move them off the thread.
- **CLS** (Cumulative Layout Shift) — how much content jumps. Target **< 0.1**. Caused by images without `width`/`height`, injected banners, and late-loading fonts.

Cheap wins, in order of payoff:

1. Ship less JavaScript. Nothing else comes close.
2. Serve modern image formats at the size actually displayed.
3. `font-display: swap` plus a preloaded font file.
4. Reserve space for anything that loads late.""",
                },
                {
                    "title": "XSS, CSRF, and where tokens live",
                    "minutes": 7,
                    "body": """**XSS** — attacker JavaScript runs on your origin. It happens when untrusted input reaches the page as markup. The fix is to escape on output (React does this by default) and to never reach for `dangerouslySetInnerHTML` without sanitising. A strict `Content-Security-Policy` is the seatbelt.

**CSRF** — the victim's browser is tricked into sending an authenticated request. It only works because cookies are attached automatically. Fixes: `SameSite=Lax` (or `Strict`) cookies plus a CSRF token on state-changing requests.

**SQL injection** — string-concatenated queries. Parameterise, always. Django's ORM does this for you; `raw()` with an f-string does not.

Where should the session token live?

| Storage | XSS exposure | CSRF exposure |
| --- | --- | --- |
| `localStorage` | **readable by any injected script** | none |
| `HttpOnly` cookie | not readable by JS | needs SameSite + token |

The consensus for browser apps: **`HttpOnly; Secure; SameSite=Lax` cookies**. CSRF has a complete, well-understood mitigation; XSS token theft does not.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Layout shift",
                    "prompt": "Images pop in and push the article text down as the page loads. Which metric is bad, and what is the standard fix?",
                    "hint": "Content is moving after paint.",
                    "explanation": "That is CLS. Giving every image explicit `width`/`height` (or an aspect-ratio box) lets the browser reserve the space before the bytes arrive.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "LCP — preload the images",
                            "CLS — set explicit width/height or aspect-ratio",
                            "INP — debounce the scroll handler",
                            "TTFB — move to a CDN",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "mcq",
                    "difficulty": "hard",
                    "title": "Token storage",
                    "prompt": "Your SPA stores its session JWT in `localStorage`. A dependency ships a compromised version that injects a script.\n\nWhat is the direct consequence?",
                    "hint": "What can any script on the origin read?",
                    "explanation": "Any script on the origin can read `localStorage`, so the token is exfiltrated and the session is fully hijacked. An `HttpOnly` cookie is not readable by JavaScript at all.",
                    "xp": 35,
                    "config": {
                        "options": [
                            "Nothing — JWTs are signed, so they cannot be misused",
                            "The script can read the token and impersonate the user",
                            "Only a CSRF attack becomes possible",
                            "The browser blocks cross-origin token reads automatically",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "Stop the cross-site cookie",
                    "prompt": "Which cookie attribute stops the browser from attaching your session cookie to requests initiated by another site — the main structural defence against CSRF?",
                    "hint": "Two words jammed together, with a value like Lax or Strict.",
                    "explanation": "`SameSite` (Lax by default in modern browsers, Strict for the sensitive cases) prevents the cookie from riding along on cross-site requests.",
                    "xp": 25,
                    "config": {"placeholder": "a cookie attribute"},
                    "solution": {"regex": True, "accept": [r"same\s*-?\s*site(\s*=\s*(lax|strict))?"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Escape before you render",
                    "prompt": "Write and export `escapeHtml(s)` that replaces `&`, `<`, `>`, `\"` and `'` with their HTML entities: `&amp;` `&lt;` `&gt;` `&quot;` `&#39;`.\n\nOrder matters — escape `&` first or you double-escape.\n\nExport with `module.exports = { escapeHtml };`",
                    "hint": "One `replace` with a character-class regex and a lookup map handles ordering for you.",
                    "explanation": "This is what a template engine does on every interpolation. Escaping `&` last would turn `&lt;` into `&amp;lt;` — hence the single-pass map.",
                    "xp": 40,
                    "config": {
                        "language": "javascript",
                        "starter": "function escapeHtml(s) {\n  // your code here\n}\n\nmodule.exports = { escapeHtml };\n",
                    },
                    "solution": {
                        "entrypoint": "escapeHtml",
                        "cases": [
                            {"args": ["<script>"], "expect": "&lt;script&gt;"},
                            {"args": ["a & b"], "expect": "a &amp; b"},
                            {"args": ["say \"hi\""], "expect": "say &quot;hi&quot;"},
                            {"args": ["it's"], "expect": "it&#39;s"},
                            {"args": [""], "expect": ""},
                            {"args": ["&<>"], "expect": "&amp;&lt;&gt;", "hidden": True},
                        ],
                    },
                },
            ],
        },
    ],
}
