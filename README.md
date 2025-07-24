# ⚡️ gk6 – Generate k6 Load Tests from Postman Collections

**gk6** is a Python CLI tool that converts Postman collections into dynamic [k6](https://k6.io) performance testing scripts — with support for chaining variables, environment parsing, automated metrics, and HTML reporting.

Built to automate what you shouldn’t have to hand-code.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)
[🌐 GitHub Pages Site](https://gopikrishna4595.github.io/gk6/)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)

---

## 🎯 Why gk6?

If you use Postman for API testing and k6 for performance testing, this tool connects the dots:
- No need to rewrite each request manually
- It respects your chaining logic (`pm.environment.set`)
- It supports environments and headers out of the box
- It gives you visibility with built-in checks and trend metrics

---

## 🧩 Features

✅ Convert any Postman Collection to a runnable k6 script  
✅ Supports `GET`, `POST`, `PUT`, `DELETE` methods  
✅ Recognizes and converts environment variables (`{{var}}`)  
✅ Detects request chaining via `pm.environment.set()`  
✅ Auto-generates `Trend` metrics and `check()` assertions  
✅ CLI-friendly with `argparse`  
✅ Optional `.env` and HTML summary output with `k6-reporter`

---

## 🚀 Quick Start

### 1. Install requirements
No extra packages needed — just Python 3.8+.

You’ll also need [k6](https://k6.io/docs/getting-started/installation) installed to run the output.

