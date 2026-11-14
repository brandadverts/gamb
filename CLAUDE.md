# Gamb Gaming — kurumsal B2B tanıtım sitesi

Canlı adres: https://brandadverts.github.io/gamb/ (GitHub Pages, repo `brandadverts/gamb`, `main` dalı kökü, her push'ta otomatik yayın; eski ad `gamb-gaming` 2026-11-11'de `gamb` olarak değiştirildi).

## Bu repo nedir
"Wild West Gaming Platform" adlı Figma Make tasarımının (kaynak: https://scene-bright-41964175.figma.site/)
**derlenmiş** React bundle'ı + sonradan eklenen yamalar. Kaynak kod (TSX) bu repoda YOK; düzenlemeler
bundle üzerinde birebir string değişimi ve `assets/index.css` sonuna eklenen CSS override'larıyla yapılır.
Köklü tasarım değişikliği gerekirse en sağlıklı yol: Figma Make'te "Remix" ile kaynağı dışa aktarıp yeniden derlemek.

Dosyalar:
- `index.html` — tek sayfa. Dil seçimi burada: `?lang=tr|en` > `localStorage.gg-lang` > `navigator.language`; TR ise `assets/index.tr.js`, değilse `assets/index.js` (EN) yüklenir. Ayrıca sağ üst logo (`#ggLogo`, tıklanınca kapak), TR/EN seçici (`#ggLang`), bölüm değişimi titreşimi (`window.__ggHaptic`, desen 40-50-40-50-180 ms; iOS Safari titreşim API'sini desteklemez, Android'de çalışır) ve videoları oynatmayı garantileyen MutationObserver.
- `assets/index.js` — EN bundle (Make çıktısı + ortak yamalar). `assets/index.tr.js` — TR bundle (aynı yamalar + Türkçe metinler).
- `tr_copy.py` — Türkçe metinlerin tek kaynağı: kart metinleri `TE_TR` (51 kart, `[eyebrow,title,desc,b1,b2,b3]`; maddesiz kartlarda b1-b3 boş string, bundle `filter(Boolean)` ile boş `<li>` üretmez), arayüz metinleri `UI_TR` (`(EN_literal, TR_literal, beklenen_adet)`).
- `build_i18n.py` — EN bundle'dan TR bundle'ı üretir ve ortak yamaları idempotent uygular; `UI_TR` adet uyuşmazlığında `WARN ui` basar (`WARN: stack back card className not matched` bilinen zararsız uyarı). Metin değiştirmek için TR'yi `tr_copy.py`'de, EN'i `assets/index.js` içindeki `te` haritasında düzenleyip `python3 build_i18n.py && node --check assets/index.js && node --check assets/index.tr.js` çalıştır.
- `assets/index.css` — Make çıktısı + sonda `/* --- Gamb Gaming overrides --- */`, `/* --- Responsive pass 2 --- */`, `/* --- Pass 3 ... Pass 14 --- */` blokları (Tailwind arbitrary sınıfları `\[`, `\,`, `\.` ile kaçırılır). Pass 12-13 kapak sığdırma (yıldız/aralık/odül satırı), Pass 14 içerik kartı metin bloğu `flex:1 1 auto` + görsel şeridi `flex:0 999 27%` (min 64px) + `max-height:720px/650px` yazı ölçeği. TUZAK: bundle'da bir Tailwind keyfi-değer sınıfının DEĞERİNİ değiştirmek (`mt-auto`→`mt-8`, `text-[clamp(26px,...)]`→`text-[clamp(28px,...)]`) derlenmemiş yeni sınıf üretir, CSS'i yoktur → kuralı `index.css` sonuna elle ekle ve `getComputedStyle` ile doğrula.
- `assets/mark.svg` — altın marka işareti; bundle'daki tüm `GG` yazı logoları buna yamalandı (`img.gg-logo-img`).
- `assets/giphy/*.mp4` (Giphy, giphy.mp4 varyantı), `assets/video/*.mp4` (Pexels, ücretsiz ticari lisans), `assets/img/*.jpg` (western/slider fotoğrafları + gerçek LuckyLira ekranları `screen-*.jpg`).

## Bundle'da bilinmesi gereken yerler
- Kart metinleri: `te={1:[eyebrow,title,desc,b1,b2,b3],...,51:[...]}`; 0 = kapak, 52 = demo formu (`mailto:info@gambgaming.com`). Krallar 13/26/39 (bullet'ları boş).
- Suit temaları: `y={spade:{...label,start:1},club:...(14),heart:...(27),diamond:...(40)}`.
- Kart→medya haritası `de={...}` (48 kart; krallar hariç hepsi) ve `fe=e=>e`. `.mp4` → `<video muted autoplay loop playsinline>`, diğerleri `<img>` (`Me` bileşeni yaması); `screen-` görsellerine sepia uygulanmaz.
- Dokunma: yatay VE dikey kaydırma (yukarı → sonraki, aşağı → önceki; form kartında kapalı). Tekerlek ve ok tuşları Make çıktısında hazır.
- `m(...)` gezinme fonksiyonunda `window.__ggHaptic(eski,yeni)` çağrısı var; overlay titreşimi (`ye`) kapatıldı. React dev build StrictMode yüzünden güncelleyici iki kez çalışır — haptik 400 ms içinde tekrarı yoksayar.
- Yama yöntemi: Python ile `js.count(old)==beklenen` assert'i, sonra `replace`.

## Yerel çalıştırma ve test
```bash
python3 -m http.server 8744   # repo kökünde; http://localhost:8744/?lang=tr
```
Tarayıcı otomasyonunda kart geçişi: `document.body.dispatchEvent(new KeyboardEvent('keydown',{key:'ArrowRight',bubbles:true}))`;
öndeki kart = en yüksek z-index'li `article` (100; arkadakiler 99/98, inline style; kartlar eğik/transform'lu olduğundan 'tamamen viewport içinde' filtresi yerine merkez noktası kullan). `window`/`document`'a dispatch çalışmaz (dinleyici `t.target.closest(...)` çağırır), `document.body` şart; adım başı ~240 ms. Kart içi taşma denetimi: `h2.closest('.overflow-hidden')` için `scrollHeight-clientHeight` 0 olmalı; kapakta açıklama `p`'si kapsayıcısına (`parentElement`) sığmalı ve ödül satırı/alt satırla aralık pozitif olmalı. Ölçümlü denetim 1280×720, 1920×1080, 768×1024, 390×844, 375×667, 390×620, 360×640'ta TR+EN yapıldı.

## Müşteri brief'i — durum
Karşılandı: 52 kartlık deste, kapakta logo · suit'e göre renk şeması · yan menü → bölüm · oyun kartı formu, köşe sembolleri, şeffaf suit · çapraz kesik görsel şeridi · geçiş animasyonları · kaydırma + scroll + klavye (dikey kaydırma dahil) · mobil tam ekran · sabit "İletişime geçin" → demo formu · ajans dilinde satış metni · her kartta gerçek görsel/GIF/video · altın logo (kapak, filigran, kart arkaları, sağ üst) · kart arkaları koyu yeşil · TR/EN tarayıcı diline göre · bölüm değişiminde titreşim · e-posta info@gambgaming.com.

Açık: masaüstünde 3–4 kart yan yana (Make tasarımı tek kart + arkada iki kart; bundle'da yapılamaz → Figma Make'te Remix). Müşteri TR/EN metinleri gözden geçirip değişiklik listesi verecek; o liste `tr_copy.py` içindeki `TE_TR`/`UI_TR` üzerinden uygulanır (EN için `te` haritası doğrudan `assets/index.js`'te). 2026-11-14 itibarıyla 51 kartın tamamının h2 başlığı iddialı altyapı sloganı; '15+ yıl tecrübe / uçtan uca full-stack' mesajı kapak alt başlığı, kapak açıklaması ve As-1'de.

## Geçiş sahneleri (overlay)
- Döngü `ke=[blackjack,counting,slots777,aviator,roulette,gunslinger,flush,slots,coins]`; her 4. kartta sırayla tetiklenir (`n%4==0`). Süreler `be={...}`.
- `aviator`: uçak SVG'sinin burnu solda olduğu için `offsetRotate: auto 180deg` (aksi halde ters uçar).
- `roulette` (`Se`): çizim tekerlek yerine `assets/video/roulette-real.mp4` (Pexels 7607440, gerçek çekim) daire maskesinde; ortada logo, sonda "0" rozeti.
- `gunslinger` (`Ge`): `assets/video/revolver.mp4` (Pexels 13618251) + CSS namlu alevi (`.gg-flash`), duman (`.gg-smoke`), geri tepme (`.gg-gun`), "BANG!" (`.gg-bang`), alt etiket High Noon / Düello Vakti; ses `ve()` switch'inde `case gunslinger` (noise + düşük sinüs).
- Her iki video `index.html`'de gizli `<video preload="auto">` ile önceden yüklenir.

## Kurallar
- Ünlü/film/dizi klipleri ve rakip kumarhane markalı GIF'ler kullanılmaz; Giphy'den illüstrasyon/soyut klipler, `giphy.mp4` varyantı.
- Varlık ve ona referans veren kod AYNI commit'te.
- Commit mesajları Türkçe, `git push origin main` ile yayın.
