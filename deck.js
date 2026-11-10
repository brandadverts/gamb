/* Gamb Gaming — 52 kartlık deste motoru v3. Bağımsız vanilla JS, dış kütüphane yok. */
(function () {
  'use strict';

  var SUITS = [
    { key: 'spades', sym: '♠', color: 'black', label: 'Platform' },
    { key: 'hearts', sym: '♥', color: 'red', label: 'Neden Biz' },
    { key: 'diamonds', sym: '♦', color: 'red', label: 'Teknoloji' },
    { key: 'clubs', sym: '♣', color: 'black', label: 'Sonuçlar' }
  ];
  var RANKS = ['A','2','3','4','5','6','7','8','9','10','J','Q','K'];

  var IMG = {
    screenHome: 'assets/images/screen-home.jpg',
    screenCasino: 'assets/images/screen-casino.jpg',
    screenSports: 'assets/images/screen-sports.jpg',
    wSaloonHall: 'img/western/saloon-hall.jpg',
    wRoyalFlush: 'img/western/royal-flush.jpg',
    wHorseRace: 'img/western/horse-race.jpg',
    wVipGambler: 'img/western/vip-gambler.jpg'
  };
  /* Pexels — ücretsiz ticari lisans (pexels.com/license), stüdyo/model çekimi
     veya jenerik şehir manzarası; gerçek/özel bir mekanın markasını göstermez. */
  var VID = {
    vRoulette: 'video/roulette-spin.mp4',
    vSlot: 'video/slot-machine-play.mp4'
  };
  var LOGOS = ['evolutiongaming','vivogaming','xprogaming','nucleusgaming','rubyplay','bigtimegaming','absolutelivegaming'];
  function logoRow() {
    return '<div class="card-logorow">' + LOGOS.map(function (l) {
      return '<img src="img/provider-logos/' + l + '.svg" alt="" loading="lazy" />';
    }).join('') + '</div>';
  }
  function list(items) { return '<ul class="card-list">' + items.map(function (t) { return '<li>' + t + '</li>'; }).join('') + '</ul>'; }

  /* Western ikon seti — basit, düz siluet, dış kütüphane yok */
  var WICON = {
    hat: '<svg viewBox="0 0 48 32" fill="currentColor"><path d="M4,23 Q24,16 44,23 Q44,27 39,27 L9,27 Q4,27 4,23 Z M15,23 Q15,7 24,7 Q33,7 33,23 Z"/></svg>',
    cactus: '<svg viewBox="0 0 24 32" fill="none" stroke="currentColor" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12,31 L12,9 Q12,4 16,4 Q19,4 19,8 M12,13 L6,13 Q4,13 4,11 L4,7 M6,13 L6,22 M19,17 L24,17 M19,21 L19,10"/></svg>',
    revolver: '<svg viewBox="0 0 48 28" fill="currentColor"><path d="M4,16 L4,20 L9,20 L9,24 L20,24 L20,18 L32,18 L32,14 L44,14 L44,10 L28,10 L28,6 L9,6 L9,12 L4,12 Z"/></svg>',
    bullet: '<svg viewBox="0 0 14 28" fill="currentColor"><path d="M7,1 L11,7 L11,24 Q11,26 9,26 L5,26 Q3,26 3,24 L3,7 Z"/></svg>',
    horseshoe: '<svg viewBox="0 0 40 44" fill="none" stroke="currentColor" stroke-width="4" stroke-linecap="round"><path d="M8,8 C8,24 14,36 20,36 C26,36 32,24 32,8"/></svg>',
    star: '<svg viewBox="0 0 48 48" fill="currentColor"><polygon points="24,2 28,17 44,17 31,27 36,43 24,33 12,43 17,27 4,17 20,17"/></svg>'
  };
  function wicon(name, cls) { return '<span class="wicon ' + (cls || '') + '">' + WICON[name] + '</span>'; }
  var WDECO_CYCLE = ['hat', 'cactus', 'revolver', 'bullet', 'horseshoe', 'star'];
  function westernDeco(idx) {
    var a = WDECO_CYCLE[idx % WDECO_CYCLE.length];
    var b = WDECO_CYCLE[(idx + 3) % WDECO_CYCLE.length];
    return '<div class="card-deco">' + wicon(a, 'deco-ic') + wicon(b, 'deco-ic') + '</div>';
  }

  /* ---------------- İÇERİK — her suit tam 13 kart: A (ana başlık) + 2-10 (9 alt başlık) + J/Q/K (3 görsel vitrin) ---------------- */
  var SUIT_CARDS = {

    spades: [
      { layout: 'text', rank: 'ace', eyebrow: 'PLATFORM', title: 'Oran geç gelirse, oyuncu rakibe gider.',
        text: 'Gamb Gaming\'in oran motoru 120ms\'nin altında güncellenir. Spor bahisten canlı casinoya tek platform.' },
      { layout: 'text', eyebrow: 'SPOR BAHİS MOTORU', title: 'Saniyeler içinde oran, saniyeler içinde kupon',
        text: 'Yüksek trafikte bile gecikmesiz güncelleme ve tek dokunuşla 1-X-2 hızlı bahis akışı.' },
      { layout: 'text', eyebrow: 'CASİNO', title: 'Binlerce başlık, tek entegrasyon',
        text: 'Evolution, Vivo, XPro ve daha fazlası tek API sözleşmesiyle; akıllı kapak eşleştirme kırık görsel bırakmaz.' },
      { layout: 'text', eyebrow: 'CÜZDAN', title: 'Oyuncu bekleme ekranında kalmasın',
        text: 'Kripto para birimlerinde anında yatırma/çekme, yerel banka yöntemleriyle birlikte.' },
      { layout: 'text', eyebrow: 'BAĞLILIK', title: 'Oyuncuyu platformda tutan katman',
        text: 'Canlı kazanç akışı, topluluk sohbeti, bonus yağmuru ve VIP rakeback tek pakette.' },
      { layout: 'text', eyebrow: 'HIZ', title: 'Bekleyen oyuncu, terk eden oyuncudur',
        text: 'Redis önbellekli API katmanı, oyun açılışı ve oran güncellemesindeki her gecikmeyi yok eder.' },
      { layout: 'text', eyebrow: 'GÜVENLİK', title: 'Büyümenizi dolandırıcılık durdurmasın',
        text: 'Cihaz tabanlı risk skorlaması ve bot koruması varsayılan olarak açık.' },
      { layout: 'text', eyebrow: 'LOKALİZASYON', title: 'Yeni pazar, bir hafta sonu projesi kadar basit',
        text: 'Merkezi ifade tablosu, arayüzün tamamını sayfa yeniden yazılmadan yeni bir dile taşır.' },
      { layout: 'text', eyebrow: 'WHITE-LABEL', title: 'Bir çekirdek, sınırsız marka',
        text: 'Aynı altyapı üzerinde farklı tema ve logoyla yeni bir marka açmak günler sürer.' },
      { layout: 'text', eyebrow: 'MARJ YÖNETİMİ', title: 'Marjı motor değil, siz belirlersiniz',
        text: 'Operatöre özel marj ve limit yönetimi, kâr marjınızdan ödün vermenizi gerektirmez.' },
      { layout: 'showcase', eyebrow: 'VİTRİN', title: 'Canlı spor bahis deneyimi', image: IMG.wHorseRace },
      { layout: 'showcase', eyebrow: 'VİTRİN', title: 'Canlı casino salonu', video: VID.vRoulette },
      { layout: 'showcase', eyebrow: 'VİTRİN', title: 'Cüzdan &amp; ödeme anı', image: IMG.wRoyalFlush }
    ],

    hearts: [
      { layout: 'text', rank: 'ace', eyebrow: 'NEDEN BİZ', title: 'Haftalarca süren kurulum, rakibe yetişme fırsatıdır.',
        text: 'Gamb Gaming\'i seçen operatörler hızı, marka esnekliğini ve büyüme desteğini aynı anda alır.' },
      { layout: 'text', eyebrow: 'KARŞILAŞTIRMA', title: 'Devreye alma: haftalar yerine günler',
        text: 'Geleneksel altyapılarda haftalar süren kurulum, bizde günler içinde tamamlanır.' },
      { layout: 'text', eyebrow: 'KARŞILAŞTIRMA', title: 'Marka: tek yerine sınırsız',
        text: 'Tek marka kısıtlaması yok — aynı çekirdek üzerinde istediğiniz kadar marka.' },
      { layout: 'text', eyebrow: 'KARŞILAŞTIRMA', title: 'Oran akışı: periyodik yerine gerçek zamanlı',
        text: 'Oranlar sabit aralıklarla değil, gerçek zamanlı güncellenir.' },
      { layout: 'text', eyebrow: 'KARŞILAŞTIRMA', title: 'Destek: bilet yerine doğrudan ekip',
        text: 'Bilet sistemi beklemek yok — doğrudan teknik ekibe ulaşırsınız.' },
      { layout: 'text', eyebrow: 'SÜREÇ · 1', title: 'Keşif &amp; ihtiyaç analizi',
        text: 'Hedef pazarınızı ve marka hedeflerinizi birlikte netleştiririz.' },
      { layout: 'text', eyebrow: 'SÜREÇ · 2', title: 'Marka &amp; tema kurulumu',
        text: 'Logo, renk paleti ve arayüz teması markanıza göre uyarlanır.' },
      { layout: 'text', eyebrow: 'SÜREÇ · 3', title: 'Entegrasyon &amp; test',
        text: 'Ödeme, sağlayıcı ve uyumluluk kontrolleri uçtan uca test edilir.' },
      { layout: 'text', eyebrow: 'SÜREÇ · 4', title: 'Canlı yayın &amp; büyüme',
        text: 'Yayın sonrası performans takibi ve yol haritası birlikte yürütülür.' },
      { layout: 'text', eyebrow: 'GÜVEN', title: 'Güven, sonradan eklenen bir katman değildir',
        text: 'Risk skorlama ve işlem izleme, platformun ilk günden temelidir.' },
      { layout: 'showcase', eyebrow: 'VAKA 01', title: 'Kripto odaklı marka, günler içinde yayında', image: IMG.wVipGambler },
      { layout: 'showcase', eyebrow: 'VAKA 02', title: 'Premium/VIP marka, ilk günden aktif', video: VID.vSlot },
      { layout: 'showcase', eyebrow: 'VAKA 03', title: 'Yeni kitle, haftalar içinde yeni marka', image: IMG.wHorseRace }
    ],

    diamonds: [
      { layout: 'text', rank: 'ace', eyebrow: 'TEKNOLOJİ', title: 'İddia değil, çalışan ürün.',
        text: 'Aşağıdaki kartlarda gördükleriniz bu altyapı üzerinde gerçekten çalışan bir platformdan alınmıştır.' },
      { layout: 'text', eyebrow: 'MİMARİ', title: 'Modern frontend mimarisi',
        text: 'Bileşen tabanlı, sunucu tarafı render destekli yapı — hızlı ilk yükleme, akıcı gezinme.' },
      { layout: 'text', eyebrow: 'MİMARİ', title: 'Mikroservis gerçek zamanlı katman',
        text: 'Sohbet, bonus yağmuru ve canlı kazanç bağımsız servislerde ölçeklenir.' },
      { layout: 'text', eyebrow: 'MİMARİ', title: 'Redis tabanlı önbellekleme',
        text: 'Oyun listeleri önbelleklenir; sağlayıcı uçlarına tekrarlayan yük bindirilmez.' },
      { layout: 'text', eyebrow: 'MİMARİ', title: 'Gözlemlenebilirlik',
        text: 'Kritik uç noktalarda performans izleme, erken uyarı için temel metrikler.' },
      { layout: 'text', eyebrow: 'MİMARİ', title: 'Katmanlı güvenlik',
        text: 'Kimlik doğrulama ve risk skorlaması farklı katmanlarda ayrı uygulanır.' },
      { layout: 'text', eyebrow: 'ENTEGRASYON', title: 'API öncelikli tasarım',
        text: 'Yeni bir marka, var olan servisleri bozmadan API sözleşmeleri üzerinden eklenir.',
        extra: '<pre style="background:#081712;border:1px solid var(--border);border-radius:8px;padding:9px;font-size:9.5px;line-height:1.5;overflow-x:auto;color:#e8e2cf;margin-top:9px">GET /v1/sportsbook/odds\n{ "odds": {"home":1.85,"draw":3.40,"away":4.10},\n  "latency_ms": 118 }</pre>' },
      { layout: 'text', eyebrow: 'İSTEK AKIŞI', title: 'İstekten ekrana dört katman',
        list: ['Arayüz — Next.js render motoru', 'API — route handler &amp; servis köprüsü', 'Önbellek — Redis hızlandırma', 'Sağlayıcı ağı — oyun &amp; oran'] },
      { layout: 'stat', value: '99.95%', label: 'Ortalama çalışma süresi' },
      { layout: 'stat', value: '120ms', label: 'Ortalama API yanıt süresi' },
      { layout: 'image-top', image: IMG.screenHome, eyebrow: 'GERÇEK PLATFORM', title: 'Anasayfa', text: 'Canlı çalışan LuckyLira platformunun anasayfası.' },
      { layout: 'image-top', image: IMG.screenCasino, eyebrow: 'GERÇEK PLATFORM', title: 'Casino lobisi', text: 'Akıllı kapak eşleştirme motoruyla binlerce başlık.' },
      { layout: 'image-top', image: IMG.screenSports, eyebrow: 'GERÇEK PLATFORM', title: 'Canlı spor ekranı', text: 'Gerçek zamanlı 1-X-2 akışı, gerçek maçlar üzerinde.' }
    ],

    clubs: [
      { layout: 'text', rank: 'ace', eyebrow: 'SONUÇLAR', title: 'Rakibiniz oranı güncellerken siz izlemeyin.',
        text: '30 dakikalık bir görüşmede platformu birlikte inceleyelim, pazarınıza özel planı çıkaralım.' },
      { layout: 'stat', value: '7+', label: 'Entegre içerik sağlayıcısı' },
      { layout: 'stat', value: '3+', label: 'Aynı altyapı üzerinde canlı marka' },
      { layout: 'text', eyebrow: 'SAĞLAYICI AĞI', title: 'Tek entegrasyon, tüm katalog',
        text: 'Operatörlerin haftalar harcadığı entegrasyonları tek bağlantıya indirdik.', extra: logoRow() },
      { layout: 'text', eyebrow: 'DEMO', title: 'Demo görüşmesinde neler var?',
        list: ['Canlı ortamda platform turu', 'Marka/tema olasılıklarının gösterimi', 'Devreye alma süresi ve plan'] },
      { layout: 'text', eyebrow: 'İLETİŞİM', title: 'Doğrudan ulaşın',
        text: 'E-posta: iletisim@gambgaming.com<br/>Telefon/WhatsApp: +90 (000) 000 00 00<br/>İstanbul, Türkiye' },
      { layout: 'form', eyebrow: 'ARANIYOR', title: 'En Hızlı Altyapıyı Arayan Operatörler',
        text: 'Ödül: sınırsız marka, 120ms\'nin altında oran, uykusuz bir teknik ekip. İzinizi bırakın, peşinize düşelim.' },
      { layout: 'text', eyebrow: 'GÜVENCE', title: 'Üç ayda bir performans gözden geçirmesi',
        text: 'Yayın sonrası durmuyoruz; büyüme hedeflerinize göre yol haritasını birlikte güncelliyoruz.' },
      { layout: 'text', eyebrow: 'SONUÇ', title: 'Bir sonraki büyüme hamleniz bir demo kadar yakın',
        text: 'Kendi marka kimliğinizi bu altyapı üzerinde nasıl hayata geçireceğimizi konuşalım.' },
      { layout: 'text', eyebrow: 'KARAR', title: 'Bekleyen operatör, pazar payı kaybeder',
        text: 'Her geçen hafta, rakibinizin bir adım daha öne geçmesi demektir.' },
      { layout: 'showcase', eyebrow: 'VİTRİN', title: 'Yüzleşme anı', image: IMG.wRoyalFlush },
      { layout: 'showcase', eyebrow: 'VİTRİN', title: 'Zaman daralıyor', image: IMG.wVipGambler },
      { layout: 'showcase', eyebrow: 'VİTRİN', title: 'Yola çıkma vakti', image: IMG.wSaloonHall }
    ]
  };

  var FULL_DECK = [{ layout: 'cover' }];
  SUITS.forEach(function (s) {
    SUIT_CARDS[s.key].forEach(function (c, i) {
      c.suitKey = s.key; c.suitSym = s.sym; c.suitColor = s.color; c.rank = c.rank || RANKS[i];
      FULL_DECK.push(c);
    });
  });

  var sectionFirstIndex = {};
  FULL_DECK.forEach(function (c, i) { if (c.suitKey && sectionFirstIndex[c.suitKey] === undefined) sectionFirstIndex[c.suitKey] = i; });

  /* ---------------- Kart şablonu ---------------- */
  function cardHTML(data, idx) {
    if (data.layout === 'cover') {
      return '<div class="ggcard" data-layout="cover"><div class="card-body"><div class="card-scroll">' +
        '<img class="cover-mark" src="assets/mark.svg" alt="" />' +
        '<div class="cover-word">GAMB <em>GAMING</em></div>' +
        '<p class="cover-tag">B2B iGaming altyapı sağlayıcısı.</p>' +
        '</div></div></div>';
    }
    var rankDisp = RANKS.indexOf(data.rank) !== -1 ? data.rank : (data.rank === 'ace' ? 'A' : data.rank);
    var corners = '<div class="card-corner tl"><span class="rank">' + rankDisp + '</span><span class="suit">' + data.suitSym + '</span></div>' +
                  '<div class="card-corner br"><span class="rank">' + rankDisp + '</span><span class="suit">' + data.suitSym + '</span></div>';
    var watermark = '<div class="card-watermark">' + data.suitSym + '</div>';
    var tagHtml = data.eyebrow ? '<span class="card-eyebrow">' + data.eyebrow + '</span>' : '';
    var textHtml = data.text ? '<p class="card-text">' + data.text + '</p>' : '';
    var listHtml = data.list ? list(data.list) : '';
    var extraHtml = data.extra || '';
    var body = '';

    if (data.layout === 'showcase') {
      var showcaseMedia = data.video
        ? '<div class="card-media"><video src="' + data.video + '" autoplay loop muted playsinline preload="metadata"></video></div>'
        : data.image
        ? '<div class="card-media"><img src="' + data.image + '" alt="" loading="lazy" /></div>'
        : '<div class="card-media is-placeholder"><span class="ph-badge">GÖRSEL — ' + data.placeholder + '</span></div>';
      body = showcaseMedia +
        '<div class="card-scroll">' + tagHtml + '<h3 class="card-title">' + data.title + '</h3></div>';
    } else if (data.layout === 'image-top' || data.layout === 'image-bottom') {
      var media = '<div class="card-media"><img src="' + data.image + '" alt="" loading="lazy" /></div>';
      var txt = '<div class="card-scroll">' + tagHtml + '<h3 class="card-title">' + data.title + '</h3>' + textHtml + '</div>';
      body = media + txt;
    } else if (data.layout === 'stat') {
      body = '<div class="card-scroll"><div class="stat-num">' + data.value + '</div><div class="stat-label">' + data.label + '</div>' + westernDeco(idx) + '</div>';
    } else if (data.layout === 'form') {
      var dayOptions = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        .map(function (d) { return '<option value="' + d + '">' + d + '</option>'; }).join('');
      body = '<div class="card-scroll wanted-scroll">' +
        wicon('hat', 'wicon-tl') + wicon('cactus', 'wicon-br') +
        '<div class="wanted-stamp">' + wicon('revolver') + wicon('bullet') + wicon('bullet') + '</div>' +
        '<span class="card-eyebrow wanted-eyebrow">' + data.eyebrow + '</span>' +
        '<h3 class="card-title wanted-title">' + data.title + '</h3>' +
        '<p class="card-text wanted-text">' + data.text + '</p>' +
        '<form data-contact-form data-contact-email="iletisim@gambgaming.com">' +
        '<div class="card-field"><label>Ad Soyad</label><input name="name" type="text" required /></div>' +
        '<div class="field-row-2">' +
        '<div class="card-field"><label>İş E-postası</label><input name="email" type="email" required /></div>' +
        '<div class="card-field"><label>Telegram / WhatsApp</label><input name="contact_channel" type="text" placeholder="@kullanici ya da +90…" /></div>' +
        '</div>' +
        '<div class="card-field"><label>Mesaj</label><textarea name="message" rows="2" required></textarea></div>' +
        '<div class="field-row-2">' +
        '<div class="card-field"><label>Tercih Edilen Gün</label><select name="day"><option value="">Seçiniz…</option>' + dayOptions + '</select></div>' +
        '<div class="card-field"><label>Saat</label><input name="time" type="time" /></div>' +
        '</div>' +
        '<button class="card-btn wanted-btn" type="submit">Demo Talebini Gönder</button>' +
        '<p class="form-status" style="font-size:10px;color:var(--text-faint);margin-top:6px"></p>' +
        '</form></div>';
    } else {
      body = '<div class="card-scroll">' + tagHtml + '<h3 class="card-title">' + data.title + '</h3>' + textHtml + listHtml + extraHtml + westernDeco(idx) + '</div>';
    }

    return '<div class="ggcard" data-layout="' + data.layout + '" data-suit-color="' + data.suitColor + '" data-rank="' + data.rank + '">' + corners + watermark + '<div class="card-body">' + body + '</div></div>';
  }

  /* ---------------- Motor ---------------- */
  var row = document.getElementById('cardRow');
  var idxLabel = document.getElementById('cardIdx');
  var progressFill = document.getElementById('progressFill');
  var current = 0;
  var animating = false;

  /* before/after: ön karttan geriye (zaten görülmüş, solda) ve ileriye
     (sırada, sağda) kaç kart daha gösterilecek — masaüstünde iki yönde de
     yığın olsun diye simetrik. */
  function visibleRange() {
    var w = window.innerWidth;
    if (w <= 860) return { before: 0, after: 0 };
    if (w <= 1150) return { before: 0, after: 2 };
    if (w <= 1500) return { before: 1, after: 2 };
    return { before: 2, after: 2 };
  }

  function wireCard(wrapEl, data) {
    if (data.layout === 'form') {
      var form = wrapEl.querySelector('[data-contact-form]');
      if (form) {
        form.addEventListener('submit', function (e) {
          e.preventDefault();
          var fd = new FormData(form);
          var to = form.getAttribute('data-contact-email');
          var subject = encodeURIComponent('Demo talebi — ' + (fd.get('name') || ''));
          var lines = [
            'Ad: ' + (fd.get('name') || ''),
            'İş E-postası: ' + (fd.get('email') || ''),
            'Telegram/WhatsApp: ' + (fd.get('contact_channel') || '—'),
            'Tercih Edilen Gün/Saat: ' + (fd.get('day') || '—') + ' ' + (fd.get('time') || '')
          ];
          var body = encodeURIComponent(lines.join('\n') + '\n\n' + (fd.get('message') || ''));
          window.location.href = 'mailto:' + to + '?subject=' + subject + '&body=' + body;
          var status = form.querySelector('.form-status');
          if (status) status.textContent = 'E-posta uygulamanız açılıyor…';
        });
      }
    }
  }

  /* ---------------- Geçiş efektleri (rulet / aviator / kart açma / kart sayma / 21 / 777 / bonus) ----------------
     Tamamen kozmetik ve pointer-events:none — kartların gerçek durumunu asla
     etkilemez, bu yüzden temizliği basit bir setTimeout ile yapmak güvenli. */
  var fxLayer = document.getElementById('fxLayer');
  var reducedMotionMQ = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)');

  /* Sentezlenmiş efekt sesleri — dış ses dosyası yok, Web Audio ile anlık
     üretiliyor. İlk kullanıcı dokunuşunda AudioContext kilidi açılıyor
     (mobil tarayıcıların otomatik ses politikası gereği). */
  var audioCtx = null;
  function ensureAudio() {
    if (audioCtx) return audioCtx;
    try {
      var Ctx = window.AudioContext || window.webkitAudioContext;
      if (!Ctx) return null;
      audioCtx = new Ctx();
    } catch (e) { return null; }
    return audioCtx;
  }
  document.addEventListener('pointerdown', function unlockAudio() {
    var ctx = ensureAudio();
    if (ctx && ctx.state === 'suspended') ctx.resume();
  }, { once: true, passive: true });

  function beep(freq, dur, type, delay, peak) {
    var ctx = ensureAudio();
    if (!ctx) return;
    var t0 = ctx.currentTime + (delay || 0);
    var osc = ctx.createOscillator();
    var gain = ctx.createGain();
    osc.type = type || 'sine';
    osc.frequency.setValueAtTime(freq, t0);
    gain.gain.setValueAtTime(0, t0);
    gain.gain.linearRampToValueAtTime(peak || 0.16, t0 + 0.02);
    gain.gain.exponentialRampToValueAtTime(0.0001, t0 + (dur || 0.2));
    osc.connect(gain); gain.connect(ctx.destination);
    osc.start(t0); osc.stop(t0 + (dur || 0.2) + 0.05);
  }
  function sweep(f0, f1, dur, type, peak) {
    var ctx = ensureAudio();
    if (!ctx) return;
    var t0 = ctx.currentTime;
    var osc = ctx.createOscillator();
    var gain = ctx.createGain();
    osc.type = type || 'sine';
    osc.frequency.setValueAtTime(f0, t0);
    osc.frequency.exponentialRampToValueAtTime(Math.max(f1, 1), t0 + dur);
    gain.gain.setValueAtTime(0, t0);
    gain.gain.linearRampToValueAtTime(peak || 0.14, t0 + 0.03);
    gain.gain.exponentialRampToValueAtTime(0.0001, t0 + dur);
    osc.connect(gain); gain.connect(ctx.destination);
    osc.start(t0); osc.stop(t0 + dur + 0.05);
  }
  var FX_SOUND = {
    roulette: function () { sweep(760, 170, 1.1, 'triangle'); },
    aviator: function () { sweep(260, 1000, 0.9, 'sawtooth', .09); },
    reveal: function () { [0, .12, .24, .36, .48].forEach(function (d, i) { beep(520 + i * 40, .12, 'triangle', d, .14); }); },
    slot: function () { [0, .08, .16].forEach(function (d, i) { beep(300 + i * 160, .14, 'square', d, .1); }); beep(880, .25, 'sine', .3, .16); },
    bonus: function () { [523, 659, 784, 1046].forEach(function (f, i) { beep(f, .22, 'sine', i * .08, .16); }); },
    count: function () { [0, .1, .2, .3, .4].forEach(function (d, i) { beep(440 + i * 30, .08, 'square', d, .1); }); },
    blackjack: function () { beep(392, .15, 'triangle', 0, .14); beep(587, .22, 'triangle', .15, .16); },
    sevens: function () { [784, 784, 784].forEach(function (f, i) { beep(f, .18, 'square', i * .14, .18); }); beep(1568, .3, 'sine', .42, .14); }
  };
  function playHaptic() {
    if (navigator.vibrate) { try { navigator.vibrate([25, 40, 60]); } catch (e) {} }
  }

  var SUITS_FOR_PIPS = ['♠', '♥', '♦', '♣'];
  function fxRoulette() {
    return '<div class="fx fx-roulette"><svg viewBox="0 0 100 100">' +
      '<circle cx="50" cy="50" r="44" fill="none" stroke="var(--border)" stroke-width="3"/>' +
      '<g class="rl-spin">' +
      Array.from({ length: 10 }).map(function (_, i) {
        var a = i * 36;
        return '<rect x="48" y="8" width="4" height="16" fill="' + (i % 2 ? 'var(--accent)' : 'var(--paper)') + '" transform="rotate(' + a + ' 50 50)"/>';
      }).join('') + '</g>' +
      '<g class="rl-ball"><circle cx="50" cy="12" r="4" fill="var(--text)"/></g>' +
      '<circle cx="50" cy="50" r="7" fill="var(--accent)"/></svg></div>' +
      '<div class="fx-caption">RULET ÇEVRİLİYOR…</div>';
  }
  function fxAviator() {
    return '<div class="fx fx-aviator"><span class="av-trail"></span><svg viewBox="0 0 24 24" fill="currentColor"><path d="M22,12 L14,9 L8,2 L6,2.5 L9,9.5 L3,9.5 L1,7 L0,7.3 L1.3,11 L0,14.7 L1,15 L3,12.5 L9,12.5 L6,19.5 L8,20 L14,13 Z"/></svg></div>' +
      '<div class="fx-caption">AVIATOR UÇUYOR…</div>';
  }
  function fxReveal() {
    return '<div class="fx fx-reveal">' + SUITS_FOR_PIPS.concat(['A']).map(function (s, i) {
      return '<div class="pk-card" style="animation-delay:' + (i * .13) + 's">' + (s === 'A' ? 'A' : s) + '</div>';
    }).join('') + '</div><div class="fx-caption">KARTLAR AÇILIYOR…</div>';
  }
  function fxCount() {
    var steps = ['+2', '+4', '+7', '+10', '+13'];
    return '<div class="fx fx-count"><div class="ct-track">' + steps.map(function (s, i) {
      return '<span class="ct-step" style="animation-delay:' + (i * .14) + 's">' + s + '</span>';
    }).join('') + '</div><div class="fx-caption">KART SAYILIYOR…</div></div>';
  }
  function fxBlackjack() {
    return '<div class="fx fx-blackjack"><div class="bj-cards">' +
      '<div class="bj-card">A<span>♠</span></div><div class="bj-card" style="animation-delay:.15s">K<span>♥</span></div>' +
      '</div><div class="bj-num">21</div></div>';
  }
  function fxSevens() {
    return '<div class="fx fx-sevens"><span class="sv-seven">7</span><span class="sv-seven">7</span><span class="sv-seven">7</span></div>' +
      '<div class="fx-caption">JACKPOT 777!</div>';
  }
  function fxBonus() {
    var msgs = ['FREE BONUS!', 'ŞANS DÖNÜYOR!', 'JACKPOT YOLDA!'];
    return '<div class="fx fx-bonus">' + msgs[Math.floor(Math.random() * msgs.length)] + '</div>';
  }
  var FX_LIST = [
    { build: fxRoulette, sound: 'roulette' },
    { build: fxAviator, sound: 'aviator' },
    { build: fxReveal, sound: 'reveal' },
    { build: fxCount, sound: 'count' },
    { build: fxBlackjack, sound: 'blackjack' },
    { build: fxSevens, sound: 'sevens' },
    { build: fxBonus, sound: 'bonus' }
  ];

  var fxTimer = null;
  function clearFx() {
    if (fxTimer) { clearTimeout(fxTimer); fxTimer = null; }
    fxLayer.innerHTML = '';
    fxLayer.classList.remove('is-active');
  }
  function maybePlayFx() {
    if (!fxLayer || (reducedMotionMQ && reducedMotionMQ.matches)) return;
    if (Math.random() > 0.4) return; /* her geçişte değil, ~%40 ihtimalle */
    clearFx();
    var pick = FX_LIST[Math.floor(Math.random() * FX_LIST.length)];
    var dim = document.createElement('div');
    dim.className = 'fx-dim';
    var wrap = document.createElement('div');
    wrap.innerHTML = pick.build();
    fxLayer.appendChild(dim);
    fxLayer.appendChild(wrap);
    fxLayer.classList.add('is-active');
    if (FX_SOUND[pick.sound]) FX_SOUND[pick.sound]();
    playHaptic();
    fxTimer = setTimeout(clearFx, 1500);
  }
  if (fxLayer) fxLayer.addEventListener('click', clearFx);

  function buildSlot(idx, pos) {
    var wrap = document.createElement('div');
    wrap.className = 'card-slot';
    wrap.setAttribute('data-pos', pos);
    wrap.setAttribute('data-idx', idx);
    wrap.innerHTML = cardHTML(FULL_DECK[idx], idx);
    wireCard(wrap, FULL_DECK[idx]);
    if (pos === 0) attachDrag(wrap);
    return wrap;
  }

  function renderFull(newCurrent) {
    row.innerHTML = '';
    var range = visibleRange();
    var from = Math.max(0, newCurrent - range.before);
    var to = Math.min(FULL_DECK.length - 1, newCurrent + range.after);
    for (var idx = from; idx <= to; idx++) {
      row.appendChild(buildSlot(idx, idx - newCurrent));
    }
    current = newCurrent;
    updateChrome();
  }

  /*
   * Not: Her geçişte satır sıfırdan, tamamen deterministik şekilde yeniden
   * kuruluyor (renderFull); uçup giden kart ayrı/bağımsız bir "hayalet"
   * olarak sahneye ekleniyor, satırın kendisiyle hiç etkileşmiyor — rAF'a
   * veya elle data-pos azaltmaya güvenmediği için kart birikmesi imkansız.
   */
  function advance(dir, flyDir) {
    if (animating) return;
    var newCurrent = current + dir;
    if (newCurrent < 0 || newCurrent >= FULL_DECK.length) return;
    animating = true;

    if (dir === 1) {
      var front = row.querySelector('.card-slot[data-pos="0"]');
      if (front) {
        /* FLIP tekniği: yeniden ebeveynlemeden (reparent) önce ekrandaki
           gerçek konumunu ölç, sonra o konuma sabitleyerek aynı yerde
           "donmuş" gibi bırak — aksi halde flex satırından çıkınca aniden
           zıplar, uçuş animasyonu o zıplamanın üstüne biner ve kopuk görünür. */
        var r = front.getBoundingClientRect();
        row.removeChild(front);
        var stage = document.querySelector('.deck-stage');
        stage.appendChild(front);
        front.classList.remove('is-dragging');
        front.style.position = 'fixed';
        front.style.left = r.left + 'px';
        front.style.top = r.top + 'px';
        front.style.width = r.width + 'px';
        front.style.height = r.height + 'px';
        front.style.margin = '0';
        void front.offsetWidth; /* reflow'u zorla, böylece asagidaki sinif animasyonu "from" karesini doğru alır */
        front.classList.add(flyDir === 'right' ? 'fly-right' : 'fly-left');
        var cleaned = false;
        var cleanup = function () { if (cleaned) return; cleaned = true; if (front.parentNode) front.parentNode.removeChild(front); };
        front.addEventListener('animationend', cleanup, { once: true });
        setTimeout(cleanup, 650);
      }
    }
    renderFull(newCurrent);
    maybePlayFx();
    setTimeout(function () { animating = false; }, 420);
  }

  function next() { advance(1, 'left'); }
  function prev() {
    if (animating || current === 0) return;
    animating = true;
    renderFull(current - 1);
    maybePlayFx();
    setTimeout(function () { animating = false; }, 420);
  }
  function goTo(targetIdx) {
    if (targetIdx === current || animating) return;
    animating = true;
    renderFull(targetIdx);
    document.body.classList.remove('menu-open');
    setTimeout(function () { animating = false; }, 420);
  }

  function updateChrome() {
    if (idxLabel) idxLabel.textContent = current === 0 ? 'kapak' : current;
    if (progressFill) progressFill.style.width = (current / (FULL_DECK.length - 1) * 100) + '%';
    var cur = FULL_DECK[current];
    var suitKey = cur.suitKey || 'spades';
    document.body.setAttribute('data-suit', suitKey);
    var launcherDot = document.querySelector('.deck-menu-launcher .launcher-dot');
    if (launcherDot && cur.suitSym) launcherDot.textContent = cur.suitSym;
    document.querySelectorAll('.deck-menu-item').forEach(function (el) {
      el.classList.toggle('is-active', el.getAttribute('data-section') === suitKey);
    });
    var upBtn = document.querySelector('.deck-arrow.up');
    var downBtn = document.querySelector('.deck-arrow.down');
    if (upBtn) upBtn.disabled = current === 0;
    if (downBtn) downBtn.disabled = current === FULL_DECK.length - 1;
  }

  /* ---------------- Sürükle-at (drag-to-throw) ---------------- */
  function attachDrag(el) {
    var startX = 0, startY = 0, dx = 0, dy = 0, dragging = false, committed = null;
    el.style.touchAction = 'pan-y';
    function pos(e) { return e.touches ? { x: e.touches[0].clientX, y: e.touches[0].clientY } : { x: e.clientX, y: e.clientY }; }
    function down(e) {
      dragging = true; committed = null; dx = 0; dy = 0;
      var p = pos(e); startX = p.x; startY = p.y;
      el.classList.add('is-dragging');
      try { el.setPointerCapture && e.pointerId !== undefined && el.setPointerCapture(e.pointerId); } catch (ignored) {}
    }
    function move(e) {
      if (!dragging) return;
      var p = pos(e); dx = p.x - startX; dy = p.y - startY;
      if (committed === null && (Math.abs(dx) > 8 || Math.abs(dy) > 8)) committed = Math.abs(dx) > Math.abs(dy) ? 'h' : 'v';
      if (committed === 'v') return;
      if (e.cancelable) e.preventDefault();
      el.style.transform = 'translate(' + dx + 'px,' + (dy * .12) + 'px) rotate(' + (dx / 16) + 'deg)';
    }
    function up() {
      if (!dragging) return;
      dragging = false; el.classList.remove('is-dragging');
      if (committed === 'h' && Math.abs(dx) > 100 && !animating) {
        /* Kartın kendi anlık sürüklenme konumundan devam etmesi için, uçuş
           animasyonu BAŞLAMADAN önce mevcut translate/rotate'i CSS değişkenine
           aktarıyoruz (@keyframes `from` bunu okuyacak) — aksi halde kart
           önce merkeze zıplayıp sonra uçardı. */
        el.style.setProperty('--dragx', dx + 'px');
        el.style.setProperty('--dragrot', (dx / 16) + 'deg');
        el.style.transform = '';
        advance(1, dx < 0 ? 'left' : 'right');
      } else {
        el.style.transform = '';
      }
    }
    el.addEventListener('pointerdown', down);
    el.addEventListener('pointermove', move);
    el.addEventListener('pointerup', up);
    el.addEventListener('pointercancel', up);
  }

  /* ---------------- Jest kontrolleri (wheel / klavye) ---------------- */
  var wheelLock = false;
  document.querySelector('.deck-stage').addEventListener('wheel', function (e) {
    e.preventDefault();
    if (wheelLock || Math.abs(e.deltaY) < 12) return;
    wheelLock = true;
    if (e.deltaY > 0) next(); else prev();
    setTimeout(function () { wheelLock = false; }, 550);
  }, { passive: false });

  document.addEventListener('keydown', function (e) {
    if (['ArrowDown', 'ArrowRight', 'PageDown'].indexOf(e.key) !== -1) { e.preventDefault(); next(); }
    else if (['ArrowUp', 'ArrowLeft', 'PageUp'].indexOf(e.key) !== -1) { e.preventDefault(); prev(); }
  });

  var resizeT;
  window.addEventListener('resize', function () {
    clearTimeout(resizeT);
    resizeT = setTimeout(function () { renderFull(current); }, 200);
  });

  /* ---------------- Menü / CTA ---------------- */
  document.querySelectorAll('.deck-menu-item').forEach(function (el) {
    el.addEventListener('click', function () { goTo(sectionFirstIndex[el.getAttribute('data-section')]); });
  });
  var launcher = document.querySelector('.deck-menu-launcher');
  if (launcher) launcher.addEventListener('click', function () { document.body.classList.toggle('menu-open'); });
  var upArrow = document.querySelector('.deck-arrow.up');
  var downArrow = document.querySelector('.deck-arrow.down');
  if (upArrow) upArrow.addEventListener('click', prev);
  if (downArrow) downArrow.addEventListener('click', next);
  var tapPrev = document.querySelector('.tap-zone.tap-prev');
  var tapNext = document.querySelector('.tap-zone.tap-next');
  if (tapPrev) tapPrev.addEventListener('click', prev);
  if (tapNext) tapNext.addEventListener('click', next);
  var stickyCta = document.querySelector('.sticky-cta');
  if (stickyCta) stickyCta.addEventListener('click', function () { goTo(sectionFirstIndex.clubs + 6); });

  renderFull(0);
})();
