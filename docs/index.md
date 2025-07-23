---
layout: default
title: ⚡️ gk6 – k6’s Secret Weapon for Postman Collections
---
<svg width="100%" height="100" viewBox="0 0 800 100">
  <style>
    .letter {
      font: 900 40px 'Fira Code', monospace;
      fill: black;
      dominant-baseline: middle;
      text-anchor: middle;
    }
    .gk {
      opacity: 1;
      animation: slideApart 1s ease-out forwards;
    }
    .generate {
      opacity: 0;
      animation: revealLetters 1s 1s ease-out forwards;
    }
    @keyframes slideApart {
      0% {
        transform: translateX(0);
      }
      100% {
        transform: translateX(-30px);
      }
    }
    @keyframes revealLetters {
      0% { opacity: 0; letter-spacing: 50px; }
      100% { opacity: 1; letter-spacing: 8px; }
    }
  </style>

  <text x="370" y="60" class="letter gk" style="font-weight:900;">g</text>
  <text x="400" y="60" class="letter generate">e n e r a t e</text>
  <text x="540" y="60" class="letter gk" style="font-weight:900;">k6</text>
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
