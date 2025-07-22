---
layout: default
title: ⚡️ gk6 – k6’s Secret Weapon for Postman Collections
---

<div class="hero-animation">
  <span class="letter g">g</span>
  <span class="spark"></span>
  <span class="generate">enerate</span>
  <span class="letter k6">k6</span>
</div>


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

## 🚀 Quick Usage

```bash
python gk6.py \
  --collection my_collection.json \
  --environment my_env.json \
  --select 1,2,3 \
  --output test_script.js

k6 run test_script.js
