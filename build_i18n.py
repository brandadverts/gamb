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
    12: "assets/img/screen-home.jpg", 14: G("9B7XwCQZRQfQs"), 15: G("jpijmSzW2RlaBMKQG6"), 16: "assets/video/roulette-spin.mp4",
    17: G("2YHdXovMSv1NtO6V4n"), 18: G("l46CbPpL3szntVNhS"), 19: G("xT9DPQFUrS0gPc2pyg"), 20: G("GWS8bXKxphfEI"),
    21: G("VJNOiHIekI4B1ALVfA"), 22: G("1DEJwfwdknKZq"), 23: G("CKGggZ7Q90ro4MteO2"), 24: "assets/img/stadium.jpg",
    25: G("0mkK0hzJmL69KInkIZ"), 27: G("lZTvTGEGKU6gnQ2wBr"), 28: G("Ce18KspdcaxaKuZ1HC"), 29: G("BfFFYPSVYr9UR6EtEL"),
    30: G("SdMY3KVYI8mSVz7StH"), 31: G("lXiRm5H49zYmHr3i0"), 32: G("Pk9ux7yJBXKF9CIpg5"), 33: "assets/img/birthday.jpg",
    34: G("qlotpC5nKBnzyBXJea"), 35: "assets/img/sports-racing.jpg", 36: "assets/img/screen-casino.jpg", 37: G("mi6DsSSNKDbUY"),
    38: "assets/img/royal-flush.jpg", 40: G("3ov9jUCYetT3GVwcy4"), 41: G("4ZFWCCSVg8K3RV89xW"), 42: G("VQXzKQKI9yvbrjrKZ1"),
    43: G("13I3peucbA8BfG"), 44: G("OE9hKAfUkurx44b5cE"), 45: G("TiDqYW1SQiA38RgoyY"), 46: G("PqjTdvXImZQfcmTYEO"),
    47: G("7UchwDJiYXiLzuRvEy"), 48: G("qTYW0EfwoAbrG"), 49: G("l4FGJM0LG9UMc0ZMI"), 50: G("3Gm15eZOsNk0tptIuG"),
    51: "assets/img/saloon-hall.jpg",
}
for v in media.values():
    assert os.path.exists(os.path.join(ROOT, v)), v
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
js = rep(js, "function ye(){`vibrate`in navigator&&navigator.vibrate([60,40,60,40,140,60,260])}", "function ye(){}", 1, "overlay vibrate off")

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
TE_TR = {
 1: ["Platform Mimarisi","Tek Motor. Batı'daki Her Masa.","Spor bahis, casino ve ödeme çekirdeği; tek sözleşmeyle devreye alınan modüler bir yığın.","Spor bahis, casino ve cüzdan tek defterde","Pazara göre açıp kapattığınız modüler servisler","Her şey için tek operatör arka ofisi"],
 2: ["Spor Bahis Motoru","120 ms. Ya Kupon Girer, Ya Kaçar.","Eski platformlar 400-800 ms gecikmede tıkanırken Gamb Gaming'in Redis önbellekli oran motoru sahadaki değişimi 120 ms'nin altında oyuncu kuponuna yansıtır.","Maç öncesi ve canlı bahis tek akışta","Büyük maç başına 2.000'den fazla bahis pazarı","API üzerinden anlık marj ayarı"],
 3: ["Canlı Kupon","Gözünü Kırpmayan Kupon.","Tekli, kombine ve sistem bahisleri; canlı oran değişimi onayı ve tek dokunuşla nakit çıkışı.","Korelasyonlu fiyatlamayla bahis kurucu","Tam ve kısmi nakit çıkışı","Yenileme olmadan oran değişimi yönetimi"],
 4: ["White-Label","Sınırsız Marka. Tek Kurulum.","Alan adı, tema, para birimi, lisans ve ödeme karmasıyla tam donanımlı bir markayı günler içinde açın.","Marka bazında tema ve CMS","Çoklu para birimi ve çoklu lisans","Ortak likidite, ayrı defterler"],
 5: ["Casino Toplayıcı","7+ Birinci Sınıf Sağlayıcı. Tek Entegrasyon.","Binlerce slot ve canlı masa tek API üzerinden; bonus ve raporlama tek çatıda.","Slot, canlı krupiye ve anlık oyunlar","Birleşik free-spin ve bonus motoru","Sağlayıcı bazında GGR raporu"],
 6: ["Cüzdan ve Ödemeler","Para, Alev Almış Posta Arabası Gibi Akar.","Fiat, kart, açık bankacılık ve kripto kanalları tek defterin arkasında; mutabakat otomatik.","Açmaya hazır 40+ ödeme yöntemi","Daha yüksek onay için akıllı yönlendirme","Anında ödeme kuralları ve limitler"],
 7: ["Bonus Motoru","Akıllı Bonuslar.","Kural tabanlı hoş geldin, yeniden yükleme, cashback ve bedava bahis kampanyaları; çevrim kontrolü dahil.","Dakikalar içinde segmentli kampanya","Suistimal ve bonus avcısı tespiti","Kampanya başına canlı ROI"],
 8: ["Arka Ofis","Şerifin Masası.","Oyuncu, pazar, limit, içerik ve finans tek konsoldan, rol bazlı yetkiyle yönetilir.","Ayrıntılı roller ve denetim izleri","Pazar ve limit kontrolleri","Toplu işlem ve kayıtlı görünümler"],
 9: ["Raporlama ve BI","Her Kuruşu Gün Doğmadan Bilin.","Gerçek zamanlı GGR, NGR, tutma ve kohort raporları; veri ambarına dışa aktarım.","Marka ve pazar bazında canlı panolar","Gelen kutusuna zamanlanmış raporlar","BigQuery ve Snowflake dışa aktarımı"],
 10: ["Risk Motoru","Akıllı Oyna. Köpekbalıklarını Yakala.","Otomatik limitler, oyuncu profilleme ve yükümlülük yönetimi marjınızı korur.","Oyuncu bazında bahis limitleri","Pazar bazında yükümlülük izleme","Anlık trader uyarıları"],
 11: ["KYC ve Uyum","Belgeler Lütfen. Nezaketle.","Entegre kimlik doğrulama, AML taraması ve sorumlu oyun araçları.","Belge ve canlılık kontrolleri","Yaptırım ve PEP taraması","Yatırım limitleri ve kendini dışlama"],
 12: ["Yerelleştirme","Her Sınırın Dilini Konuşun.","Diller, oran formatları, para birimleri ve bölgesel içerik kutudan çıktığı gibi hazır.","30+ dil","Ondalık, kesirli ve Amerikan oranlar","Pazara özel bölgesel promosyonlar"],
 13: ["Maça Papazı","Platform Sizin Tacınız.","Bir pazara hükmetmek için operatörün ihtiyaç duyduğu her şey, savaşta sınanmış tek bir yığın olarak.","","",""],
 14: ["Altyapı","Uçsuz Bucaksız Ovalar Gibi Ölçeklenin.","Otomatik ölçeklenen Kubernetes kümeleri bir cumartesi finalini ter dökmeden kaldırır.","Yatay pod otomatik ölçekleme","Çok bölgeli aktif-aktif","50 kat trafik sıçraması sorunsuz"],
 15: ["Güvenlik","Sıfır Güven. Sıfır Bahane.","Her servis, kullanıcı ve istek doğrulanır. Hiçbir şeye geldiği yere bakılarak güvenilmez.","Servisler arası mTLS","Donanım destekli gizli anahtar deposu","Yıllık bağımsız sızma testleri"],
 16: ["Gerçek Zamanlı","WebSocket Üzerinden Canlı Akış.","Oranlar, skorlar ve bakiyeler değiştiği anda tarayıcıya itilir.","50 ms altı dağıtım","Otomatik yeniden bağlanma ve tekrar oynatma","Milyonlarca eşzamanlı soket"],
 17: ["Mimari","Mikroservis, Kargaşa Değil.","Net sözleşmeli bağımsız servisler; tek bir arıza asla salonu kapatmaz.","Kafka ile olay güdümlü","Her gün bağımsız dağıtım","Varsayılan olarak devre kesiciler"],
 18: ["Adil Oyun","Kanıtlanabilir Adil. Kanıtlanabilir Sizin.","Kriptografik tohumlarla her oyuncu, özgün oyunlarımızın her sonucunu doğrulayabilir.","HMAC-SHA256 tohum taahhütleri","Herkese açık doğrulama aracı","Bağımsız denetim raporları"],
 19: ["Geliştiriciler","Önce API. Dokümantasyon Dahil.","Her entegrasyon noktası için sandbox, webhook ve SDK'larla REST ve GraphQL API'leri.","OpenAPI şeması ve Postman seti","Yeniden denemeli imzalı webhook'lar","5 dakikada sandbox"],
 20: ["Güvenilirlik","%99,99 ve Sayaç Dönüyor.","Yedekli bölgeler, sağlık kontrolleri ve otomatik devralma defterlerinizi hep açık tutar.","Varsayılan olarak çoklu erişilebilirlik bölgesi","30 saniyenin altında otomatik devralma","Herkese açık durum sayfası"],
 21: ["Gözlemlenebilirlik","Her İzin Üzerinde Göz.","Metrikler, loglar ve izler ilişkilendirilir; olaylar oyuncu fark etmeden bulunur.","Dağıtık izleme","SLO tabanlı uyarılar","Operatöre açık sağlık görünümü"],
 22: ["Veri","Uzun Ömürlü Bir Boru Hattı.","Akış tabanlı olay hattı; analitik, CRM ve riski üretime dokunmadan besler.","Change-data-capture akışları","Dakika altı ambar gecikmesi","Gizlilik odaklı veri maskeleme"],
 23: ["Dolandırıcılık Tespiti","Haydutların Peşine Düşün.","Cihaz parmak izi ve davranış modelleri çoklu hesap ve bonus suistimalini erkenden yakalar.","Cihaz ve ağ puanlama","Ödeme dolandırıcılığı sinyalleri","Manuel inceleme kuyruğu"],
 24: ["Uç Nokta","Her Oyuncuya Yakın.","Küresel CDN ve uç önbellekleme sayesinde lobi Lagos'tan Lima'ya hızla açılır.","Uçta önbelleklenen statik ve API okumaları","DDoS koruması dahil","1,2 saniyenin altında medyan yükleme"],
 25: ["Dayanıklılık","Kötü Gün İçin Yedek.","Zaman noktasına geri dönüş ve prova edilmiş runbook'lar; kurtarma dakikalarla ölçülür.","1 dakikanın altında RPO","15 dakikanın altında RTO","Üç ayda bir kurtarma tatbikatı"],
 26: ["Sinek Papazı","Sınırları Aşacak Şekilde Kuruldu.","Büyümeniz asla bizimkini beklemesin diye tasarlanmış altyapı.","","",""],
 27: ["Oyuncu Tutma","Geri Dönen Oyuncular.","Tutma mekanikleri sonradan eklenmez; ürünün içine dokunur.","Görevler, seriler ve ödüller","Segment bazlı tetikleyiciler","Kontrol gruplarıyla ölçülen etki"],
 28: ["Sosyal Kanıt","Canlı Kazanç Şeridi.","Gerçek zamanlı kazanç akışı lobide güven ve aciliyet yaratır.","Ayarlanabilir eşikler","Gizliliğe uygun kullanıcı adları","Lobide dönüşümü artırır"],
 29: ["Topluluk","Yağmur Botları Para Yağdırır.","Sohbet ve Telegram botları aktif oyunculara programlı sürpriz ödüller bırakır.","Telegram ve uygulama içi sohbet","Dağıtım başına bütçe tavanı","Ölçülebilir etkileşim artışı"],
 30: ["VIP Programı","Büyük Mahmuzlara Kademeli Rakeback.","Bronz'dan Kanun Kaçağı'na kademeler; rakeback, VIP temsilcisi ve özel ayrıcalıklar.","Otomatik kademe ilerlemesi","Haftalık ve aylık rakeback","VIP temsilci araçları"],
 31: ["Oyunlaştırma","Peşinden Koşulacak Görevler.","Günlük ve haftalık görevler net hedef ve ödüllerle oyuncuyu geri getirir.","Kodsuz görev kurucu","Ürünler arası hedefler","Suistimale karşı korumalar"],
 32: ["Liderlik Tabloları","Silahı En Hızlı Kim Çekiyor?","Turnuvalar ve liderlik tabloları tek tek oyuncuları rekabetçi bir kasabaya dönüştürür.","Slot ve spor turnuvaları","Canlı sıralama güncellemeleri","Ödül havuzu otomasyonu"],
 33: ["CRM","Tam Öğle Vakti Doğru Mesaj.","E-posta, SMS, push ve WhatsApp üzerinden canlı davranışa göre yaşam döngüsü yolculukları.","Görsel yolculuk kurucu","Gerçek zamanlı segmentasyon","Onay ve sıklık sınırları"],
 34: ["Kanallar","Telegram ve WhatsApp'ta Yerli.","Oyuncularla zaten oldukları yerde buluşun: botlar, uyarılar ve tek dokunuşla yatırım.","Bot destekli kayıt","Kupon paylaşım bağlantıları","Temsilciye sorunsuz devir"],
 35: ["Büyüme","Referanslar Orman Yangını Gibi Yayılır.","Şeffaf, dolandırıcılık kontrollü takipli affiliate ve oyuncu referans programları.","Çok kademeli affiliate planları","Postback ve S2S takibi","Gerçek zamanlı ödemeler"],
 36: ["Vaka Çalışması","60 Günde 0'dan 10 Bin Oyuncuya.","Yeni bir operatör imzadan iki ayda on bin aktif oyuncuya ulaştı.","14 günde yayında","60. günde 10.000 oyuncu","30. günde %31 tutma"],
 37: ["Vaka Çalışması","Fethedilen Bir Pazar.","Aynı yığın ve aynı ekiple regüle bir pazarda ikinci marka açıldı.","İlk haftada yerel ödemeler","Yerelleştirilmiş spor bahis içeriği","Üçüncü ayda başabaş"],
 38: ["Yaşam Boyu Değer","Katlanarak Büyüyen Değer.","Kohort analitiği, oyuncu değerini zamanla gerçekten hangi kolların artırdığını gösterir.","Kanal ve kohort bazında LTV","Kayıp tahmini","Aksiyona dönüşen haftalık içgörüler"],
 39: ["Kupa Papazı","Gerçek İkramiye Sadakattir.","Oyuncular tanındıklarını hissettikleri yerde kalır. Onları tanımanız için araçları veriyoruz.","","",""],
 40: ["Anahtar Teslim Paketler","Elinizi Seçin.","Bugününüze ve yarınınıza göre boyutlandırılmış, dağıtıma hazır üç paket.","Starter, Growth ve Enterprise","Platform değiştirmeden yükseltme","Sabit devreye alma takvimi"],
 41: ["Starter Paketi","Starter. Hızla Eyerleyin.","İlk pazar için temel ödemeler ve uyumla markalı spor bahis ve casino.","Tek marka, tek lisans","Temel spor bahis ve casino","Standart destek"],
 42: ["Growth Paketi","Growth. Toprakları Genişletin.","Pazarlar arasında ölçeklenen operatörler için çoklu marka, CRM, VIP ve ileri risk.","5 markaya kadar","CRM, VIP ve bonus paketi","Özel başarı yöneticisi"],
 43: ["Enterprise Paketi","Enterprise. Sınıra Hükmedin.","Sınırsız marka, özel altyapı ve kurumsal SLA'larla özel entegrasyonlar.","Sınırsız marka","Size özel altyapı","7/24 öncelikli destek"],
 44: ["Özgün Oyunlar","Mines. Dikkatli Adım Atın.","Kanıtlanabilir adil sonuçlar ve ayarlanabilir kasa avantajıyla özgün ızgara oyunumuz.","Ayarlanabilir ızgara ve mayın sayısı","Kanıtlanabilir adil","İlk günden lobinizde"],
 45: ["Özgün Oyunlar","Plinko. Bırakın Düşsün.","Risk seviyeleri ve tatmin edici çarpanlarıyla fizik tadında bir favori.","Üç risk seviyesi","16 sıra yapılandırması","1.000x'e varan maksimum kazanç"],
 46: ["Özgün Oyunlar","Crash. Zamanında Çıkın.","Çarpan tırmanır, uçak uçar. Ne zaman atlayacağına oyuncu karar verir.","Canlı sosyal bahis turları","Otomatik nakit çıkışı kontrolleri","Tur geçmişi ve doğrulayıcı"],
 47: ["Oyun Stüdyosu","Size Özel Markalı Oyunlar.","Sizin sanatınız, sizin matematiğiniz, sizin mekaniklerinizle oyun sipariş edin.","Konseptten yayına 8 hafta","Özel IP seçenekleri","Sertifikalı matematik modelleri"],
 48: ["14 Günlük Yol Haritası","1-4. Gün: Alanı İşaretleyin.","Keşif, marka varlıkları, lisans eşlemesi ve ortam kurulumu.","Başlangıç ve kapsam kilidi","Marka ve alan adı kurulumu","Staging ortamı hazır"],
 49: ["14 Günlük Yol Haritası","5-9. Gün: Kasabayı Kurun.","Ödemeler, içerik, oyunlar ve arka ofis yapılandırması; entegrasyon testleri.","Ödemeler ve KYC testte canlı","Oyun ve içerik aktarımı","Ekibe arka ofis eğitimi"],
 50: ["14 Günlük Yol Haritası","10-14. Gün: Kapıları Açın.","Yük testi, uyum onayı ve gözetimli yumuşak açılış.","Yük ve güvenlik testleri","Uyum incelemesi","Yoğun destekle canlıya geçiş"],
 51: ["Destek","Çağrıya Hazır Bir Posse.","İsimleri belli mühendisler, net SLA'lar ve ekibinizle ortak bir kanal.","Ortak Slack veya Telegram kanalı","P1 yanıtı 15 dakikada","Üç aylık iş değerlendirmeleri"],
}
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

