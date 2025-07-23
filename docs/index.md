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
    .g { animation: moveG 10s ease-in-out infinite; }
    .k6 { animation: moveK6 10s ease-in-out infinite; }
    .generate-group {
      clip-path: inset(0 100% 0 0);
      opacity: 0;
      animation: moveG 10s ease-in-out infinite, revealClip 10s ease-in-out infinite, fadeOut 10s ease-in-out infinite;
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
  </style>

  <!-- Stars -->
  <circle class="star" cx="50" cy="20" r="3"/>
  <circle class="star" cx="300" cy="10" r="2"/>
  <circle class="star" cx="500" cy="30" r="2.5"/>
  <circle class="star" cx="150" cy="60" r="2"/>

  <!-- g and k6 with burning effect -->
  <text x="300" y="60" class="letter g burning">g</text>
  <text x="332" y="60" class="letter k6 burning">k6</text>

  <!-- 'enerate ' group -->
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

  <!-- 120 fireworks sparks -->
  {% for x in (0..4) %}
    {% assign cx = 50 | plus: x | times: 50 %}
    {% for y in (0..5) %}
      <circle class="firework red left" cx="{{ cx | plus: y }}" cy="100" r="1.2" />
      <circle class="firework blue center" cx="{{ cx | plus: y | plus: 100 }}" cy="100" r="1.2" />
      <circle class="firework green right" cx="{{ cx | plus: y | plus: 200 }}" cy="100" r="1.2" />
      <circle class="firework yellow left" cx="{{ cx | minus: y | plus: 20 }}" cy="100" r="1.2" />
    {% endfor %}
  {% endfor %}
</svg>
</div>
