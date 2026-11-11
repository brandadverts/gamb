#!/usr/bin/env python3
"""EN + TR bundle uretimi: assets/index.js (EN, yamali) -> assets/index.js (EN) + assets/index.tr.js (TR).
Ortak yamalar (medya, swipe, haptik, e-posta, kart arkasi) her iki bundle'a; metin cevirisi sadece TR'ye."""
import re, sys, os, json

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, "assets", "index.js")
js = open(SRC, encoding="utf-8").read()

def rep(s, old, new, expect=1, label=""):
    n = s.count(old)
    if n == 0 and new in s:
        print("already applied:", label or old[:50])
        return s
    assert n == expect, f"{label or old[:60]!r}: expected {expect}, found {n}"
    return s.replace(old, new)

# ---------- ortak yamalar ----------
js = rep(js, "sales@gambgaming.com", "info@gambgaming.com", 1, "email")

G = lambda i: f"assets/giphy/{i}.mp4"
media = {
    1: G("11peb90FxNJqfK"), 2: "assets/img/screen-sports.jpg", 3: G("xT9DPi61MmrDLzVFzq"), 4: G("PhdC5X5qr6mzK"),
    5: G("CFaGnXWf6GABHKKZcC"), 6: "assets/img/casino-deposit.jpg", 7: "assets/video/slot-machine-play.mp4",
    8: G("3Hw6enl0Gz29DaiZaY"), 9: G("Vu5UbNpjpqfMq2UFg0"), 10: "assets/img/horse-race.jpg", 11: "assets/img/vip-gambler.jpg",
    12: "assets/img/screen-home.jpg", 14: G("CJxDzLxi9hngW7efbw"), 15: G("jZuKY2yJ2dj1OJfgoN"), 16: G("m7uHEe1Gse6fxmoX7E"),
    17: G("skqsmAzGjZZpS"), 18: G("l46CbPpL3szntVNhS"), 19: "fx:matrix", 20: G("jN9S0faVsUUfdaY50J"),
    21: G("ki1rmMhjvLlm"), 22: G("QpVUMRUJGokfqXyfa1"), 23: G("2i7jspnRBYgg6v4Oki"), 24: "assets/img/stadium.jpg",
    25: G("xUPGchZBY0Oh4qdGXm"), 27: G("lZTvTGEGKU6gnQ2wBr"), 28: G("Ce18KspdcaxaKuZ1HC"), 29: G("BfFFYPSVYr9UR6EtEL"),
    30: G("SdMY3KVYI8mSVz7StH"), 31: G("lXiRm5H49zYmHr3i0"), 32: G("Pk9ux7yJBXKF9CIpg5"), 33: "assets/img/birthday.jpg",
    34: G("qlotpC5nKBnzyBXJea"), 35: "assets/img/sports-racing.jpg", 36: "assets/img/screen-casino.jpg", 37: G("mi6DsSSNKDbUY"),
    38: "assets/img/royal-flush.jpg", 40: G("3ov9jUCYetT3GVwcy4"), 41: G("4ZFWCCSVg8K3RV89xW"), 42: G("VQXzKQKI9yvbrjrKZ1"),
    43: G("13I3peucbA8BfG"), 44: G("OE9hKAfUkurx44b5cE"), 45: G("TiDqYW1SQiA38RgoyY"), 46: G("PqjTdvXImZQfcmTYEO"),
    47: G("7UchwDJiYXiLzuRvEy"), 48: G("qTYW0EfwoAbrG"), 49: G("l4FGJM0LG9UMc0ZMI"), 50: G("3Gm15eZOsNk0tptIuG"),
    51: "assets/img/saloon-hall.jpg",
}
for v in media.values():
    assert v.startswith("fx:") or os.path.exists(os.path.join(ROOT, v)), v
# fx:<ad> değerleri <canvas class="gg-fx-<ad>"> olarak render edilir (animasyon index.html'de)
js = rep(js, "(a.endsWith(`.mp4`)?(0,x.jsxDEV)(`video`",
          "(a.startsWith(`fx:`)?(0,x.jsxDEV)(`canvas`,{className:`gg-fx gg-fx-`+a.slice(3)+` h-full w-full`},void 0,!1,void 0,void 0):a.endsWith(`.mp4`)?(0,x.jsxDEV)(`video`", 1, "fx canvas")
demap = "{" + ",".join(f"{k}:`{v}`" for k, v in sorted(media.items())) + "}"
js, n = re.subn(r"de=\{[^}]*\},fe=e=>e", "de=" + demap + ",fe=e=>e", js)
assert n == 1, "media map"

