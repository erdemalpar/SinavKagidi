from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sinav-kagidi-gizli-anahtar-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sinav_kagidi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/yuklemeler'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max dosya boyutu

# İzin verilen dosya uzantıları
IZIN_VERILEN_UZANTILAR = {'pdf', 'docx', 'xlsx', 'xls', 'png', 'jpg', 'jpeg'}

# Veritabanı modellerini import et
from models import db, Soru, SinavAyarlari, SinavKagidi, SinavSorusu, Ayarlar

# db'yi app ile başlat
db.init_app(app)

def izin_verilen_dosya(dosya_adi):
    """Dosya uzantısının izin verilen listede olup olmadığını kontrol eder"""
    return '.' in dosya_adi and \
           dosya_adi.rsplit('.', 1)[1].lower() in IZIN_VERILEN_UZANTILAR

@app.route('/')
def anasayfa():
    """Ana sayfa - Dashboard"""
    toplam_soru = Soru.query.count()
    toplam_sinav = SinavKagidi.query.count()
    return render_template('anasayfa.html', 
                         toplam_soru=toplam_soru, 
                         toplam_sinav=toplam_sinav)

@app.route('/soru-bankasi')
def soru_bankasi():
    """Soru bankası sayfası"""
    sorular = Soru.query.order_by(Soru.olusturma_tarihi.desc()).all()
    return render_template('soru_bankasi.html', sorular=sorular)

@app.route('/soru-ekle', methods=['POST'])
def soru_ekle():
    """Yeni soru ekle"""
    try:
        data = request.json
        yeni_soru = Soru(
            soru_metni=data.get('soru_metni'),
            secenek_a=data.get('secenek_a'),
            secenek_b=data.get('secenek_b'),
            secenek_c=data.get('secenek_c'),
            secenek_d=data.get('secenek_d'),
            secenek_e=data.get('secenek_e'),
            dogru_cevap=data.get('dogru_cevap'),
            konu=data.get('konu'),
            zorluk=data.get('zorluk', 'Orta'),
            puan=data.get('puan', 5),
            gorsel_yolu=data.get('gorsel_yolu'),
            gorsel_konum=data.get('gorsel_konum', 'arada'),
            sik_duzeni=data.get('sik_duzeni', 'alt_alta')
        )
        db.session.add(yeni_soru)
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Soru başarıyla eklendi', 'soru_id': yeni_soru.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/soru-sil/<int:soru_id>', methods=['DELETE'])
def soru_sil(soru_id):
    """Soru sil"""
    try:
        soru = Soru.query.get_or_404(soru_id)
        db.session.delete(soru)
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Soru başarıyla silindi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/dosya-yukle', methods=['POST'])
def dosya_yukle():
    """Dosya yükle ve işle"""
    try:
        if 'dosya' not in request.files:
            return jsonify({'basarili': False, 'mesaj': 'Dosya bulunamadı'}), 400
        
        dosya = request.files['dosya']
        if dosya.filename == '':
            return jsonify({'basarili': False, 'mesaj': 'Dosya seçilmedi'}), 400
        
        if dosya and izin_verilen_dosya(dosya.filename):
            dosya_adi = secure_filename(dosya.filename)
            dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], dosya_adi)
            
            # Upload klasörünü oluştur
            os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            dosya.save(dosya_yolu)
            
            # Dosya uzantısını al
            dosya_uzantisi = dosya_adi.rsplit('.', 1)[1].lower()
            
            # Görsel dosyaları işle
            if dosya_uzantisi in ['png', 'jpg', 'jpeg']:
                return jsonify({
                    'basarili': True, 
                    'mesaj': 'Görsel başarıyla yüklendi. Manuel olarak soru eklerken kullanabilirsiniz.',
                    'dosya_adi': dosya_adi,
                    'dosya_yolu': dosya_yolu,
                    'tip': 'gorsel'
                })
            
            # Metin dosyalarını işle (PDF, DOCX, Excel)
            print(f"=== Dosya işleniyor: {dosya_adi}, uzantı: {dosya_uzantisi} ===")
            try:
                from dosya_isleme import dosya_isle
                print("dosya_isleme modülü başarıyla import edildi")
            except Exception as import_hatasi:
                print(f"IMPORT HATASI: {import_hatasi}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'basarili': False, 
                    'mesaj': f'Dosya işleme modülü yüklenemedi: {str(import_hatasi)}'
                }), 400
            
            try:
                sorular = dosya_isle(dosya_yolu, dosya_uzantisi)
                print(f"Dosya işleme tamamlandı. Bulunan soru sayısı: {len(sorular) if sorular else 0}")
            except Exception as isle_hatasi:
                print(f"DOSYA İŞLEME HATASI: {isle_hatasi}")
                import traceback
                traceback.print_exc()
                return jsonify({
                    'basarili': False, 
                    'mesaj': f'Dosya işlenirken hata: {str(isle_hatasi)}'
                }), 400
            
            if not sorular:
                return jsonify({
                    'basarili': False, 
                    'mesaj': 'Dosyadan soru çıkarılamadı. Lütfen dosya formatını kontrol edin.'
                }), 400
            
            # Soruları veritabanına ekle
            eklenen_sayisi = 0
            hatali_sayisi = 0
            
            for soru_data in sorular:
                try:
                    yeni_soru = Soru(
                        soru_metni=soru_data.get('soru_metni'),
                        secenek_a=soru_data.get('secenek_a'),
                        secenek_b=soru_data.get('secenek_b'),
                        secenek_c=soru_data.get('secenek_c'),
                        secenek_d=soru_data.get('secenek_d'),
                        secenek_e=soru_data.get('secenek_e'),
                        dogru_cevap=soru_data.get('dogru_cevap', 'A'),
                        konu=soru_data.get('konu', ''),
                        zorluk=soru_data.get('zorluk', 'Orta'),
                        puan=soru_data.get('puan', 5)
                    )
                    db.session.add(yeni_soru)
                    eklenen_sayisi += 1
                except Exception as e:
                    hatali_sayisi += 1
                    print(f"Soru ekleme hatası: {e}")
                    continue
            
            db.session.commit()
            
            return jsonify({
                'basarili': True, 
                'mesaj': f'Başarıyla {eklenen_sayisi} soru eklendi!' + 
                        (f' ({hatali_sayisi} soru eklenemedi)' if hatali_sayisi > 0 else ''),
                'dosya_adi': dosya_adi,
                'eklenen_soru_sayisi': eklenen_sayisi,
                'hatali_soru_sayisi': hatali_sayisi
            })
        else:
            return jsonify({'basarili': False, 'mesaj': 'İzin verilmeyen dosya türü'}), 400
            
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': f'Hata: {str(e)}'}), 400