UI = [
    ("label:`Tech`", "label:`Teknoloji`", 1), ("label:`Why Us`", "label:`Neden Biz`", 1), ("label:`Solutions`", "label:`Çözümler`", 1),
    ("`✦ Provided By ✦`", "`✦ Karşınızda ✦`", 1),
    ("`The finest betting provider in the West`", "`Batı'nın en iyi bahis sağlayıcısı`", 1),
    ("`Reward: Unlimited Revenue`", "`Ödül: Sınırsız Gelir`", 1),
    ("`Dead or Alive — sub-120ms odds engine, unlimited white-label brands, and player retention mechanics built-in. Outlaw-grade technology the sheriff wouldn't dare mess with.`",
     "`Ölü ya da Diri — 120 ms altı oran motoru, sınırsız white-label marka ve ürüne gömülü oyuncu tutma mekanikleri. Şerifin bile bulaşmaya cesaret edemeyeceği kanun kaçağı teknoloji.`", 1),
    ("`Deal Yourself In ·`", "`Masaya Oturun ·`", 1), ("`Swipe to Claim ›`", "`Almak İçin Kaydırın ›`", 1),
    ("title:`CLAIM YOUR REWARD`", "title:`ÖDÜLÜNÜZÜ ALIN`", 1), ("children:`CLAIM YOUR REWARD`", "children:`ÖDÜLÜNÜZÜ ALIN`", 1),
    ("eyebrow:`King of Diamonds`", "eyebrow:`Karo Papazı`", 1),
    ("`Wanted: operators with big ambitions`", "`Aranıyor: büyük hedefleri olan operatörler`", 1),
    ("`A valid business email is required, partner.`", "`Geçerli bir kurumsal e-posta gerekli, ortak.`", 1),
    ("`Your email app should open with a pre-filled request. Send it to lock in the demo.`", "`E-posta uygulamanız önceden doldurulmuş taleple açılacak. Demoyu kesinleştirmek için gönderin.`", 1),
    ("`Demo request — `", "`Demo talebi — `", 1),
    ("`Company: ${", "`Şirket: ${", 1), ("`Email: ${", "`E-posta: ${", 1), ("`Preferred days: ${", "`Tercih edilen günler: ${", 1),
    ("`Preferred time: ${", "`Tercih edilen saat: ${", 1), ("`Platform requirements:`", "`Platform ihtiyaçları:`", 1),
    ("Fe=[`Mon`,`Tue`,`Wed`,`Thu`,`Fri`]", "Fe=[`Pzt`,`Sal`,`Çar`,`Per`,`Cum`]", 1),
    ("`☀️ Morning`", "`☀️ Sabah`", 1), ("`🌤 Afternoon`", "`🌤 Öğleden sonra`", 1), ("`🌙 Evening`", "`🌙 Akşam`", 1),
    ("`Business email *`", "`Kurumsal e-posta *`", 1), ("`Business email`", "`Kurumsal e-posta`", 1),
    ("`Telegram @handle or WhatsApp number`", "`Telegram kullanıcı adı veya WhatsApp numarası`", 1), ("`Telegram or WhatsApp`", "`Telegram veya WhatsApp`", 1),
    ("`Company / syndicate name`", "`Şirket / grup adı`", 1), ("`Company`", "`Şirket`", 1),
    ("`Platform requirements`", "`Platform ihtiyaçlarınız`", 2),
    ("`Preferred days`", "`Tercih edilen günler`", 1), ("`Select days`", "`Gün seçin`", 1), ("`Preferred time slot`", "`Tercih edilen saat aralığı`", 1),
    ("`🔫 CLAIM YOUR REWARD — SCHEDULE DEMO`", "`🔫 ÖDÜLÜNÜZÜ ALIN — DEMO PLANLAYIN`", 1),
    ("[`Sound `,n?`on`:`off`]", "[`Ses `,n?`açık`:`kapalı`]", 1),
    ("`Previous card`", "`Önceki kart`", 1), ("`Next card`", "`Sonraki kart`", 1),
    ("\"aria-label\":`Suits`", "\"aria-label\":`Bölümler`", 2), ("\"aria-label\":`Cover`", "\"aria-label\":`Kapak`", 1),
    ("`Need to talk to someone who gets it?`", "`İşin içinden biriyle konuşmak ister misiniz?`", 1), ("`Contact us`", "`İletişime geçin`", 1),
    ("`FREE GAMES START`", "`BEDAVA OYUNLAR BAŞLIYOR`", 1), ("`Running count`", "`Sayım`", 1),
    ("children:`High Noon`", "children:`Düello Vakti`", 1),
]
for old, new, exp in UI:
    n = tr.count(old)
    if n != exp:
        print(f"WARN ui {old[:50]!r}: expected {exp}, found {n}")
        if n == 0: continue
    tr = tr.replace(old, new)

open(os.path.join(ROOT, "assets", "index.js"), "w", encoding="utf-8").write(EN)
open(os.path.join(ROOT, "assets", "index.tr.js"), "w", encoding="utf-8").write(tr)
print("EN", len(EN), "TR", len(tr), "media cards", len(media))
