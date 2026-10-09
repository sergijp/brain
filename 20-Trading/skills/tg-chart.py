#!/usr/bin/env python3
"""
Малює читабельний графік угоди для Telegram (SVG -> PNG через rsvg-convert).
Позиція займає майже весь кадр: свічки зліва, великий червоно-зелений box
(ризик/ціль) справа, великі підписи ENTRY / SL / TP.

Використання:
    python3 tg-chart.py < input.json
    python3 tg-chart.py input.json

Вхідний JSON:
{
  "symbol": "GBPUSD", "tf": "M5", "side": "short",          # short | long
  "entry": 1.32084, "sl": 1.32187, "tp": 1.31815,
  "entry_time": 1791465300,                                   # unix, бар входу
  "bars": [[t, o, h, l, c], ...],                             # M5, від ~12 барів до входу і до зараз
  "levels": [[1.32134, "Session Open (ЗНЯТО)"], ...],         # контекстні рівні (необов'язково)
  "title_extra": "13:15 UTC", "reason": "зняття ... ",        # необов'язково
  "exit_time": 1791466800, "exit_price": 1.31815,              # лише для ЗАКРИТТЯ: бар і ціна виходу
  "status": "ВІДКРИТО" | "СТОП −1.00R" | "ЦІЛЬ +2.61R",       # необов'язково
  "out": "/шлях/до/файлу.png", "pip": 0.0001,
  "pending": true,                                            # ЛІМІТКА: box починається після останньої свічки
  "from_zone": {"lo": 1.12394, "hi": 1.12428, "label": "H1 OB ↓ + зняття Asia H"},   # ЗВІДКИ пішла/піде ціна
  "to_zone":   {"lo": 1.12104, "hi": 1.12129, "label": "SSL Asia L / PDC"}            # КУДИ йде ціна
}
Друкує шлях до PNG.
"""
import json
import subprocess
import sys
from datetime import datetime, timezone
from xml.sax.saxutils import escape

FONT = "Helvetica, Arial, sans-serif"
GREEN, RED, INK, GRID = "#1f9d8b", "#e0504d", "#17212b", "#e4e8ec"


