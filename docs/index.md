---
layout: default
title: ⚡️ gk6 – k6’s Secret Weapon for Postman Collections
---
<div style="text-align:center; margin-bottom: 1rem;">
<svg viewBox="0 0 800 120" width="90%" height="120" xmlns="http://www.w3.org/2000/svg">
  <!-- Stars -->
  <circle class="star" cx="50" cy="20" r="3"/>
  <circle class="star" cx="300" cy="10" r="2"/>
  <circle class="star" cx="500" cy="30" r="2.5"/>
  <circle class="star" cx="150" cy="60" r="2"/>

  <!-- Sliding Text: g → generate → k6 -->
  <text x="300" y="60" class="letter g burning">g</text>
  <text x="332" y="60" class="letter k6 burning">k6</text>
  <g class="generate-group">
    <text x="322" y="60" class="letter">e</text>
    <text x="346" y="60" class="letter">n</text>
    <text x="370" y="60" class="letter">e</text>
    <text x="394" y="60" class="letter">r</text>
    <text x="418" y="60" class="letter">a</text>
    <text x="442" y="60" class="letter">t</text>
    <text x="466" y="60" class="letter">e</text>
    <text x="490" y="60" class="letter"> </text>
  </g>

  <!-- Firework sparks (exactly 45 total) -->
<g class="firework-group">
  <!-- 5 clusters on the left -->
  <circle class="firework red vertical" cx="120" cy="60" r="2"/>
  <circle class="firework blue arc"     cx="130" cy="60" r="2"/>
  <circle class="firework green arc"    cx="140" cy="60" r="2"/>

  <circle class="firework red vertical" cx="150" cy="60" r="2"/>
  <circle class="firework blue arc"     cx="160" cy="60" r="2"/>
  <circle class="firework green arc"    cx="170" cy="60" r="2"/>

  <circle class="firework red vertical" cx="180" cy="60" r="2"/>
  <circle class="firework blue arc"     cx="190" cy="60" r="2"/>
  <circle class="firework green arc"    cx="200" cy="60" r="2"/>

  <circle class="firework red vertical" cx="210" cy="60" r="2"/>
  <circle class="firework blue arc"     cx="220" cy="60" r="2"/>
  <circle class="firework green arc"    cx="230" cy="60" r="2"/>

  <circle class="firework red vertical" cx="240" cy="60" r="2"/>
  <circle class="firework blue arc"     cx="250" cy="60" r="2"/>
  <circle class="firework green arc"    cx="260" cy="60" r="2"/>

  <!-- 5 clusters in the center -->
  <circle class="firework yellow vertical" cx="330" cy="60" r="2"/>
  <circle class="firework green arc"       cx="340" cy="60" r="2"/>
  <circle class="firework red arc"         cx="350" cy="60" r="2"/>

  <circle class="firework yellow vertical" cx="360" cy="60" r="2"/>
  <circle class="firework green arc"       cx="370" cy="60" r="2"/>
  <circle class="firework red arc"         cx="380" cy="60" r="2"/>

  <circle class="firework yellow vertical" cx="390" cy="60" r="2"/>
  <circle class="firework green arc"       cx="400" cy="60" r="2"/>
  <circle class="firework red arc"         cx="410" cy="60" r="2"/>

  <circle class="firework yellow vertical" cx="420" cy="60" r="2"/>
  <circle class="firework green arc"       cx="430" cy="60" r="2"/>
  <circle class="firework red arc"         cx="440" cy="60" r="2"/>

  <circle class="firework yellow vertical" cx="450" cy="60" r="2"/>
  <circle class="firework green arc"       cx="460" cy="60" r="2"/>
  <circle class="firework red arc"         cx="470" cy="60" r="2"/>

  <!-- 5 clusters on the right -->
  <circle class="firework blue vertical" cx="540" cy="60" r="2"/>
  <circle class="firework yellow arc"    cx="550" cy="60" r="2"/>
  <circle class="firework green arc"     cx="560" cy="60" r="2"/>

  <circle class="firework blue vertical" cx="570" cy="60" r="2"/>
  <circle class="firework yellow arc"    cx="580" cy="60" r="2"/>
  <circle class="firework green arc"     cx="590" cy="60" r="2"/>

  <circle class="firework blue vertical" cx="600" cy="60" r="2"/>
  <circle class="firework yellow arc"    cx="610" cy="60" r="2"/>
  <circle class="firework green arc"     cx="620" cy="60" r="2"/>

  <circle class="firework blue vertical" cx="630" cy="60" r="2"/>
  <circle class="firework yellow arc"    cx="640" cy="60" r="2"/>
  <circle class="firework green arc"     cx="650" cy="60" r="2"/>

  <circle class="firework blue vertical" cx="660" cy="60" r="2"/>
  <circle class="firework yellow arc"    cx="670" cy="60" r="2"/>
  <circle class="firework green arc"     cx="680" cy="60" r="2"/>
</g>

</svg>
</div>

---

🧠 **Convert Postman collections into powerful [k6](https://k6.io) load test scripts — automatically.**  
No rewrites. No duct tape. Just pure Python + performance clarity.

[⭐ View on GitHub](https://github.com/gopikrishna4595/gk6)

---

## 🚀 What Does gk6 Actually Do?

**gk6** reads your Postman collection and:

- 🌪️ Detects `pm.environment.set()` like a bloodhound on Red Bull  
- 🔗 Follows variable chaining across tests and folders  
- 🧬 Converts `{{envVars}}` to `__ENV.` or chained values for k6  
- 📊 Adds `Trend` metrics + response checks for every request  
- ⚙️ Outputs clean, executable `.js` files and optional `.env` config

---

## ⚠️ Known Limitations

- ❌ No support (yet) for GraphQL requests
- 🧱 Doesn't currently handle `pm.globals.set()`
- 🌪️ Assumes all requests are RESTful and JSON-friendly
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

k6 run test_script.js
```

---

Got questions or feedback? Raise an issue — or better yet, a PR 😎
