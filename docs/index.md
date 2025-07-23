---
layout: default
title: ⚡️ gk6 – k6’s Secret Weapon for Postman Collections
---

<link rel="stylesheet" href="./assets/css/fireworks.css" />

<svg viewBox="0 0 800 120" width="100%" height="120" xmlns="http://www.w3.org/2000/svg">
  <!-- Background -->
  <rect width="100%" height="120" fill="transparent" />

  <!-- Stars twinkle -->
  <circle class="star" cx="50" cy="20" r="3"/>
  <circle class="star" cx="300" cy="10" r="2"/>
  <circle class="star" cx="500" cy="30" r="2.5"/>
  <circle class="star" cx="150" cy="60" r="2"/>

  <!-- Fireworks -->
  <g class="fireworks">
    <circle class="firework" cx="400" cy="40" r="2" />
    <circle class="firework" cx="380" cy="80" r="2" />
    <circle class="firework" cx="420" cy="90" r="2" />
    <circle class="firework" cx="410" cy="50" r="2" />
    <circle class="firework" cx="430" cy="60" r="2" />
  </g>

  <!-- g and k6 burning -->
  <text x="300" y="60" class="letter g burning">g</text>
  <text x="332" y="60" class="letter k6 burning">k6</text>

  <!-- Reveal en- e-r-a-t-e -->
  <g class="generate-group">
    <text x="322" y="60" class="letter">e</text>
    <text x="346" y="60" class="letter">n</text>
    <text x="370" y="60" class="letter">e</text>
    <text x="394" y="60" class="letter">r</text>
    <text x="418" y="60" class="letter">a</text>
    <text x="442" y="60" class="letter">t</text>
    <text x="466" y="60" class="letter">e</text>
  </g>
</svg>

---

🧠 **Convert Postman collections into powerful [k6](https://k6.io) load test scripts — automatically.**  
No rewrites. No duct tape. Just pure Python + performance clarity.

[⭐ View on GitHub](https://github.com/gopikrishna4595/gk6)

---

## 🔥 What Does gk6 Actually Do?

**gk6** reads your Postman collection and:

- 🧪 Detects `pm.environment.set()` like a bloodhound on Red Bull  
- 🔗 Follows variable chaining across tests and folders  
- 🧬 Converts `{{envVars}}` to `__ENV.` or chained values for k6  
- 📊 Adds `Trend` metrics + response checks for every request  
- ⚙️ Outputs clean, executable `.js` files and optional `.env` config

---

## ⚠️ Known Limitations

- ❌ No support (yet) for GraphQL requests
- 🧱 Doesn't currently handle `pm.globals.set()`
- 🧪 Assumes all requests are RESTful and JSON-friendly
- 🔗 Variable chaining that spans *multiple levels* may not fully resolve
- 👻 If your Postman script is a spaghetti monster — it’ll still be spaghetti in k6

---

## 🚀 Quick Usage

```bash
python gk6.py \
  --collection my_collection.json \
  --environment my_env.json \
  --select 1,2,3 \
  --output test_script.js

k6 run test_script.js ```

---


Got questions or feedback? Raise an issue — or better yet, a PR 😎
