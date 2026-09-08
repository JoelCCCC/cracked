TRACK = {
    "slug": "web",
    "name": "Web Development",
    "tagline": "How the modern web actually works: HTTP, DOM, APIs, rendering, and security.",
    "description": (
        "Start from absolute zero. Learn how the browser and server communicate over HTTP, "
        "how the DOM renders, how to design clean REST APIs, modern Next.js rendering strategies, and web security."
    ),
    "icon": "◍",
    "accent": "#ff7a45",
    "order": 3,
    "required_xp": 450,
    "levels": [
        # =========================================================================
        # LEVEL 1: HOW THE WEB WORKS & HTTP
        # =========================================================================
        {
            "index": 1,
            "title": "Web Foundations & The HTTP Protocol",
            "summary": "DNS resolution, TCP/TLS handshakes, HTTP request/response anatomy, and status codes.",
            "xp_reward": 85,
            "lessons": [
                {
                    "title": "How the Web Works: From URL to Screen",
                    "minutes": 6,
                    "body": """What actually happens in the 50 milliseconds after you enter a URL or click a link?

### 1. DNS Resolution (The Internet's Phonebook)
Computers communicate using numerical IP addresses (such as `142.250.190.46`), not friendly domain names.
Your computer first queries a **Domain Name System (DNS)** server:
`api.example.com` $\\rightarrow$ `93.184.216.34`.

### 2. The TCP & TLS Handshake
Before sending web traffic, your browser establishes a secure connection:
- **TCP 3-Way Handshake**: `SYN` (client asks to connect) $\\rightarrow$ `SYN-ACK` (server agrees) $\\rightarrow$ `ACK` (connection established).
- **TLS Handshake**: In `https://`, client and server exchange certificates and agree on a cryptographic session key so eavesdroppers cannot read passwords or credit card data.

### 3. The HTTP Request Anatomy
HTTP is a plaintext, stateless request/response protocol:

```http
POST /api/v1/orders HTTP/1.1
Host: api.example.com
User-Agent: Mozilla/5.0
Content-Type: application/json
Authorization: Bearer eyJhbGci...

{"item_id": 42, "quantity": 1}
```

Every request contains:
1. **Start Line**: Method (`POST`), Path (`/api/v1/orders`), Protocol (`HTTP/1.1`).
2. **Headers**: Key-value metadata (auth tokens, content formats).
3. **Blank Line**: Mandatory delimiter separating headers from body.
4. **Body**: The payload (JSON, form data, or binary).""",
                },
                {
                    "title": "HTTP Methods & Status Codes Used Correctly",
                    "minutes": 6,
                    "body": """HTTP defines clear semantic contracts for verbs and responses.

### HTTP Methods & Idempotency
An operation is **idempotent** if applying it multiple times produces the exact same server state as applying it once.

| Method | Safe | Idempotent | Purpose |
| :--- | :--- | :--- | :--- |
| **GET** | Yes | Yes | Retrieve a resource. Must NEVER mutate state. |
| **POST** | No | No | Create a new resource or execute an arbitrary action. |
| **PUT** | No | Yes | Replace the resource at the given URL completely. |
| **PATCH** | No | No | Partially update specific fields on a resource. |
| **DELETE** | No | Yes | Delete the resource at the given URL. |

> [!NOTE]
> Why does idempotency matter? If a user clicks "Submit Order" and the Wi-Fi blinks, a retried `POST` might charge them twice! That's why payment APIs require an *idempotency key*.

### The Status Code Families
- **2xx Success**: `200 OK`, `201 Created` (returns new URL in `Location`), `204 No Content`
- **3xx Redirection**: `301 Moved Permanently` (browser caches aggressively), `304 Not Modified`
- **4xx Client Error**:
  - `400 Bad Request`: Malformed syntax or JSON.
  - `401 Unauthorized`: **Who are you?** (Missing or invalid auth credentials).
  - `403 Forbidden`: **I know who you are, but you are not allowed.** (Authenticated, but insufficient permissions).
  - `404 Not Found`: Resource doesn't exist.
  - `429 Too Many Requests`: Rate limit hit.
- **5xx Server Error**: `500 Internal Error`, `502 Bad Gateway`, `504 Gateway Timeout`.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "401 vs 403 Distinction",
                    "prompt": "A logged-in user with a valid session attempts to view another user's private medical record. What HTTP status code should the API return?",
                    "hint": "Do we know who they are?",
                    "explanation": "The user is authenticated, but forbidden from accessing this specific record: 403 Forbidden. 401 would tell them to log in again.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "401 Unauthorized",
                            "403 Forbidden",
                            "400 Bad Request",
                            "500 Internal Server Error",
                        ]
                    },
                    "solution": {"answer": 1},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Idempotent HTTP Methods",
                    "prompt": "Which of the following HTTP requests can a client safely retry multiple times without creating duplicate items on the server?",
                    "hint": "Idempotent means f(f(x)) = f(x).",
                    "explanation": "GET only reads, PUT replaces the existing resource at a fixed path, and DELETE removes it. POST creates new entries and is not idempotent.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "GET /users/123",
                            "PUT /users/123 with a full profile payload",
                            "POST /orders creating a new checkout",
                            "DELETE /users/123",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Resource Created Status Code",
                    "prompt": "Which 3-digit HTTP status code signifies that a request succeeded and led to the creation of a new resource?",
                    "hint": "In the 2xx family.",
                    "explanation": "201 Created is returned when a new resource has been successfully created.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. 200"},
                    "solution": {"regex": True, "accept": [r"^201$"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Classify HTTP Status Code",
                    "prompt": "Write and export `classifyStatus(code)` returning:\n- `\"success\"` for 2xx codes (200-299)\n- `\"redirect\"` for 3xx codes (300-399)\n- `\"client-error\"` for 4xx codes (400-499)\n- `\"server-error\"` for 5xx codes (500-599)\n- `\"other\"` for any other integer\n\nExport it: `module.exports = { classifyStatus };`",
                    "hint": "Integer divide by 100 or use numeric comparisons.",
                    "explanation": "The status class is defined by the hundreds digit.",
                    "xp": 35,
                    "config": {
                        "language": "javascript",
                        "starter": "function classifyStatus(code) {\n  // your code here\n}\n\nmodule.exports = { classifyStatus };\n",
                    },
                    "solution": {
                        "entrypoint": "classifyStatus",
                        "cases": [
                            {"args": [200], "expect": "success"},
                            {"args": [204], "expect": "success"},
                            {"args": [301], "expect": "redirect"},
                            {"args": [404], "expect": "client-error"},
                            {"args": [500], "expect": "server-error"},
                            {"args": [100], "expect": "other"},
                            {"args": [418], "expect": "client-error", "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 2: HTML & THE DOCUMENT OBJECT MODEL (DOM)
        # =========================================================================
        {
            "index": 2,
            "title": "HTML & The Document Object Model (DOM)",
            "summary": "Semantic HTML, elements and attributes, the DOM tree, and manipulating pages with JavaScript.",
            "xp_reward": 90,
            "lessons": [
                {
                    "title": "HTML: The Skeleton of the Web",
                    "minutes": 6,
                    "body": """HTML (HyperText Markup Language) provides the structure and meaning of web content.

### Anatomy of an HTML Element
```html
<button class="primary-btn" id="submit-btn" disabled>Submit Order</button>
```
- `<button ...>`: Opening tag.
- `class` and `id`: **Attributes** providing metadata, styling hooks, and unique identifiers.
- `disabled`: A **boolean attribute** (its mere presence means true).
- `Submit Order`: The child text content.
- `</button>`: Closing tag.

### Why Semantic HTML Matters
Using semantic tags (`<header>`, `<nav>`, `<main>`, `<article>`, `<button>`) instead of generic `<div>` tags:
1. **Accessibility**: Screen readers can navigate landmarks easily.
2. **Built-in Behavior**: `<button>` is accessible via the keyboard (`Tab` + `Enter`), while `<div onclick="...">` requires tedious manual keyboard handling.
3. **SEO**: Search engine crawlers understand what content is primary.""",
                },
                {
                    "title": "The DOM Tree & JavaScript Interactivity",
                    "minutes": 6,
                    "body": """When the browser downloads HTML text, it parses it into an in-memory tree of objects called the **DOM (Document Object Model)**.

Every HTML tag becomes a DOM node:
```
Document
 └── <html>
      ├── <head>
      └── <body>
           ├── <header>
           └── <main>
                └── <button id="btn">Click me</button>
```

### Manipulating the DOM with JavaScript
```javascript
// 1. Find the element in the tree
const button = document.querySelector('#btn');

// 2. Modify its properties
button.textContent = 'Processing...';

// 3. Listen for user interactions
button.addEventListener('click', (event) => {
    console.log('Button clicked!');
});
```""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "The Document Object Model",
                    "prompt": "What does the browser construct in memory when it finishes parsing an HTML document?",
                    "hint": "Three-letter acronym representing an object tree.",
                    "explanation": "The browser constructs the DOM (Document Object Model), allowing JavaScript to inspect and modify elements.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "The DOM (Document Object Model)",
                            "The DNS cache",
                            "A SQL database",
                            "A WebAssembly binary",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "CSS ID Selector Prefix",
                    "prompt": "In CSS selectors and `document.querySelector`, what single character prefixes an ID attribute (e.g. for `<div id=\"app\">`)?",
                    "hint": "The hash symbol.",
                    "explanation": "The `#` symbol represents an ID selector, e.g. `#app`.",
                    "xp": 20,
                    "config": {"placeholder": "a symbol"},
                    "solution": {"regex": True, "accept": [r"^#$"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Standard DOM Events",
                    "prompt": "Which of the following are built-in browser DOM events that can be listened to with `addEventListener`?",
                    "hint": "Think about common mouse, keyboard, and form actions.",
                    "explanation": "`click`, `submit`, and `keydown` are standard DOM events. `compile` is not a DOM event.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "click",
                            "submit",
                            "keydown",
                            "compile",
                        ]
                    },
                    "solution": {"answers": [0, 1, 2]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Count HTML Tags",
                    "prompt": "Write and export `countTags(html, tag)` that counts how many times an opening tag `<tag` appears in an HTML string.\nCase-insensitive (`<p>` and `<P>` both count).\n\n```javascript\ncountTags('<p>Hello</p><p>World</p>', 'p') -> 2\ncountTags('<div><span></span></div>', 'span') -> 1\ncountTags('<h1>Title</h1>', 'div') -> 0\n```\n\nExport: `module.exports = { countTags };`",
                    "hint": "Convert to lower case and use regex or string splitting on `<${tag.toLowerCase()}`.",
                    "explanation": "Counting tag occurrences verifies element counts in markup templates.",
                    "xp": 35,
                    "config": {
                        "language": "javascript",
                        "starter": "function countTags(html, tag) {\n  // your code here\n}\n\nmodule.exports = { countTags };\n",
                    },
                    "solution": {
                        "entrypoint": "countTags",
                        "cases": [
                            {"args": ["<p>Hello</p><p>World</p>", "p"], "expect": 2},
                            {"args": ["<div><span></span></div>", "span"], "expect": 1},
                            {"args": ["<h1>Title</h1>", "div"], "expect": 0},
                            {"args": ["<P>Hi</P><p>There</p>", "p"], "expect": 2},
                            {"args": ["", "div"], "expect": 0, "hidden": True},
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 3: MODERN APIS: FETCH, JSON & REST
        # =========================================================================
        {
            "index": 3,
            "title": "Modern APIs: Fetch, JSON & REST",
            "summary": "Asynchronous JavaScript, Promises, async/await, JSON interchange, and REST API design.",
            "xp_reward": 100,
            "lessons": [
                {
                    "title": "Asynchronous JavaScript: Promises & Async/Await",
                    "minutes": 6,
                    "body": """JavaScript is single-threaded. If network requests blocked execution, your browser would completely freeze until the server responded!

### Promises and Async/Await
A **Promise** represents a value that will become available in the future (pending $\\rightarrow$ resolved or rejected).
The modern syntax is `async` / `await`:

```javascript
async function loadUserData(userId) {
    try {
        const response = await fetch(`https://api.example.com/users/${userId}`);
        if (!response.ok) {
            throw new Error(`HTTP Error: ${response.status}`);
        }
        const user = await response.json();
        return user;
    } catch (err) {
        console.error('Failed to load user:', err);
    }
}
```

### JSON (JavaScript Object Notation)
JSON is the universal language of web APIs:
- `JSON.stringify(object)`: Turns a JavaScript object into a JSON string payload.
- `JSON.parse(string)`: Parses a JSON string into a live JavaScript object.""",
                },
                {
                    "title": "REST API Design Principles",
                    "minutes": 6,
                    "body": """REST (Representational State Transfer) structures URLs around **resources (nouns)**, using HTTP methods for actions:

- `GET /api/v1/articles` $\\rightarrow$ List articles
- `POST /api/v1/articles` $\\rightarrow$ Create a new article
- `GET /api/v1/articles/42` $\\rightarrow$ Retrieve article #42
- `DELETE /api/v1/articles/42` $\\rightarrow$ Delete article #42

### Query Strings vs Path Parameters
- **Path parameters** (`/users/42`): Identify a specific unique resource.
- **Query strings** (`/users?role=admin&sort=desc`): Filter, sort, or paginate collections.""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "easy",
                    "title": "JSON Serialization",
                    "prompt": "Which built-in JavaScript method converts a live JavaScript object into a JSON string payload?",
                    "hint": "Methods on the global JSON object.",
                    "explanation": "JSON.stringify() serializes a JavaScript object into a JSON formatted string.",
                    "xp": 20,
                    "config": {
                        "options": [
                            "JSON.stringify()",
                            "JSON.parse()",
                            "Object.toJSON()",
                            "fetch.serialize()",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Parsing JSON",
                    "prompt": "What built-in JavaScript method parses a raw JSON string back into a JavaScript object or array?",
                    "hint": "JSON dot something.",
                    "explanation": "JSON.parse() converts a JSON string into JavaScript data.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. JSON.parse"},
                    "solution": {"regex": True, "accept": [r"JSON\.parse(\(\))?"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Good REST API Conventions",
                    "prompt": "Which of the following endpoint designs adhere to standard RESTful conventions?",
                    "hint": "Nouns for resources, HTTP verbs for operations.",
                    "explanation": "REST uses plural nouns for collections and verbs in the HTTP method, not `/deleteUser` in the URL.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "GET /api/products",
                            "POST /api/products",
                            "GET /api/deleteUser?id=42",
                            "DELETE /api/products/42",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Build a Deterministic Query String",
                    "prompt": "Write and export `toQuery(params)` that turns an object into a sorted URL query string.\n- Ignore `null`, `undefined`, and empty string `\"\"` values\n- Keys must be sorted alphabetically for deterministic cache keys\n- URL-encode keys and values\n- Return `\"\"` if empty\n\n```javascript\ntoQuery({ b: 2, a: 'x y', c: null }) -> \"a=x%20y&b=2\"\n```\n\nExport: `module.exports = { toQuery };`",
                    "hint": "Use Object.entries(), filter out null/undefined/empty, sort by key, and encode with encodeURIComponent.",
                    "explanation": "Sorting query string keys makes cache keys deterministic.",
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

        # =========================================================================
        # LEVEL 4: RENDERING STRATEGIES & NEXT.JS
        # =========================================================================
        {
            "index": 4,
            "title": "Rendering Strategies & Next.js",
            "summary": "CSR, SSR, SSG, ISR, React Server Components vs Client Components, and URL state discipline.",
            "xp_reward": 110,
            "lessons": [
                {
                    "title": "Where HTML is Born: CSR, SSR, SSG & ISR",
                    "minutes": 7,
                    "body": """Every modern web architecture answers one central question: **When and where does the HTML get generated?**

| Strategy | When Built | Best For | Trade-offs |
| :--- | :--- | :--- | :--- |
| **CSR** (Client-Side Rendering) | In the browser after downloading JS | Private dashboards behind login | Blank initial paint, poor SEO |
| **SSR** (Server-Side Rendering) | On the server for every single request | Personalised, real-time dynamic pages | Server compute cost on every hit |
| **SSG** (Static Site Generation) | Once at build time | Marketing pages, documentation, blogs | Requires rebuild to update |
| **ISR** (Incremental Static Revalidation) | At build time, revalidated in background | Huge product catalogues | Brief window of stale data |

In the Next.js App Router, these choices are made **per-route and per-component**, not per-app!""",
                },
                {
                    "title": "React Server Components vs Client Components",
                    "minutes": 6,
                    "body": """In Next.js:
- **Server Components (Default)**: Run exclusively on the server. They ship **0 KB of JavaScript** to the browser and can query databases directly without exposing credentials.
- **Client Components (`\"use client\"`)**: Opt-in components that run in both browser and server. Required whenever you use `useState`, `useEffect`, or DOM event handlers (`onClick`).

### State Discipline
Most frontend bugs stem from one mistake: **storing derived state**.
```javascript
// WRONG: Two sources of truth that will desynchronize
const [items, setItems] = useState([]);
const [count, setCount] = useState(0);

// RIGHT: Compute it directly
const count = items.length;
```""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Catalog Rendering Strategy",
                    "prompt": "An online store has 50,000 product pages. Prices change a few times a day. Fast loading and SEO are critical.\n\nWhich rendering strategy is best?",
                    "hint": "Full rebuilds take too long, but rendering on every request strains the server.",
                    "explanation": "ISR (Incremental Static Regeneration) serves cached static HTML instantly and revalidates in the background on an interval.",
                    "xp": 30,
                    "config": {
                        "options": [
                            "Pure Client-Side Rendering (CSR)",
                            "SSR on every request",
                            "Incremental Static Regeneration (ISR)",
                            "Manual rebuild on every price change",
                        ]
                    },
                    "solution": {"answer": 2},
                },
                {
                    "kind": "short",
                    "difficulty": "easy",
                    "title": "Next.js Client Directive",
                    "prompt": "What directive string must be placed at the very top of a file to declare a Client Component in the Next.js App Router?",
                    "hint": "Two words in quotes.",
                    "explanation": "\"use client\" marks the component and its imports for inclusion in the client JS bundle.",
                    "xp": 20,
                    "config": {"placeholder": "e.g. \"use client\""},
                    "solution": {"regex": True, "accept": [r"[\"'`]?use\s+client[\"'`]?;?"]},
                },
                {
                    "kind": "multi",
                    "difficulty": "medium",
                    "title": "Where State Belongs",
                    "prompt": "Which of the following pieces of state should be stored in the **URL query string** rather than local React component state?",
                    "hint": "Ask: should sharing or bookmarking the link preserve this state?",
                    "explanation": "Search filters, pagination, and active tabs should live in the URL so links and the browser back button work as expected.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "The active search filter and sort selection",
                            "The current page number in a list",
                            "Whether a dropdown menu is momentarily open",
                            "The selected tab on a settings page",
                        ]
                    },
                    "solution": {"answers": [0, 1, 3]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Derive Order Summary Stats",
                    "prompt": "Write and export `deriveStats(items)` that calculates summary statistics from an array of order items.\nEach item has `{ price: number, active: boolean }`.\n\nReturn an object:\n`{ totalCount: number, activeCount: number, totalPrice: number }`\n\n```javascript\nderiveStats([{ price: 10, active: true }, { price: 20, active: false }])\n// -> { totalCount: 2, activeCount: 1, totalPrice: 30 }\n```\n\nExport: `module.exports = { deriveStats };`",
                    "hint": "Use array reduce or loop through items.",
                    "explanation": "Deriving values directly prevents stale state bugs.",
                    "xp": 40,
                    "config": {
                        "language": "javascript",
                        "starter": "function deriveStats(items) {\n  // your code here\n}\n\nmodule.exports = { deriveStats };\n",
                    },
                    "solution": {
                        "entrypoint": "deriveStats",
                        "cases": [
                            {
                                "args": [[{"price": 10, "active": True}, {"price": 20, "active": False}]],
                                "expect": {"totalCount": 2, "activeCount": 1, "totalPrice": 30},
                            },
                            {
                                "args": [[]],
                                "expect": {"totalCount": 0, "activeCount": 0, "totalPrice": 0},
                            },
                            {
                                "args": [[{"price": 15.5, "active": True}]],
                                "expect": {"totalCount": 1, "activeCount": 1, "totalPrice": 15.5},
                            },
                            {
                                "args": [[{"price": 5, "active": True}, {"price": 5, "active": True}]],
                                "expect": {"totalCount": 2, "activeCount": 2, "totalPrice": 10},
                                "hidden": True,
                            },
                        ],
                    },
                },
            ],
        },

        # =========================================================================
        # LEVEL 5: WEB SECURITY & PERFORMANCE
        # =========================================================================
        {
            "index": 5,
            "title": "Web Security & Performance",
            "summary": "Core Web Vitals, XSS sanitization, CSRF mitigation, HttpOnly cookies, and caching headers.",
            "xp_reward": 120,
            "lessons": [
                {
                    "title": "The Core Web Vitals That Matter",
                    "minutes": 6,
                    "body": """Google measures real user experience using three **Core Web Vitals**:

- **LCP (Largest Contentful Paint)**: How fast the main content renders. Target: **< 2.5s**. Fix: Preload hero images, remove render-blocking JS.
- **INP (Interaction to Next Paint)**: How quickly the UI responds to user clicks/taps. Target: **< 200ms**. Fix: Break up long JavaScript tasks.
- **CLS (Cumulative Layout Shift)**: How much page elements jump around as resources load. Target: **< 0.1**. Fix: Always set explicit `width` and `height` attributes on images and videos.""",
                },
                {
                    "title": "XSS, CSRF & Safe Token Storage",
                    "minutes": 7,
                    "body": """### 1. Cross-Site Scripting (XSS)
Occurs when untrusted user input is rendered as HTML without escaping, letting an attacker run malicious JavaScript on your domain.
- **Defense**: Always escape special HTML entities (`&`, `<`, `>`, `\"`, `'`). Modern React escapes strings automatically unless you bypass it with `dangerouslySetInnerHTML`.

### 2. Cross-Site Request Forgery (CSRF)
An attacker tricks a victim's browser into submitting an unauthorized request to a site where they are logged in.
- **Defense**: Use `SameSite=Lax` or `Strict` cookies, and include an unpredictable CSRF token with state-changing requests.

### 3. Where Should Auth Tokens Live?
| Storage | XSS Vulnerability | Recommended? |
| :--- | :--- | :--- |
| `localStorage` | **High**: Any injected script can read and steal the token | No |
| `HttpOnly; Secure; SameSite=Lax` Cookie | **Immune**: JavaScript cannot read HttpOnly cookies | **Yes** |""",
                },
            ],
            "challenges": [
                {
                    "kind": "mcq",
                    "difficulty": "medium",
                    "title": "Layout Shift Prevention",
                    "prompt": "Images pop into the page late, causing the text to violently jump downward. What metric is suffering, and what fixes it?",
                    "hint": "CLS measures visual stability.",
                    "explanation": "This is CLS (Cumulative Layout Shift). Providing explicit width and height allows the browser to reserve the exact layout space before image bytes arrive.",
                    "xp": 25,
                    "config": {
                        "options": [
                            "CLS — specify width and height or aspect-ratio boxes",
                            "LCP — upgrade server CPU",
                            "INP — debounce the scroll listener",
                            "TTFB — install an SSL certificate",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "mcq",
                    "difficulty": "hard",
                    "title": "Token Storage Security",
                    "prompt": "A web app stores its session JWT in `localStorage`. A compromised third-party npm package executes arbitrary script on the page.\n\nWhat is the direct risk?",
                    "hint": "Can client-side JavaScript access localStorage?",
                    "explanation": "Any script running on the page can access localStorage and exfiltrate the token to an attacker server. HttpOnly cookies cannot be read by JavaScript.",
                    "xp": 35,
                    "config": {
                        "options": [
                            "The script can read the JWT and hijack the user session",
                            "Nothing, because JWTs are signed with a private key",
                            "Only images can be read",
                            "The browser automatically restricts localStorage access",
                        ]
                    },
                    "solution": {"answer": 0},
                },
                {
                    "kind": "short",
                    "difficulty": "medium",
                    "title": "Cache Header for Sensitive Data",
                    "prompt": "Which Cache-Control directive instructs browsers and intermediary proxies to NEVER store the response in any cache or disk storage?",
                    "hint": "Starts with 'no-'. Not 'no-cache'.",
                    "explanation": "Cache-Control: no-store instructs caches to never write the response to disk.",
                    "xp": 25,
                    "config": {"placeholder": "e.g. no-store"},
                    "solution": {"regex": True, "accept": [r"no-?\s?store", r"cache-control:\s*no-?\s?store"]},
                },
                {
                    "kind": "code",
                    "difficulty": "medium",
                    "title": "Escape HTML Entities (XSS Defense)",
                    "prompt": "Write and export `escapeHtml(s)` that replaces sensitive characters with HTML entities:\n- `&` $\\rightarrow$ `&amp;`\n- `<` $\\rightarrow$ `&lt;`\n- `>` $\\rightarrow$ `&gt;`\n- `\"` $\\rightarrow$ `&quot;`\n- `'` $\\rightarrow$ `&#39;`\n\n```javascript\nescapeHtml('<script>') -> \"&lt;script&gt;\"\nescapeHtml('a & b') -> \"a &amp; b\"\n```\n\nExport: `module.exports = { escapeHtml };`",
                    "hint": "Use a regex character class or replace `&` first before replacing other characters.",
                    "explanation": "Escaping special characters prevents browsers from executing user input as code.",
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