# dikey swipe: yukari kaydir -> sonraki, asagi -> onceki (yatay davranis korunur)
js = rep(js,
    "onTouchStart:e=>u.current=e.touches[0].clientX,onTouchEnd:t=>{if(u.current===null)return;let n=t.changedTouches[0].clientX-u.current;u.current=null,Math.abs(n)>50&&!t.target.closest(`form`)&&m(e+(n<0?1:-1))}",
    "onTouchStart:e=>u.current=[e.touches[0].clientX,e.touches[0].clientY],onTouchEnd:t=>{if(u.current===null)return;let n=t.changedTouches[0].clientX-u.current[0],o=t.changedTouches[0].clientY-u.current[1];u.current=null;if(t.target.closest(`form`))return;Math.abs(o)>Math.abs(n)?Math.abs(o)>60&&m(e+(o<0?1:-1)):Math.abs(n)>50&&m(e+(n<0?1:-1))}",
    1, "swipe")

# haptik: bolum degisiminde (index.html'deki window.__ggHaptic), overlay titresimi kapali
js = rep(js, "let n=Math.max(0,Math.min(52,e));if(n===t)return t;",
          "let n=Math.max(0,Math.min(52,e));if(n===t)return t;try{window.__ggHaptic&&window.__ggHaptic(t,n)}catch(_){}", 1, "haptic hook")
# geçiş sahnesi (overlay) başlarken titreşim: kısa-kısa-uzun
# overlay titreşimi bundle içinden güvenilir tetiklenmiyor; index.html'deki MutationObserver .gg-overlay eklenince titreştirir
for old in ("function ye(){`vibrate`in navigator&&navigator.vibrate([60,40,60,40,140,60,260])}", "function ye(){try{`vibrate`in navigator&&navigator.vibrate([45,60,45,60,220])}catch(_){}}"):
    if old in js:
        js = js.replace(old, "function ye(){}"); break

# kart arkalari: flip arka yuzu + yigindaki arka kartlar -> .gg-back
js = rep(js, "bg-[#14100A] [backface-visibility:hidden]", "bg-[#14100A] gg-back [backface-visibility:hidden]", 1, "flip back")
h = js.find("repeating-linear-gradient(45deg, rgba(200,169,74,.12) 0 2px, transparent 2px 10px)")
assert h > 0
seg = js[h-1200:h]
k = seg.rfind("className:`")
print("BACK-CARD className region:", seg[k:k+160].replace("\n", " "))
m = re.search(r"className:`([^`]*gg-leather[^`]*)`", seg[k:])
if m and "gg-back" not in m.group(1):
    old = "className:`" + m.group(1) + "`"
    js = js[:h-1200] + js[h-1200:h].replace(old, "className:`" + m.group(1) + " gg-back`", 1) + js[h:]
    print("stack back card tagged .gg-back")
else:
    print("WARN: stack back card className not matched; CSS fallback only")

# yığındaki arka kartlar saydam olmasın (her derinlikte %22 solma kaldırıldı; kaydırılıp giden kart yine 0)
js = rep(js, "opacity:n<0&&!a?0:1-Math.abs(n)*.22,", "opacity:n<0&&!a?0:1,", 1, "stack opacity")

# aviator: uçak SVG'sinin burnu solda, offset-rotate auto ise +x yönüne bakıyordu -> 180° çevir
js = rep(js, "offsetRotate:`auto`", "offsetRotate:`auto 180deg`", 1, "aviator nose")

# rulet geçişi: çizim tekerlek yerine gerçek rulet videosu (daire maskesi içinde), top kaldırıldı
s = js.find("(0,x.jsxDEV)(`div`,{className:`gg-wheel-spin absolute inset-0 rounded-full")
if s > 0:
    endmark = "lineNumber:15,columnNumber:9},this)"
    e = js.find(endmark, s) + len(endmark)
    js = js[:s] + ("(0,x.jsxDEV)(`div`,{className:`absolute inset-0 overflow-hidden rounded-full border-[6px] border-[#C8A94A] "
                   "shadow-[0_0_60px_rgba(200,169,74,.5)] bg-black`,children:(0,x.jsxDEV)(`video`,{src:`assets/video/roulette-real.mp4`,"
                   "autoPlay:!0,muted:!0,loop:!0,playsInline:!0,preload:`auto`,className:`h-full w-full object-cover`},void 0,!1,void 0,void 0)},"
                   "void 0,!1,void 0,void 0)") + js[e:]
    print("roulette wheel -> video")
else:
    assert "assets/video/roulette-real.mp4" in js, "roulette patch missing"
    print("already applied: roulette video")
js = rep(js, "(0,x.jsxDEV)(`div`,{className:`gg-ball absolute left-1/2 top-1/2 h-0 w-0`,children:(0,x.jsxDEV)(`i`,{className:`absolute -left-2 -top-2 h-4 w-4 rounded-full bg-white shadow-[0_0_8px_#fff]`},void 0,!1,{fileName:E,lineNumber:24,columnNumber:68},this)},void 0,!1,{fileName:E,lineNumber:24,columnNumber:9},this),",
          "", 1, "roulette ball") if "gg-ball absolute" in js else js
