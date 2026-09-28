# PT100 Calculator

Single-page converter between PT100 resistance and temperature. No build, no dependencies — open `index.html` or use the GitHub Pages link.

**Live:** https://ifrumin.github.io/pt100-calculator/

## What it does

- Ω → °C and °C → Ω (IEC 60751 Callendar–Van Dusen, α = 0.00385)
- Optional 2-wire lead-resistance subtraction (each 1 Ω of copper lead ≈ +2.6 °C error)
- Custom R₀ (PT100 / PT500 / PT1000)
- Quick-reference table; click a row to load it

## Equations

For T ≥ 0 °C: `R = R₀ (1 + A·T + B·T²)`, solved as a quadratic.
For T < 0 °C: `R = R₀ (1 + A·T + B·T² + C·(T − 100)·T³)`, solved by Newton iteration.

`A = 3.9083e-3`, `B = −5.775e-7`, `C = −4.183e-12`. Valid −200 … 850 °C.

## Why

Bench-checking a PT100 with a multimeter while tuning a heater PID loop. Built for the Rinberg Lab GC-olfactometry transfer-line project.


## Python

`python/` has a dependency-free module + CLI, same equations as the page. See the docstring in `python/pt100.py`.

MIT © Idan Frumin & Claude (Anthropic)
