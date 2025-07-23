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
    @keyframes burnEffect {
      0%, 44%, 85%, 100% {
        filter: none;
        fill: #fff;
        transform: none;
      }
      45%, 48%, 52%, 56%, 58% {
        fill: #ffaa33;
        filter: drop-shadow(0 0 2px #ffaa33) drop-shadow(0 0 4px #ffdd55);
        transform: scaleY(1.05) translateY(-1px);
      }
      46%, 50%, 54% {
        fill: #ffee99;
        filter: drop-shadow(0 0 3px #ffcc33) drop-shadow(0 0 6px #ff6600);
        transform: scaleY(0.96) translateY(1px);
      }
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
    @keyframes moveG {
      0%, 15%   { transform: translateX(0); }
      25%, 85%  { transform: translateX(-64px); }
      95%, 100% { transform: translateX(0); }
    }
    @keyframes moveK6 {
      0%, 15%   { transform: translateX(0); }
      25%, 85%  { transform: translateX(128px); }
      95%, 100% { transform: translateX(0); }
    }
    @keyframes revealClip {
      0%, 15%   { clip-path: inset(0 100% 0 0); }
      25%, 85%  { clip-path: inset(0 0% 0 0); }
      95%, 100% { clip-path: inset(0 100% 0 0); }
    }
    @keyframes fadeOut {
      0%, 70%   { opacity: 1; }
      85%, 100% { opacity: 0; }
    }
    .star {
      fill: #ffe34c;
      animation: twinkle 10s infinite ease-in-out alternate;
    }
    @keyframes twinkle {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1; }
    }

    .firework {
      opacity: 0;
      r: 2;
    }
    .arc1 {
      animation: arc1 10s ease-in-out infinite;
    }
    .arc2 {
      animation: arc2 10s ease-in-out infinite;
    }
    .arc3 {
      animation: arc3 10s ease-in-out infinite;
    }
    .arc4 {
      animation: arc4 10s ease-in-out infinite;
    }

    @keyframes arc1 {
      25% { opacity: 1; transform: translate(-40px, -30px) scale(1.5); }
      50% { opacity: 1; transform: translate(-60px, -70px) scale(1); }
      85% { opacity: 0; transform: translate(-80px, -100px) scale(0.5); }
    }
    @keyframes arc2 {
      28% { opacity: 1; transform: translate(50px, -20px) scale(1.2); }
      55% { opacity: 1; transform: translate(70px, -60px) scale(1); }
      85% { opacity: 0; transform: translate(90px, -90px) scale(0.5); }
    }
    @keyframes arc3 {
      30% { opacity: 1; transform: translate(0, -40px) scale(1.4); }
      55% { opacity: 1; transform: translate(-30px, -80px) scale(1); }
      85% { opacity: 0; transform: translate(-50px, -110px) scale(0.5); }
    }
    @keyframes arc4 {
      33% { opacity: 1; transform: translate(20px, -25px) scale(1.3); }
      58% { opacity: 1; transform: translate(40px, -70px) scale(1); }
      85% { opacity: 0; transform: translate(60px, -90px) scale(0.5); }
    }
  </style>

  <!-- Stars -->
  <circle class="star" cx="50" cy="20" r="3"/>
  <circle class="star" cx="300" cy="10" r="2"/>
  <circle class="star" cx="500" cy="30" r="2.5"/>
  <circle class="star" cx="150" cy="60" r="2"/>

  <!-- Fireworks (behind text) -->
  <circle class="firework arc1" cx="360" cy="80" fill="#ff2e63" />
  <circle class="firework arc2" cx="370" cy="90" fill="#33cc33" />
  <circle class="firework arc3" cx="390" cy="75" fill="#3399ff" />
  <circle class="firework arc4" cx="410" cy="85" fill="#ffff66" />
  <circle class="firework arc1" cx="430" cy="88" fill="#ff9900" />
  <circle class="firework arc2" cx="450" cy="70" fill="#cc33cc" />
  <circle class="firework arc3" cx="470" cy="95" fill="#00ccff" />
  <circle class="firework arc4" cx="490" cy="78" fill="#ff3366" />

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