js = rep(js, "gg-wheel-drop relative h-[260px] w-[260px]", "gg-wheel-drop relative h-[min(72vw,330px)] w-[min(72vw,330px)]", 1, "wheel size")
# rulet videosuna poster: klip daha yüklenmeden ilk kare görünsün
js = rep(js, "src:`assets/video/roulette-real.mp4`,autoPlay:!0", "src:`assets/video/roulette-real.mp4`,poster:`assets/video/roulette-poster.jpg`,autoPlay:!0", 1, "roulette poster")

# silahşor geçiş sahnesi (yeni kind: gunslinger) — gerçek tabanca klibi + namlu alevi + BANG!
GE = ("function Ge(){return(0,x.jsxDEV)(xe,{children:(0,x.jsxDEV)(`div`,{className:`gg-gun relative h-[min(60vw,320px)] w-[min(92vw,560px)] overflow-hidden rounded-2xl border-[4px] border-[#C8A94A] shadow-[0_0_60px_rgba(200,169,74,.5)] bg-black`,children:["
      "(0,x.jsxDEV)(`video`,{src:`assets/video/revolver.mp4`,autoPlay:!0,muted:!0,playsInline:!0,preload:`auto`,className:`h-full w-full object-cover`},void 0,!1,void 0,void 0),"
      "(0,x.jsxDEV)(`div`,{className:`gg-flash pointer-events-none absolute inset-0`},void 0,!1,void 0,void 0),"
      "(0,x.jsxDEV)(`div`,{className:`gg-smoke pointer-events-none`},void 0,!1,void 0,void 0),"
      "(0,x.jsxDEV)(`div`,{className:`gg-bang pointer-events-none absolute inset-0 flex items-center justify-center font-['Rye'] text-6xl text-[#FFB830]`,style:{textShadow:`0 0 40px rgba(255,184,48,.8), 0 4px 0 #6b5518`},children:`BANG!`},void 0,!1,void 0,void 0),"
      "(0,x.jsxDEV)(`div`,{className:`absolute bottom-3 left-1/2 -translate-x-1/2 whitespace-nowrap font-elite text-[12px] uppercase tracking-[0.3em] text-[#F0EAD8]/80`,children:`High Noon`},void 0,!1,void 0,void 0)"
      "]},void 0,!0,void 0,void 0)},void 0,!1,void 0,void 0)}")
if "function Ge()" not in js:
    js = rep(js, "function O({kind:e}){return{roulette:(0,x.jsxDEV)(Se,",
              GE + "function O({kind:e}){return{gunslinger:(0,x.jsxDEV)(Ge,{},void 0,!1,void 0,void 0),roulette:(0,x.jsxDEV)(Se,", 1, "overlay map")
    js = rep(js, "ke=[`blackjack`,`counting`,`slots777`,`aviator`,`roulette`,`flush`,`slots`,`coins`]",
              "ke=[`blackjack`,`counting`,`slots777`,`aviator`,`roulette`,`gunslinger`,`flush`,`slots`,`coins`]", 1, "kind cycle")
    js = rep(js, "be={roulette:2e3,", "be={gunslinger:2300,roulette:2e3,", 1, "durations")
    js = rep(js, "case`coins`:for(let e=0;e<16;e++)",
              "case`gunslinger`:ge(.56,.05,.35,2800),ge(.6,.45,.16,420),he(64,.58,.5,`sine`,.16,24);break;case`coins`:for(let e=0;e<16;e++)", 1, "gunshot sound")
    print("gunslinger overlay added")
else:
    print("already applied: gunslinger")

EN = js

# ---------- TR ----------
from tr_copy import TE_TR, UI_TR
assert sorted(TE_TR) == list(range(1, 52))
for k, v in TE_TR.items():
    assert len(v) == 6, k
    for s in v:
        assert "`" not in s and "${" not in s, (k, s)

tr = EN
i = tr.find("te={1:[")
j = tr.find("},ne={", i)
assert i > 0 and j > i
te_tr = "te={" + ",".join(f"{k}:[" + ",".join("`" + s + "`" for s in v) + "]" for k, v in sorted(TE_TR.items())) + "}"
tr = tr[:i] + te_tr + tr[j+1:]

UI = UI_TR
for old, new, exp in UI:
    n = tr.count(old)
    if n != exp:
        print(f"WARN ui {old[:50]!r}: expected {exp}, found {n}")
        if n == 0: continue
    tr = tr.replace(old, new)

open(os.path.join(ROOT, "assets", "index.js"), "w", encoding="utf-8").write(EN)
open(os.path.join(ROOT, "assets", "index.tr.js"), "w", encoding="utf-8").write(tr)
print("EN", len(EN), "TR", len(tr), "media cards", len(media))
