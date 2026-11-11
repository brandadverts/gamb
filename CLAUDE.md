# Gamb Gaming — kurumsal B2B tanıtım sitesi

Canlı adres: https://brandadverts.github.io/gamb-gaming/ (GitHub Pages, `main` dalı kökü, her push'ta otomatik yayın).

## Bu repo nedir
"Wild West Gaming Platform" adlı Figma Make tasarımının (kaynak: https://scene-bright-41964175.figma.site/)
**derlenmiş** React bundle'ı + sonradan eklenen yamalar. Kaynak kod (TSX) bu repoda YOK; düzenlemeler
`assets/index.js` üzerinde birebir string değişimi ve `assets/index.css` sonuna eklenen CSS override'larıyla yapılır.
Köklü tasarım değişikliği gerekirse en sağlıklı yol: Figma Make'te "Remix" ile kaynağı dışa aktarıp yeniden derlemek.

Dosyalar:
- `index.html` — tek sayfa; `assets/index.js` (React, jsxDEV build, ~460 KB) ve `assets/index.css` (Tailwind v4 çıktısı) yükler.
- `assets/index.css` — Make çıktısı + sonda `/* --- Gamb Gaming overrides --- */` ve `/* --- Responsive pass 2 --- */` blokları (bizim eklerimiz; Tailwind arbitrary sınıfları `\[`, `\,`, `\.` ile kaçırılır).
- `assets/mark.svg` — altın marka işareti. Bundle'daki tüm `GG` yazı logoları (`children:\`GG\``) bu görsele yamalandı (`img.gg-logo-img`).
- `assets/giphy/*.mp4` — Giphy klipleri (giphy.mp4 varyantı), `assets/video/*.mp4` — Pexels (ücretsiz ticari lisans), `assets/img/*.jpg` — western/slider fotoğrafları ve gerçek LuckyLira platform ekranları (`screen-*.jpg`).
- `deck.js`, `deck.css`, `img/`, `video/` — ESKİ el yapımı deste; artık kullanılmıyor, silinecek (silme işlemi onay gerektirdiği için kaldı).

## Bundle'da bilinmesi gereken yerler (assets/index.js)
- Kart metinleri: `te={1:[eyebrow,title,desc,bullet1,bullet2,bullet3],...,51:[...]}`; 0 = kapak, 52 = demo formu (`mailto:sales@gambgaming.com`).
- Suit temaları: `y={spade:{bg,accent,...,label:"Platform",start:1},club:...Tech(14),heart:...Why Us(27),diamond:...Solutions(40)}`.
- Kart→medya haritası: `de={2:\`assets/img/screen-sports.jpg\`,5:\`assets/giphy/CFaGnXWf6GABHKKZcC.mp4\`,...}` ve `fe=e=>e`. `.mp4` uzantılı değerler `<video muted autoplay loop playsinline>`, diğerleri `<img>` olarak render edilir (`Me` bileşeni yaması). `screen-` içeren görsellere sepia filtresi uygulanmaz.
- Yama yöntemi: Python ile `js.count(old)==beklenen` assert'i, sonra `replace`. Bir satırı değiştirmeden önce mutlaka say.
- Kart geçiş animasyonları (rulet, aviator, slot 777, blackjack 21, poker, para yağmuru) ve swipe/wheel/klavye gezinmesi Make çıktısında hazır.

## Yerel çalıştırma ve test
```bash
python3 -m http.server 8744   # repo kökünde; http://localhost:8744/
```
Tarayıcı otomasyonunda kart geçişi için `document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))`;
öndeki kart = en yüksek z-index'li `article` (100; arkadakiler 99/98). Son ölçümlü denetim: 1280×720, 1920×1080, 768×1024, 375×812, 360×640 — tüm kartlarda kırpma/bindirme yok.

## Müşteri brief'i (2026-11-09/10 sohbeti) — durum
Karşılandı: 52 kartlık deste, kapakta logo ✓ · suit'e göre renk şeması değişimi ✓ · yan menü → bölüm ✓ · oyun kartı formu, köşe sembolleri, arka planda şeffaf suit ✓ · çapraz kesik görsel şeridi ✓ · geçiş animasyonları (rulet/aviator/slot/blackjack/poker/bonus) ✓ · elle kaydırma + scroll + klavye ✓ · mobil tam ekran ✓ · sabit "Contact us" → kart 52 demo formu ✓ · ajans dilinde satış metni ✓ · gerçek platform ekranları + video + Giphy ✓ · logo altın marka işareti (kapak, filigran, kart arkaları) ✓.

Açık kalanlar (Make tasarımı farklı çözdüğü için dokunulmadı; müşteri isterse yapılacak):
1. Masaüstünde 3–4 kart yan yana ekranı kaplasın (şu an tek kart + arkada iki kart). Bundle'da mümkün değil → Make'te Remix veya yeniden yazım.
2. Logo sağ üstte olsun (şu an sol rayda; mobilde üstte logo yok).
3. Kart arkaları koyu yeşil olsun (şu an deri/altın).
4. İçerik Türkçe (şu an tamamen İngilizce; `te` haritası çevrilerek yapılabilir).
5. İletişim e-postası: Make `sales@gambgaming.com`, eski deste `iletisim@gambgaming.com` — hangisi doğru, müşteriye sor.

## Kurallar
- Ünlü/film/dizi klipleri ve rakip kumarhane markalı GIF'ler kullanılmaz; Giphy'den seçerken illüstrasyon/soyut klipleri tercih et, `giphy.mp4` varyantını indir.
- Varlık eklerken dosyayı ve ona referans veren kodu AYNI commit'te gönder (canlıda kırık görsel kalmasın).
- Commit mesajları Türkçe, `git push origin main` ile yayın.
