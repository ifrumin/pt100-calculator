#!/usr/bin/env python3
"""PT100 resistance <-> temperature (IEC 60751, Callendar-Van Dusen).

    from pt100 import ohm_to_temp, temp_to_ohm
    ohm_to_temp(150.0)            # -> 130.4 Â°C
    ohm_to_temp(166.0, lead=0.3)  # subtract 2-wire lead resistance
    temp_to_ohm(200.0)            # -> 175.86 Î©

CLI:  python pt100.py 150        # Î© -> Â°C
      python pt100.py -t 200     # Â°C -> Î©
      python pt100.py 150 --lead 0.3 --r0 100
"""
import argparse, math, sys

try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

A = 3.9083e-3
B = -5.775e-7
C = -4.183e-12
T_MIN, T_MAX = -200.0, 850.0


def temp_to_ohm(t: float, r0: float = 100.0) -> float:
    if not T_MIN <= t <= T_MAX:
        raise ValueError(f"temperature {t} Â°C outside {T_MIN}..{T_MAX}")
    if t >= 0:
        return r0 * (1 + A * t + B * t * t)
    return r0 * (1 + A * t + B * t * t + C * (t - 100) * t ** 3)


def ohm_to_temp(r: float, r0: float = 100.0, lead: float = 0.0) -> float:
    r = r - lead
    if r < r0 * 0.1852 or r > r0 * 3.9048:
        raise ValueError(f"resistance {r} Î© outside PT range for R0={r0}")
    if r >= r0:
        d = A * A - 4 * B * (1 - r / r0)
        return (-A + math.sqrt(d)) / (2 * B)
    t = (r / r0 - 1) / A
    for _ in range(50):
        f = r0 * (1 + A * t + B * t * t + C * (t - 100) * t ** 3) - r
        df = r0 * (A + 2 * B * t + C * (4 * t ** 3 - 300 * t * t))
        dt = f / df
        t -= dt
        if abs(dt) < 1e-7:
            break
    return t


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    p.add_argument("value", type=float, help="resistance in Î© (or Â°C with -t)")
    p.add_argument("-t", "--temp", action="store_true", help="input is Â°C, output Î©")
    p.add_argument("--r0", type=float, default=100.0, help="R at 0 Â°C (default 100)")
    p.add_argument("--lead", type=float, default=0.0, help="2-wire lead resistance to subtract, Î©")
    a = p.parse_args(argv)
    try:
        if a.temp:
            print(f"{temp_to_ohm(a.value, a.r0):.3f} Î©")
        else:
            t = ohm_to_temp(a.value, a.r0, a.lead)
            print(f"{t:.2f} Â°C  ({t * 9 / 5 + 32:.1f} Â°F, {t + 273.15:.2f} K)")
    except ValueError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()
