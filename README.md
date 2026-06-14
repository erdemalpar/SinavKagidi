<div align="center">

# 🎓 Sınav Kağıdı Hazırlama Sistemi

**Öğretmenler için modern, hızlı ve profesyonel sınav kağıdı hazırlama web uygulaması**

[![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-000000?style=for-the-badge&logo=flask&logoColor=white)](https://flask.palletsprojects.com)
[![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=for-the-badge&logo=sqlite&logoColor=white)](https://sqlite.org)
[![License](https://img.shields.io/badge/Lisans-Eğitim_Amaçlı-green?style=for-the-badge)](LICENSE)

</div>

---

## 📌 Genel Bakış

**Sınav Kağıdı Hazırlama Sistemi**, öğretmenlerin soru bankası oluşturmasını, soruları yönetmesini, profesyonel PDF sınav kağıtları hazırlamasını ve yoklama takibi yapmasını sağlayan tam kapsamlı bir web uygulamasıdır.

---

## ✨ Özellikler

### 📚 Soru Bankası
- Soru metni ve A–E şıklı sorular ekleme / düzenleme / silme
- Konu, zorluk ve puan bazında filtreleme
- Görsel (PNG/JPG) yükleme ve soru içinde gösterme
- PDF, DOCX, Excel dosyalarından toplu soru aktarımı
- Sık düzeni (yatay / dikey) ve soru tipi desteği

### 📝 Sınav Hazırlama
- Soru bankasından tek tıkla soru seçimi
- Seçilen sorularda gerçek zamanlı istatistik (adet, toplam puan, ortalama)
- Sınav başlığı, tarih, saat, salon, eğitim yılı ve dönem bilgisi
- Okul logosu (sol / sağ) ve özel imza metni
- Yazı fontu, boyutu, rengi ve stili ayarı
- Soru sırası sürükle-bırak ile değiştirme
- Birden fazla sınav kaydedip listeleme
- Kaydedilmiş sınavı düzenleme / silme

### 🖨️ Sınav Önizleme & PDF
- A4 formatında canlı, gerçek zamanlı önizleme
- Sınav başlığı katsayısı, üst/alt boşluk, şık boşluğu ayarları
- Logo boyutu ve puan kutusu boyutu kontrolü
- `html2pdf.js` ile yüksek kaliteli PDF indirme
- Doğrudan yazdırma desteği
- Öğretmene özel cevap anahtarı görünümü

### 📊 Not Girişi
- Sınıf seçimi ve öğrenci listesi yönetimi
- Not girişi ve istatistik hesaplama
- Başarı analizi ve görsel raporlama

### 📋 Yoklama Sistemi
- Oturum bazlı yoklama takibi (14 hafta desteği)
- Excel öğrenci listesi yükleme ve veritabanına mühürleme
- QR kod ile öğrenci katılım kaydı
- Konum doğrulama ve süre kısıtı seçenekleri
- Haftalık/oturumsal istatistik ve rapor
- Yoklama verilerini Excel'e aktarma

### 🔐 Kullanıcı Yönetimi
- Admin / Öğrenci rol sistemi
- Oturum bazlı yetkilendirme (`@admin_required`, `@login_required`)
- JWT desteği

---

## 🛠️ Teknoloji Stack

| Katman | Teknoloji |
|--------|-----------|
| **Backend** | Python 3.8+, Flask 3.0.0 |
| **Veritabanı** | SQLite + SQLAlchemy ORM |
| **Frontend** | HTML5, Tailwind CSS, Vanilla JS |
| **PDF** | html2pdf.js |
| **İkonlar** | Lucide Icons |
| **Bildirimler** | SweetAlert2 |
| **Dosya İşleme** | python-docx, PyPDF2, openpyxl, Pillow, pandas |
| **QR Kod** | qrcode |

---

## 📦 Kurulum

### Gereksinimler

- Python **3.8** veya üstü
- `pip` (Python paket yöneticisi)

### Adım Adım

```bash
# 1. Repoyu klonlayın
git clone https://github.com/erdemalpar/SinavKagidi.git
cd SinavKagidi

# 2. Sanal ortam oluşturun ve aktif edin
python3 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows

# 3. Bağımlılıkları yükleyin
pip install -r requirements.txt

# 4. Uygulamayı başlatın
python app.py
```

Uygulama **http://127.0.0.1:5001** adresinde çalışmaya başlar.

---

## 📂 Proje Yapısı

```
SinavKagidi/
├── app.py                      # Flask ana uygulama & tüm route'lar
├── requirements.txt            # Python bağımlılıkları
├── templates/
│   ├── base.html               # Ana layout (sidebar, toast, logger)
│   ├── anasayfa.html           # Dashboard
│   ├── login.html              # Giriş ekranı
│   ├── soru_bankasi.html       # Soru yönetimi
│   ├── sinav_hazirlama.html    # Sınav oluşturma
│   ├── sinav_onizleme.html     # PDF önizleme
│   ├── not_girisi.html         # Not girişi & analiz
│   ├── yoklama.html            # Yoklama paneli
│   ├── yoklama_kayit.html      # Öğrenci katılım formu
│   ├── analiz.html             # Sınıf analiz ekranı
│   ├── ayarlar.html            # Sistem ayarları
│   └── tarif.html              # Yardım & kılavuz
└── static/
    ├── uploads/                # Yüklenen görseller
    └── yoklama/                # Yoklama dosyaları & raporlar
```

---

## 🎯 Kullanım

### 1️⃣ Soru Bankası Oluşturma
1. Sol menüden **Soru Bankası**'na gidin
2. **Yeni Soru Ekle** butonuna tıklayın
3. Soru metni, A–E şıkları, doğru cevap, konu, zorluk ve puanı girin
4. İsteğe bağlı görsel yükleyin
5. **Kaydet**

### 2️⃣ Sınav Hazırlama
1. Sol menüden **Sınav Hazırla**'ya gidin
2. Soru bankasından soruları seçin
3. Başlık, tarih, okul bilgilerini doldurun
4. **Sınavı Kaydet** veya **Önizle & PDF**

### 3️⃣ PDF Oluşturma
1. Önizleme ekranında kağıdı inceleyin
2. Sağ panelden yazı/boyut/boşluk ayarlarını yapın
3. **PDF İndir** veya **Yazdır**

### 4️⃣ Yoklama Açma
1. Sol menüden **Yoklama**'ya gidin
2. **Yeni Oturum Başlat** ile yoklama oluşturun
3. Excel öğrenci listesi yükleyin
4. QR kodu paylaşın; öğrenciler katılımlarını kaydetsin

---

## 🔒 Güvenlik Notları

> Bu uygulama **geliştirme (development)** modundadır.

Production ortamı için yapılması gerekenler:

- `SECRET_KEY` değerini güçlü rastgele bir değerle değiştirin
- `debug=False` yapın
- Gunicorn veya uWSGI gibi bir WSGI sunucusu kullanın
- HTTPS zorunlu hale getirin
- Dosya yükleme güvenlik kontrolleri ekleyin

---

## 🤝 Katkıda Bulunma

1. Bu repoyu **fork** edin
2. Yeni bir **feature branch** oluşturun (`git checkout -b ozellik/yeni-ozellik`)
3. Değişikliklerinizi **commit** edin (`git commit -m 'feat: yeni özellik eklendi'`)
4. Branch'i **push** edin (`git push origin ozellik/yeni-ozellik`)
5. Bir **Pull Request** açın

---

## 📧 İletişim

Hata bildirimi veya öneri için lütfen [issue açın](https://github.com/erdemalpar/SinavKagidi/issues).

---

<div align="center">

**🎓 Başarılı sınavlar hazırlamanız dileğiyle!**

*Geliştirici: [erdemalpar](https://github.com/erdemalpar)*

</div>
