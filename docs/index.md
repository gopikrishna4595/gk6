---
layout: default
title: ⚡️ gk6 – k6’s Secret Weapon for Postman Collections
---

<div style="text-align:center; margin-bottom: 1rem;">
<svg viewBox="0 0 800 160" width="90%" height="160" xmlns="http://www.w3.org/2000/svg">
  <!-- Stars -->
  <circle class="star" cx="50" cy="20" r="3"/>
  <circle class="star" cx="300" cy="10" r="2"/>
  <circle class="star" cx="500" cy="30" r="2.5"/>
  <circle class="star" cx="150" cy="60" r="2"/>

  <!-- Sliding Text -->
  <text x="300" y="100" class="letter g burning">g</text>
  <text x="332" y="100" class="letter k6 burning">k6</text>
  <g class="generate-group">
    <text x="322" y="100" class="letter">e</text>
    <text x="346" y="100" class="letter">n</text>
    <text x="370" y="100" class="letter">e</text>
    <text x="394" y="100" class="letter">r</text>
    <text x="418" y="100" class="letter">a</text>
    <text x="442" y="100" class="letter">t</text>
    <text x="466" y="100" class="letter">e</text>
  </g>

  <!-- Firework Sparks (45) -->
  <g class="firework-group">
    {% for i in (0..14) %}
      {% assign baseX = 180 | plus: i | times: 10 %}
      <circle class="firework arc" cx="{{ baseX }}" cy="100" r="1.5"/>
    {% endfor %}
    {% for i in (0..14) %}
      {% assign baseX = 360 | plus: i | times: 10 %}
      <circle class="firework vertical" cx="{{ baseX }}" cy="100" r="1.5"/>
    {% endfor %}
    {% for i in (0..14) %}
      {% assign baseX = 540 | plus: i | times: 10 %}
      <circle class="firework arc" cx="{{ baseX }}" cy="100" r="1.5"/>
    {% endfor %}
  </g>

  <!-- Confetti (50) -->
  <g class="confetti-group">
    {% assign colors = "red,blue,green,yellow" | split: "," %}
    {% for i in (0..49) %}
      {% assign x = 260 | plus: i | times: 10 %}
      {% assign color = colors[i | modulo: 4] %}
      <rect class="confetti confetti-{{ color }}" x="{{ x | modulo: 800 }}" y="0" width="6" height="10"/>
    {% endfor %}
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
