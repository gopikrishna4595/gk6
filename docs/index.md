---
layout: default
title: ⚡️ gk6 – k6’s Secret Weapon for Postman Collections
---
<div style="text-align:center; margin-bottom: 1rem;">
<svg viewBox="0 0 800 120" width="90%" height="120" xmlns="http://www.w3.org/2000/svg">
  <style>
    .letter {
      font: bold 48px 'Fira Code', monospace;
      fill: #000;
      dominant-baseline: middle;
    }
    .burning {
      animation: burnEffect 10s ease-in-out infinite;
      transform-origin: center;
    }
    .g {
      animation: moveG 10s ease-in-out infinite;
    }
    .k6 {
      animation: moveK6 10s ease-in-out infinite;
    }
    .generate-group {
      clip-path: inset(0 100% 0 0);
      opacity: 0;
      animation:
        moveG 10s ease-in-out infinite,
        revealClip 10s ease-in-out infinite,
        fadeOut 10s ease-in-out infinite;
    }
    .star {
      fill: #ffe34c;
      animation: twinkle 10s infinite ease-in-out alternate;
    }
    .firework {
      animation: riseAndDrop 10s ease-in-out infinite;
      transform-origin: center;
      opacity: 0;
    }
    .red    { fill: #ff4d6d; }
    .green  { fill: #53dd6c; }
    .blue   { fill: #4dabf7; }
    .yellow { fill: #ffd43b; }
    .orange { fill: #ffa94d; }
    .purple { fill: #da77f2; }
  </style>

  <!-- Stars -->
  <circle class="star" cx="50" cy="20" r="3"/>
  <circle class="star" cx="300" cy="10" r="2"/>
  <circle class="star" cx="500" cy="30" r="2.5"/>
  <circle class="star" cx="150" cy="60" r="2"/>

  <!-- g and k6 with burning effect during pause -->
  <text x="300" y="60" class="letter g burning">g</text>
  <text x="332" y="60" class="letter k6 burning">k6</text>

  <!-- 'enerate ' moves with 'g' and reveals -->
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

  <!-- Firework Sparks (vertical rise/drop) -->
  <g class="fireworks-layer">
    <circle class="firework red" cx="300" cy="90" r="2" style="animation-delay: 0s;" />
    <circle class="firework green" cx="310" cy="90" r="2" style="animation-delay: 0.2s;" />
    <circle class="firework blue" cx="320" cy="90" r="2" style="animation-delay: 0.4s;" />
    <circle class="firework yellow" cx="330" cy="90" r="2" style="animation-delay: 0.6s;" />
    <circle class="firework orange" cx="340" cy="90" r="2" style="animation-delay: 0.8s;" />
    <circle class="firework purple" cx="350" cy="90" r="2" style="animation-delay: 1s;" />
    <circle class="firework red" cx="360" cy="90" r="2" style="animation-delay: 1.2s;" />
    <circle class="firework green" cx="370" cy="90" r="2" style="animation-delay: 1.4s;" />
    <circle class="firework blue" cx="380" cy="90" r="2" style="animation-delay: 1.6s;" />
    <circle class="firework yellow" cx="390" cy="90" r="2" style="animation-delay: 1.8s;" />
    <circle class="firework orange" cx="400" cy="90" r="2" style="animation-delay: 2s;" />
    <circle class="firework purple" cx="410" cy="90" r="2" style="animation-delay: 2.2s;" />
    <circle class="firework red" cx="420" cy="90" r="2" style="animation-delay: 2.4s;" />
    <circle class="firework green" cx="430" cy="90" r="2" style="animation-delay: 2.6s;" />
    <circle class="firework blue" cx="440" cy="90" r="2" style="animation-delay: 2.8s;" />
    <circle class="firework yellow" cx="450" cy="90" r="2" style="animation-delay: 3s;" />
    <circle class="firework orange" cx="460" cy="90" r="2" style="animation-delay: 3.2s;" />
    <circle class="firework purple" cx="470" cy="90" r="2" style="animation-delay: 3.4s;" />
    <circle class="firework red" cx="480" cy="90" r="2" style="animation-delay: 3.6s;" />
    <circle class="firework green" cx="490" cy="90" r="2" style="animation-delay: 3.8s;" />
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