def main():
    raw = open(sys.argv[1]).read() if len(sys.argv) > 1 else sys.stdin.read()
    d = json.loads(raw)
    pip = d.get("pip", 0.0001)
    dec = d.get("dec", 5 if pip < 0.01 else 1)
    unit = "п" if pip < 1 else "пт"

    def fmt(v):
        return f"{v:.{dec}f}"

    side = d["side"]
    entry, sl, tp = d["entry"], d["sl"], d["tp"]
    bars = d["bars"]
    out = d.get("out", "/tmp/tg-chart.png")

    pending = bool(d.get("pending"))
    fz, tz = d.get("from_zone"), d.get("to_zone")
    xi = None
    if pending:
        first = max(0, len(bars) - 40)
        view = bars[first:]
        ei = len(view)                    # box починається одразу після останньої свічки
        after = 0
        box_w = 24
        slots = ei + box_w + 3
    else:
        ei = next((i for i, b in enumerate(bars) if b[0] == d.get("entry_time")), None)
        if ei is None:
            ei = max(0, len(bars) - 1)
        first = max(0, ei - 12)
        view = bars[first:]
        ei -= first
        after = len(view) - 1 - ei
        if d.get("exit_time"):
            xi = next((i - first for i, b in enumerate(bars) if b[0] == d["exit_time"]), None)
    if pending:
        pass
    elif xi is not None:
        box_w = max(4, xi - ei + 1)      # box закінчується на барі виходу
        slots = ei + box_w + 14          # місце справа під великі підписи
    else:
        box_w = max(26, after + 16)      # ширина position-box у барах
        slots = ei + box_w + 3

    W, H = 1600, 1000
    x0, x1 = 30, 1430                      # область графіка (без шкали ціни)
    y0, y1 = 190, 905
    slot = (x1 - x0) / slots

    lows = [b[3] for b in view] + [sl, tp, entry]
    highs = [b[2] for b in view] + [sl, tp, entry]
    for z in (fz, tz):
        if z:
            lows.append(z["lo"])
            highs.append(z["hi"])
    pad = 3 * pip
    pmin, pmax = min(lows) - pad, max(highs) + pad

    def Y(p):
        return y1 - (p - pmin) / (pmax - pmin) * (y1 - y0)

    def X(i):                              # центр свічки i
        return x0 + (i + 0.5) * slot

    risk = abs(sl - entry) / pip
    reward = abs(tp - entry) / pip
    rr = reward / risk if risk else 0
    sname = "ШОРТ" if side == "short" else "ЛОНГ"
    s = []
    a = s.append
    a(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" font-family="{FONT}">')
    a(f'<rect width="{W}" height="{H}" fill="#ffffff"/>')
    a('<defs><marker id="ah" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#5b3fd1"/></marker></defs>')

    # заголовок
    status = d.get("status", "")
    a(f'<text x="30" y="58" font-size="44" font-weight="700" fill="{INK}">{escape(d["symbol"])} · {escape(d.get("tf","M5"))} · {sname} {fmt(entry)}</text>')
    if status:
        col = GREEN if "ЦІЛЬ" in status else RED if "СТОП" in status else INK
        a(f'<text x="{W-30}" y="58" font-size="44" font-weight="700" fill="{col}" text-anchor="end">{escape(status)}</text>')
    sub = f'Ризик {risk:.1f} {unit} · Ціль {reward:.1f} {unit} · RR {rr:.2f}'
    if d.get("title_extra"):
        sub += f' · {d["title_extra"]}'
    a(f'<text x="30" y="104" font-size="30" fill="#4a5866">{escape(sub)}</text>')
    if d.get("reason"):
        a(f'<text x="30" y="138" font-size="24" fill="#6b7885">{escape(d["reason"])}</text>')

    # сітка і шкала ціни
    rng_p = (pmax - pmin) / pip
    step_pips = 5 if rng_p <= 60 else 10 if rng_p <= 150 else 20 if rng_p <= 400 else 50
    step = step_pips * pip
    p = int(pmin / step) * step
    while p <= pmax:
        if p >= pmin:
            y = Y(p)
            a(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
            a(f'<text x="{x1+10}" y="{y+8:.1f}" font-size="22" fill="#7a8794">{fmt(p)}</text>')
        p += step

    # контекстні рівні
    for lv in d.get("levels", []):
        price, label = lv[0], lv[1]
        if pmin <= price <= pmax:
            y = Y(price)
            a(f'<line x1="{x0}" y1="{y:.1f}" x2="{x1}" y2="{y:.1f}" stroke="#9aa6b2" stroke-width="1.5" stroke-dasharray="8 6"/>')
            a(f'<text x="{x0+8}" y="{y-6:.1f}" font-size="21" fill="#4a5866" stroke="#ffffff" stroke-width="6" stroke-linejoin="round" paint-order="stroke">{escape(label)} {fmt(price)}</text>')

    # зони: ЗВІДКИ (фіолетова) і КУДИ (бірюзова)
    ZCOL = {"from": "#6a4bd8", "to": "#0b8f8c"}
    for key, z, tag in (("from", fz, "ЗВІДКИ"), ("to", tz, "КУДИ")):
        if not z:
            continue
        yt, yb = Y(z["hi"]), Y(z["lo"])
        hgt = max(10, yb - yt)
        c = ZCOL[key]
        a(f'<rect x="{x0}" y="{yt:.1f}" width="{x1-x0}" height="{hgt:.1f}" fill="{c}" fill-opacity="0.16" stroke="{c}" stroke-width="2" stroke-dasharray="10 6"/>')
        lab = f'{tag}: {z.get("label","")}  {fmt(z["lo"])}–{fmt(z["hi"])}'
        ty = yt - 8 if key == "from" and side == "short" else yb + 28 if key == "from" else (yb + 28 if side == "short" else yt - 8)
        a(f'<text x="{x0+8}" y="{ty:.1f}" font-size="22" font-weight="700" fill="{c}" stroke="#ffffff" stroke-width="7" stroke-linejoin="round" paint-order="stroke">{escape(lab)}</text>')

    # position box (як у TradingView): від бару входу вправо
    bx0 = X(ei) - slot / 2
    bx1 = bx0 + box_w * slot
    yE, yS, yT = Y(entry), Y(sl), Y(tp)
    a(f'<rect x="{bx0:.1f}" y="{min(yE,yS):.1f}" width="{bx1-bx0:.1f}" height="{abs(yS-yE):.1f}" fill="{RED}" fill-opacity="0.20" stroke="{RED}" stroke-width="2"/>')
    a(f'<rect x="{bx0:.1f}" y="{min(yE,yT):.1f}" width="{bx1-bx0:.1f}" height="{abs(yT-yE):.1f}" fill="{GREEN}" fill-opacity="0.20" stroke="{GREEN}" stroke-width="2"/>')
    a(f'<line x1="{bx0:.1f}" y1="{yE:.1f}" x2="{bx1:.1f}" y2="{yE:.1f}" stroke="{INK}" stroke-width="3"/>')

    # великі підписи всередині box
    tx = (bx1 + 16) if xi is not None else max(bx0 + 24, X(len(view) - 1) + slot * 1.6)
    if (fz or tz) and xi is None:
        tx = max(tx, x0 + (x1 - x0) * 0.52)   # підписи угоди правіше від підписів зон
    HALO = 'stroke="#ffffff" stroke-width="7" stroke-linejoin="round" paint-order="stroke"'
    a(f'<text x="{tx:.1f}" y="{yE-12:.1f}" font-size="34" font-weight="700" fill="{INK}" {HALO}>ВХІД {fmt(entry)}</text>' if side == "long"
      else f'<text x="{tx:.1f}" y="{yE+40:.1f}" font-size="34" font-weight="700" fill="{INK}" {HALO}>ВХІД {fmt(entry)}</text>')
    sl_y = yS + (-12 if side == "long" else 38)
    a(f'<text x="{tx:.1f}" y="{(yS+44) if side=="long" else (yS-14):.1f}" font-size="34" font-weight="700" fill="{RED}" {HALO}>SL {fmt(sl)}  (−{risk:.1f} {unit})</text>')
    a(f'<text x="{tx:.1f}" y="{(yT+40) if side=="short" else (yT-14):.1f}" font-size="34" font-weight="700" fill="{GREEN}" {HALO}>TP {fmt(tp)}  (+{reward:.1f} {unit})</text>')
    mid = (yE + yT) / 2
    if xi is None:
     a(f'<text x="{(bx0+bx1)/2:.1f}" y="{mid+22:.1f}" font-size="64" font-weight="700" fill="{GREEN}" fill-opacity="0.55" text-anchor="middle">RR {rr:.2f}</text>')

    # стрілка ЗВІДКИ → КУДИ
    if fz and tz:
        ax = (bx1 - 46) if True else x1 - 60
        ya, yb2 = Y((fz["lo"] + fz["hi"]) / 2), Y((tz["lo"] + tz["hi"]) / 2)
        a(f'<line x1="{ax:.1f}" y1="{ya:.1f}" x2="{ax:.1f}" y2="{yb2:.1f}" stroke="#5b3fd1" stroke-width="7" marker-end="url(#ah)" stroke-opacity="0.85"/>')

    # свічки
    cw = max(4, slot * 0.62)
    for i, (t, o, h, l, c) in enumerate(view):
        col = GREEN if c >= o else RED
        x = X(i)
        a(f'<line x1="{x:.1f}" y1="{Y(h):.1f}" x2="{x:.1f}" y2="{Y(l):.1f}" stroke="{col}" stroke-width="2.5"/>')
        top, bot = Y(max(o, c)), Y(min(o, c))
        a(f'<rect x="{x-cw/2:.1f}" y="{top:.1f}" width="{cw:.1f}" height="{max(2,bot-top):.1f}" fill="{col}"/>')
    # маркер виходу
    if xi is not None and d.get("exit_price") is not None:
        ex, ey = X(xi), Y(d["exit_price"])
        ecol = GREEN if "ЦІЛЬ" in status else RED if "СТОП" in status else INK
        a(f'<circle cx="{ex:.1f}" cy="{ey:.1f}" r="13" fill="{ecol}" stroke="#ffffff" stroke-width="4"/>')
        a(f'<text x="{ex:.1f}" y="{ey-26:.1f}" font-size="30" font-weight="700" fill="{ecol}" text-anchor="middle" stroke="#ffffff" stroke-width="7" stroke-linejoin="round" paint-order="stroke">ВИХІД {fmt(d["exit_price"])}</text>')
        a(f'<polygon points="{ex:.1f},{y1+4} {ex-9:.1f},{y1+22} {ex+9:.1f},{y1+22}" fill="{ecol}"/>')
    # маркер бару входу
    if not pending:
        a(f'<polygon points="{X(ei):.1f},{y1+4} {X(ei)-9:.1f},{y1+22} {X(ei)+9:.1f},{y1+22}" fill="{INK}"/>')
    else:
        a(f'<line x1="{x0}" y1="{yE:.1f}" x2="{bx0:.1f}" y2="{yE:.1f}" stroke="{INK}" stroke-width="3" stroke-dasharray="14 8"/>')

    # мітки на шкалі ціни
    for price, col, txt in ((entry, INK, "ENTRY"), (sl, RED, "SL"), (tp, GREEN, "TP")):
        y = Y(price)
        a(f'<rect x="{x1+4}" y="{y-17:.1f}" width="160" height="34" rx="4" fill="{col}"/>')
        a(f'<text x="{x1+12}" y="{y+8:.1f}" font-size="22" font-weight="700" fill="#ffffff">{fmt(price)}</text>')

    # шкала часу (UTC)
    every = 6
    for i, b in enumerate(view):
        if i % every == 0:
            hh = datetime.fromtimestamp(b[0], tz=timezone.utc).strftime("%H:%M")
            a(f'<text x="{X(i):.1f}" y="{y1+50}" font-size="22" fill="#7a8794" text-anchor="middle">{hh}</text>')
    if fz or tz:
        a(f'<text x="30" y="{H-12}" font-size="22" fill="#4a5866"><tspan fill="#6a4bd8" font-weight="700">■ звідки</tspan>   <tspan fill="#0b8f8c" font-weight="700">■ куди</tspan>   стрілка — рух ціни</text>')
    a(f'<text x="{x1}" y="{H-12}" font-size="20" fill="#9aa6b2" text-anchor="end">час UTC · M5</text>')
    a('</svg>')

    svg_path = out.rsplit(".", 1)[0] + ".svg"
    open(svg_path, "w").write("\n".join(s))
    subprocess.run(["rsvg-convert", "-o", out, svg_path], check=True)
    print(out)


if __name__ == "__main__":
    main()