@app.route('/sinav-hazirlama')
def sinav_hazirlama():
    """Sınav hazırlama sayfası"""
    sorular = Soru.query.all()
    ayarlar = SinavAyarlari.query.first()
    if not ayarlar:
        # Varsayılan ayarlar oluştur
        ayarlar = SinavAyarlari()
        db.session.add(ayarlar)
        db.session.commit()
    
    # Düzenleme modu: URL'den sınav ID'si gelirse o sınavı yükle
    sinav_id = request.args.get('sinav')
    eski_sinav = None
    if sinav_id:
        eski_sinav = SinavKagidi.query.get(sinav_id)
        
    return render_template('sinav_hazirlama.html', sorular=sorular, ayarlar=ayarlar, eski_sinav=eski_sinav)

@app.template_filter('turkce_tarih')
def turkce_tarih_filter(tarih_str):
    if not tarih_str:
        return ""
    try:
        from datetime import datetime
        # Tarih formatı: YYYY-MM-DD
        dt = datetime.strptime(tarih_str, '%Y-%m-%d')
        aylar = ['', 'Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran', 
                'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
        return f"{dt.day} {aylar[dt.month]} {dt.year}"
    except:
        return tarih_str

@app.route('/sinav-kaydet', methods=['POST'])
def sinav_kaydet():
    """Sınav kağıdını kaydet"""
    try:
        data = request.json
        yeni_sinav = SinavKagidi(
            baslik=data.get('baslik', ''),
            egitim_yili=data.get('egitim_yili'),
            donem=data.get('donem'),
            aciklama=data.get('aciklama'),
            tarih=data.get('tarih'),
            saat=data.get('saat'), # Yeni eklenen
            okul_adi=data.get('okul_adi'),
            imza_metni=data.get('imza_metni'), # Yeni İmza Metni
            yazi_fontu=data.get('yazi_fontu'),
            yazi_boyutu=data.get('yazi_boyutu', 12),
            yazi_rengi=data.get('yazi_rengi', '#000000'),
            yazi_stili=data.get('yazi_stili', 'normal'),
            gorsel_boyutu=data.get('gorsel_boyutu', 100),
            logo_sol=data.get('logo_sol'),
            logo_sag=data.get('logo_sag'),
            logo_boyutu=data.get('logo_boyutu', 80)
        )
        db.session.add(yeni_sinav)
        db.session.flush()
        
        # Seçilen soruları ekle
        for soru_id in data.get('soru_idleri', []):
            soru = Soru.query.get(soru_id)
            if soru:
                sinav_sorusu = SinavSorusu(
                    sinav_id=yeni_sinav.id,
                    soru_id=soru.id,
                    sira=len(yeni_sinav.sorular) + 1
                )
                db.session.add(sinav_sorusu)
        
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Sınav başarıyla kaydedildi', 'sinav_id': yeni_sinav.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400



@app.route('/sinav-onizleme/<int:sinav_id>')
def sinav_onizleme(sinav_id):
    """Sınav kağıdı önizleme"""
    sinav = SinavKagidi.query.get_or_404(sinav_id)
    ayarlar = SinavAyarlari.query.first()
    ayarlar_imza = Ayarlar.query.first()
    return render_template('sinav_onizleme.html', sinav=sinav, ayarlar=ayarlar, ayarlar_imza=ayarlar_imza)

@app.route('/ayarlar')
def ayarlar():
    """Ayarlar sayfası"""
    ayarlar = Ayarlar.query.first()
    return render_template('ayarlar.html', ayarlar=ayarlar)

@app.route('/ayarlar-kaydet', methods=['POST'])
def ayarlar_kaydet():
    """Ayarları kaydet"""
    try:
        data = request.get_json()
        ayarlar = Ayarlar.query.first()
        
        if not ayarlar:
            ayarlar = Ayarlar()
            db.session.add(ayarlar)
        
        ayarlar.imza_metni = data.get('imza_metni', '')
        ayarlar.cizgi_rengi = data.get('cizgi_rengi', '#CCCCCC')
        ayarlar.cizgi_kalinlik = float(data.get('cizgi_kalinlik', 1.0))
        ayarlar.metin_boyutu = int(data.get('metin_boyutu', 12))
        
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Ayarlar başarıyla kaydedildi'})
    except Exception as e:
        db.session.rollback()
        print(f"Ayarlar kaydetme hatası: {e}")
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/soru/<int:soru_id>')
def soru_getir(soru_id):
    """Tek bir sorunun bilgilerini getir"""
    try:
        soru = Soru.query.get_or_404(soru_id)
        return jsonify({
            'basarili': True,
            'soru': soru.sozluk_olustur()
        })
    except Exception as e:
        return jsonify({'basarili': False, 'mesaj': str(e)}), 404


@app.route('/gorsel-yukle', methods=['POST'])
def gorsel_yukle():
    """Soru görseli yükle"""
    if 'gorsel' not in request.files:
        return jsonify({'basarili': False, 'mesaj': 'Dosya bulunamadı'}), 400
    
    dosya = request.files['gorsel']
    if dosya.filename == '':
        return jsonify({'basarili': False, 'mesaj': 'Dosya seçilmedi'}), 400
        
    if dosya and izin_verilen_dosya(dosya.filename):
        import uuid
        from werkzeug.utils import secure_filename
        
        dosya_adi = secure_filename(dosya.filename)
        ext = dosya_adi.rsplit('.', 1)[1].lower()
        if ext not in {'png', 'jpg', 'jpeg', 'gif'}:
            return jsonify({'basarili': False, 'mesaj': 'Sadece resim dosyaları yüklenebilir'}), 400
            
        yeni_ad = f"soru_{uuid.uuid4().hex[:8]}.{ext}"
        
        # uploads klasörüne kaydet
        kayit_yolu = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(kayit_yolu, exist_ok=True)
        dosya.save(os.path.join(kayit_yolu, yeni_ad))
        
        return jsonify({'basarili': True, 'dosya_yolu': f'/static/uploads/{yeni_ad}'})
    
    return jsonify({'basarili': False, 'mesaj': 'Geçersiz dosya'}), 400


@app.route('/soru-guncelle/<int:soru_id>', methods=['PUT'])
def soru_guncelle(soru_id):
    """Soru güncelle"""
    try:
        soru = Soru.query.get_or_404(soru_id)
        data = request.get_json()
        
        soru.soru_metni = data.get('soru_metni', soru.soru_metni)
        soru.secenek_a = data.get('secenek_a', soru.secenek_a)
        soru.secenek_b = data.get('secenek_b', soru.secenek_b)
        soru.secenek_c = data.get('secenek_c', soru.secenek_c)
        soru.secenek_d = data.get('secenek_d', soru.secenek_d)
        soru.secenek_e = data.get('secenek_e', soru.secenek_e)
        soru.dogru_cevap = data.get('dogru_cevap', soru.dogru_cevap)
        soru.konu = data.get('konu', soru.konu)
        soru.zorluk = data.get('zorluk', soru.zorluk)
        soru.puan = data.get('puan', soru.puan)
        
        # Yeni alanlar
        soru.gorsel_yolu = data.get('gorsel_yolu', soru.gorsel_yolu)
        soru.gorsel_konum = data.get('gorsel_konum', soru.gorsel_konum)
        soru.sik_duzeni = data.get('sik_duzeni', soru.sik_duzeni)
        
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Soru güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
