# 📝 Sınav Kağıdı Hazırlama Sistemi

Modern ve kullanıcı dostu bir web uygulaması ile profesyonel sınav kağıtları oluşturun!

[![Canlı Demo](https://img.shields.io/badge/Canlı_Demo-Görüntüle-2ea44f?style=for-the-badge&logo=github)](https://erdemalpar.github.io/SinavKagidi)

## 🚀 Özellikler

### ✅ Tamamlanan Özellikler (v1.0)

- **📚 Soru Bankası Yönetimi**
  - Soruları metin ve şıklar olarak kaydetme
  - Soru ekleme, silme ve görüntüleme
  - Konu, zorluk ve puan bazında filtreleme
  - Detaylı soru kartları ile modern görünüm

- **⚙️ Antet Ayarları**
  - Okul adı, eğitim yılı, dönem bilgileri
  - Tarih ve salon bilgisi
  - Puan gösterme/gizleme seçeneği
  - Canlı önizleme ile anlık görsel geri bildirim

- **📄 Sınav Hazırlama**
  - Soru bankasından soru seçimi
  - Seçilen soruların gerçek zamanlı istatistikleri
  - Toplam soru sayısı, puan ve ortalama hesaplama
  - Sınav başlığı ve açıklama ekleme

- **🖨️ PDF Çıktısı**
  - A4 formatında profesyonel sınav kağıdı
  - html2pdf.js ile yüksek kaliteli PDF oluşturma
  - Yazdırma öncesi önizleme
  - Öğretmen için cevap anahtarı (yazdırılmaz)

- **🎨 Modern Kullanıcı Arayüzü**
  - Tailwind CSS ile şık ve responsive tasarım
  - Lucide ikonları ile görsel zenginlik
  - Sidebar navigasyon menüsü
  - Gradient renkler ve animasyonlar
  - Toast bildirimleri

### 🔜 Yakında Eklenecek Özellikler

- **📤 Dosya Yükleme ve İşleme**
  - PDF dosyasından soru çıkarma
  - DOCX dosyasından soru içe aktarma
  - Excel toplu soru yükleme
  - Görsel (PNG/JPG) upload ve soru içinde gösterme

- **🎨 Gelişmiş Özellikler**
  - Okul logosu ekleme
  - Farklı tema seçenekleri
  - Soru düzenleme özelliği
  - Sınav geçmişi ve şablonlar

## 🛠️ Teknoloji Stack

- **Backend:** Python Flask 3.0.0
- **Veritabanı:** SQLite (SQLAlchemy ORM)
- **Frontend:** HTML5, Tailwind CSS, JavaScript
- **PDF:** html2pdf.js
- **İkonlar:** Lucide Icons
- **Dosya İşleme:** python-docx, PyPDF2, openpyxl, Pillow

## 📦 Kurulum

### Gereksinimler

- Python 3.8 veya üstü
- pip (Python paket yöneticisi)

### Adım Adım Kurulum

1. **Projeyi klonlayın veya indirin**
```bash
cd sinav-kagidi
```

2. **Gerekli Python paketlerini yükleyin**
```bash
pip install -r requirements.txt
```

3. **Uygulamayı başlatın**
```bash
python app.py
```

4. **Tarayıcınızda açın**
```
http://127.0.0.1:5001
```

## 📂 Proje Yapısı

```
sinav-kagidi/
├── app.py                  # Flask ana uygulama dosyası
├── models.py               # SQLAlchemy veritabanı modelleri
├── requirements.txt        # Python bağımlılıkları
├── templates/              # HTML şablonları
│   ├── base.html          # Ana şablon (layout)
│   ├── anasayfa.html      # Dashboard
│   ├── soru_bankasi.html  # Soru yönetimi
│   ├── sinav_hazirlama.html # Sınav oluşturma
│   ├── ayarlar.html       # Antet ayarları
│   └── sinav_onizleme.html # PDF önizleme
├── static/                 # Statik dosyalar
│   └── yuklemeler/        # Yüklenen dosyalar
└── sinav_kagidi.db        # SQLite veritabanı (otomatik oluşur)
```

## 🎯 Kullanım

### 1. Soru Bankası Oluşturma

- Sol menüden **"Soru Bankası"** sekmesine gidin
- **"Yeni Soru Ekle"** butonuna tıklayın
- Soru metnini ve şıkları (A-E) girin
- Doğru cevabı, konuyu, zorluk seviyesini ve puanı belirleyin
- **"Soru Ekle"** ile kaydedin

### 2. Antet Ayarlarını Yapılandırma

- Sol menüden **"Ayarlar"** sekmesine gidin
- Okul adı, eğitim yılı, dönem bilgilerini girin
- Tarih ve salon bilgilerini ekleyin (opsiyonel)
- Değişiklikler canlı önizlemede görünür
- **"Ayarları Kaydet"** ile kaydedin

### 3. Sınav Hazırlama

- Sol menüden **"Sınav Hazırla"** sekmesine gidin
- Sol panelden eklemek istediğiniz soruları seçin
- Sağ panelde seçilen soruların istatistiklerini görün
- Sınav başlığı ve açıklama (opsiyonel) ekleyin
- **"Sınavı Kaydet"** veya **"Önizle & PDF"** butonuna tıklayın

### 4. PDF Oluşturma

- Sınav önizleme sayfasında kağıdı inceleyin
- **"Yazdır"** butonu ile doğrudan yazdırabilirsiniz
- **"PDF İndir"** butonu ile bilgisayarınıza kaydedin

## 🗄️ Veritabanı Modelleri

### Soru
- Soru metni, şıklar (A-E), doğru cevap
- Konu, zorluk seviyesi, puan
- Görsel yolu (yakında)
- Oluşturma/güncellenme tarihleri

### SinavAyarlari
- Okul adı, eğitim yılı, dönem
- Tarih, salon bilgileri
- Puan gösterme ayarı
- Logo yolu (yakında)

### SinavKagidi
- Sınav başlığı ve açıklaması
- İlişkili sorular (many-to-many)
- Oluşturma/güncellenme tarihleri

### SinavSorusu
- Sınav-Soru ilişki tablosu
- Soru sırası
- Özel puan (opsiyonel)

## 🎨 Ekran Görüntüleri

Uygulama modern ve kullanıcı dostu bir arayüze sahiptir:
- 🏠 Dashboard ile hızlı erişim
- 📊 İstatistik kartları
- 🎨 Gradient renkler ve animasyonlar
- 📱 Responsive tasarım

## 🔒 Güvenlik Notları

- Bu uygulama development (geliştirme) modundadır
- Production kullanımı için:
  - `SECRET_KEY` değiştirin
  - `debug=False` yapın
  - WSGI server (Gunicorn, uWSGI) kullanın
  - HTTPS aktif edin
  - Dosya yükleme güvenliği ekleyin

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 🤝 Katkıda Bulunma

Önerileriniz ve katkılarınız için:
1. Fork edin
2. Feature branch oluşturun
3. Commitinizi yapın
4. Pull request gönderin

## 📧 İletişim

Sorularınız ve geri bildirimleriniz için issue açabilirsiniz.

---

**🎓 Başarılı sınavlar hazırlamanız dileğiyle!**
