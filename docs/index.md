---
layout: default
title: gk6 – Your Postman’s Secret Weapon
---

# ⚡️ gk6 – Your Postman’s Secret Weapon

**Convert boring old Postman collections into blazing-fast [k6](https://k6.io) load tests**  
No manual rewrites. No fragile copy-paste. Just `python gk6.py` and boom — performance testing magic.

[⭐ View on GitHub](https://github.com/gopikrishna4595/gk6)

---

## 🎯 What Does This Tool Actually Do?

**gk6** reads your Postman collection and:

- 🧪 Detects `pm.environment.set()` calls like a bloodhound on a scent trail  
- 🔗 Tracks variable dependencies so chaining works without tears  
- 🧬 Transforms `{{var}}` into something k6 actually understands (no, not a love letter)  
- 📊 Injects `Trend` metrics and response time checks for every request  
- 📤 Outputs a runnable `.js` file and optional `.env` file — just plug & k6  

Basically: **you write nothing, you break nothing, and you get metrics that actually mean something.**

---

## ⚙️ How to Use It

```bash
python gk6.py \
  --collection postman.json \
  --environment env.json \
  --select 1,3,4 \
  --output stress_test.js

k6 run stress_test.js
