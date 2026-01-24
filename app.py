from flask import Flask, render_template, request, jsonify, redirect, url_for
from datetime import datetime
from sqlalchemy import text
import os
from werkzeug.utils import secure_filename
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sinav-kagidi-gizli-anahtar-2026'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///sinav_kagidi.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/yuklemeler'
app.config['MAX_CONTENT_LENGTH'] = 512 * 1024 * 1024  # 512MB max dosya boyutu (Kullanıcı isteği üzerine artırıldı)

# İzin verilen dosya uzantıları
IZIN_VERILEN_UZANTILAR = {'pdf', 'docx', 'xlsx', 'xls', 'png', 'jpg', 'jpeg', 'json'}

# Veritabanı modellerini import et
from models import db, Soru, SinavAyarlari, SinavKagidi, SinavSorusu, Ayarlar, YoklamaOturumu, YoklamaKayit

# db'yi app ile başlat
db.init_app(app)

# JWT Yapılandırması
from flask_jwt_extended import JWTManager, create_access_token, decode_token
import qrcode
import io
import base64
from math import radians, cos, sin, asin, sqrt

app.config['JWT_SECRET_KEY'] = 'yoklama-gizli-anahtar-2026'
jwt = JWTManager(app)

def haversine(lon1, lat1, lon2, lat2):
    """İki koordinat arasındaki mesafeyi metre cinsinden hesaplar"""
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371000 # Dünyanın metre cinsinden yarıçapı
    return c * r

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
    # Benzersiz konuları al (boş olmayanları)
    konular = db.session.query(Soru.konu).filter(Soru.konu != None, Soru.konu != '').distinct().all()
    konular = sorted([k[0] for k in konular])
    
    # Benzersiz zorluk seviyelerini al
    zorluklar = db.session.query(Soru.zorluk).filter(Soru.zorluk != None, Soru.zorluk != '').distinct().all()
    zorluklar = [z[0] for z in zorluklar]
    
    return render_template('soru_bankasi.html', sorular=sorular, konular=konular, zorluklar=zorluklar)

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
            gorsel_konum=data.get('gorsel_konum', 'yanda'),
            sik_duzeni=data.get('sik_duzeni', 'iki_sutun'),
            soru_tipi=data.get('soru_tipi', 'test')
        )
        # Mükerrer Kayıt Kontrolü
        mevcut = Soru.query.filter_by(soru_metni=data.get('soru_metni')).first()
        if mevcut:
            return jsonify({'basarili': False, 'mesaj': 'Bu soru zaten soru bankasında kayıtlı!'}), 400

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

@app.route('/api/sorular-json')
def sorular_json():
    """Tüm soruları JSON formatında döndürür"""
    try:
        sorular = Soru.query.all()
        soru_listesi = []
        for soru in sorular:
            soru_listesi.append({
                'id': soru.id,
                'soru_metni': soru.soru_metni,
                'secenek_a': soru.secenek_a,
                'secenek_b': soru.secenek_b,
                'secenek_c': soru.secenek_c,
                'secenek_d': soru.secenek_d,
                'secenek_e': soru.secenek_e,
                'dogru_cevap': soru.dogru_cevap,
                'konu': soru.konu,
                'zorluk': soru.zorluk,
                'puan': soru.puan,
                'gorsel_yolu': soru.gorsel_yolu,
                'gorsel_konum': soru.gorsel_konum,
                'sik_duzeni': soru.sik_duzeni,
                'soru_tipi': soru.soru_tipi,
                'olusturma_tarihi': soru.olusturma_tarihi.strftime('%Y-%m-%d %H:%M:%S') if soru.olusturma_tarihi else None
            })
        return jsonify(soru_listesi)
    except Exception as e:
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/tum-sorulari-sil', methods=['DELETE'])
def tum_sorulari_sil():
    """Tüm soruları sil"""
    try:
        # Tüm soruları sil
        silinen_sayisi = Soru.query.delete()
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': f'{silinen_sayisi} soru başarıyla silindi.'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/dosya-yukle', methods=['POST'])
def dosya_yukle():
    """Dosya yükle ve işle (Çoklu Dosya Desteği)"""
    try:
        if 'dosya' not in request.files:
            return jsonify({'basarili': False, 'mesaj': 'Dosya bulunamadı'}), 400
        
        dosyalar = request.files.getlist('dosya')
        
        if not dosyalar or all(d.filename == '' for d in dosyalar):
            return jsonify({'basarili': False, 'mesaj': 'Dosya seçilmedi'}), 400
            
        # Upload klasörünü oluştur
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
            
        toplam_eklenen = 0
        toplam_hata = 0
        toplam_mukerrer = 0
        islenen_dosyalar = []
        yuklenen_gorseller = []
        
        from dosya_isleme import dosya_isle # Lazy import
        
        for dosya in dosyalar:
            if not dosya or dosya.filename == '':
                continue
                
            if not izin_verilen_dosya(dosya.filename):
                print(f"İzin verilmeyen dosya türü: {dosya.filename}")
                continue
                
            dosya_adi = secure_filename(dosya.filename)
            dosya_yolu = os.path.join(app.config['UPLOAD_FOLDER'], dosya_adi)
            dosya.save(dosya_yolu)
            
            dosya_uzantisi = dosya_adi.rsplit('.', 1)[1].lower()
            
            # Görsel Dosyaları (Soru Olarak Kaydet)
            if dosya_uzantisi in ['png', 'jpg', 'jpeg']:
                try:
                    # Görseli soru olarak ekle
                    # Web uyumlu yol (static/yuklemeler/dosya.png)
                    web_gorsel_yolu = f"static/yuklemeler/{dosya_adi}"
                    
                    yeni_soru = Soru(
                        soru_metni=f"Görsel Soru ({dosya_adi}) - Lütfen soruyu ve şıkları düzenleyiniz.",
                        secenek_a="-", secenek_b="-", secenek_c="-", secenek_d="-", secenek_e="-",
                        dogru_cevap="A",
                        konu="Görsel Yükleme",
                        zorluk="Orta",
                        puan=5,
                        gorsel_yolu=web_gorsel_yolu,
                        gorsel_konum="altta", # Görsel sorularda genelde görsel altta veya üstte olur
                        sik_duzeni="yan_yana"
                    )
                    db.session.add(yeni_soru)
                    toplam_eklenen += 1
                    islenen_dosyalar.append(f"{dosya_adi} (Görsel)")
                except Exception as e:
                    toplam_hata += 1
                    print(f"Görsel soru ekleme hatası: {e}")
                
                continue
                
            # Soru Dosyaları (İşle ve DB'ye ekle)
            try:
                print(f"=== Dosya işleniyor: {dosya_adi} ===")
                sorular = dosya_isle(dosya_yolu, dosya_uzantisi)
                
                if not sorular:
                    toplam_hata += 1 # Dosyadan soru çıkmadıysa hata/uyarı hanesine yaz
                    print(f"Uyarı: {dosya_adi} dosyasından soru çıkarılamadı.")
                    continue
                
                eklenen_bu_dosya = 0
                
                for soru_data in sorular:
                    try:
                        # Mükerrer Kontrolü
                        if Soru.query.filter_by(soru_metni=soru_data.get('soru_metni')).first():
                            toplam_mukerrer += 1
                            continue

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
                            puan=soru_data.get('puan', 5),
                            gorsel_yolu=soru_data.get('gorsel_yolu'),
                            gorsel_konum=soru_data.get('gorsel_konum', 'yanda'),
                            sik_duzeni=soru_data.get('sik_duzeni', 'iki_sutun')
                        )
                        db.session.add(yeni_soru)
                        toplam_eklenen += 1
                        eklenen_bu_dosya += 1
                    except Exception as e:
                        toplam_hata += 1
                        print(f"Soru ekleme hatası: {e}")
                
                islenen_dosyalar.append(f"{dosya_adi} ({eklenen_bu_dosya} soru)")
                
            except Exception as isle_hatasi:
                toplam_hata += 1
                print(f"Dosya işleme hatası ({dosya_adi}): {isle_hatasi}")
                import traceback
                traceback.print_exc()

        db.session.commit()
        
        # Sonuç Yanıtı
        mesaj_parcalari = []
        if islenen_dosyalar:
            mesaj_parcalari.append(f"{len(islenen_dosyalar)} döküman işlendi.")
        if yuklenen_gorseller:
            mesaj_parcalari.append(f"{len(yuklenen_gorseller)} görsel yüklendi.")
            
        genel_mesaj = " ".join(mesaj_parcalari)
        detay_mesaj = f"Toplam {toplam_eklenen} soru eklendi."
        
        if toplam_mukerrer > 0:
            detay_mesaj += f" ({toplam_mukerrer} mükerrer atlandı)"
        if toplam_hata > 0:
            detay_mesaj += f" ({toplam_hata} işlem hatası)"
            
        full_mesaj = f"{genel_mesaj} {detay_mesaj}"
        
        # Eğer sadece görsel yüklendiyse özel format
        if yuklenen_gorseller and not islenen_dosyalar:
             return jsonify({
                'basarili': True, 
                'mesaj': f'{len(yuklenen_gorseller)} görsel başarıyla yüklendi.',
                'tip': 'gorsel',
                'dosya_adi': yuklenen_gorseller[0]['dosya_adi'] # Arkadaki JS tek dosya mantığına sahip olabilir, uyumluluk için
            })

        return jsonify({
            'basarili': True, 
            'mesaj': full_mesaj,
            'eklenen_soru_sayisi': toplam_eklenen,
            'hatali_soru_sayisi': toplam_hata,
            'mukerrer_soru_sayisi': toplam_mukerrer
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': f'Genel Hata: {str(e)}'}), 400

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
            okul_adi_boyutu=data.get('okul_adi_boyutu', 24),
            egitim_yili_boyutu=data.get('egitim_yili_boyutu', 18),
            donem_boyutu=data.get('donem_boyutu', 16),
            baslik_boyutu=data.get('baslik_boyutu', 16),
            imza_metni=data.get('imza_metni'), # Yeni İmza Metni
            yazi_fontu=data.get('yazi_fontu'),
            yazi_boyutu=data.get('yazi_boyutu', 12),
            yazi_rengi=data.get('yazi_rengi', '#000000'),
            yazi_stili=data.get('yazi_stili', 'normal'),
            gorsel_boyutu=data.get('gorsel_boyutu', 100),
            logo_sol=data.get('logo_sol'),
            logo_sag=data.get('logo_sag'),
            logo_boyutu=data.get('logo_boyutu', 80),
            puan_kutusu_boyutu=data.get('puan_kutusu_boyutu', 100),
            sik_boslugu=data.get('sik_boslugu', 16),
            siklar_arasi_bosluk=data.get('siklar_arasi_bosluk', 8),
            siklar_yatay_bosluk=data.get('siklar_yatay_bosluk', 24),
            ust_bosluk=data.get('ust_bosluk', 40),
            alt_bosluk=data.get('alt_bosluk', 40),
            baslik_katsayisi=data.get('baslik_katsayisi', 100)
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
        
        # Loglama
        su_an = datetime.now().strftime('%d.%m.%Y %H:%M:%S')
        print(f"📄 SINAV KAYDEDİLDİ: ID={yeni_sinav.id}, Tarih={su_an}")
        
        return jsonify({'basarili': True, 'mesaj': 'Sınav başarıyla kaydedildi', 'sinav_id': yeni_sinav.id})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/api/sinav-ayar-guncelle/<int:sinav_id>', methods=['POST'])
def sinav_ayar_guncelle(sinav_id):
    """Sınavın görsel/stil ayarlarını günceller"""
    sinav = SinavKagidi.query.get_or_404(sinav_id)
    try:
        data = request.json
        if 'puan_kutusu_boyutu' in data:
            sinav.puan_kutusu_boyutu = data['puan_kutusu_boyutu']
        if 'sik_boslugu' in data:
            sinav.sik_boslugu = data['sik_boslugu']
        if 'siklar_arasi_bosluk' in data:
            sinav.siklar_arasi_bosluk = data['siklar_arasi_bosluk']
        if 'baslik_katsayisi' in data:
            sinav.baslik_katsayisi = data['baslik_katsayisi']
        if 'siklar_yatay_bosluk' in data:
            sinav.siklar_yatay_bosluk = data['siklar_yatay_bosluk']
            
        if 'ust_bosluk' in data:
            sinav.ust_bosluk = data['ust_bosluk']
        if 'alt_bosluk' in data:
            sinav.alt_bosluk = data['alt_bosluk']
            
        db.session.commit()
        return jsonify({'basarili': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400



@app.route('/sinav-onizleme/<int:sinav_id>')
def sinav_onizleme(sinav_id):
    """Sınav kağıdı önizleme"""
    try:
        sinav = SinavKagidi.query.get_or_404(sinav_id)
        ayarlar = SinavAyarlari.query.first()
        ayarlar_imza = Ayarlar.query.first()
        return render_template('sinav_onizleme.html', sinav=sinav, ayarlar=ayarlar, ayarlar_imza=ayarlar_imza)
    except Exception as e:
        import traceback
        return f"<h3>Önizleme Hatası (500)</h3><p>Hata: {str(e)}</p><pre>{traceback.format_exc()}</pre>", 500

@app.route('/ayarlar')
def ayarlar():
    """Ayarlar sayfası"""
    ayarlar_obj = Ayarlar.query.first()
    
    # Sayaç Bilgilerini Çek
    istatistik = {
        'soru_toplam': Soru.query.count(),
        'soru_sayac': 0,
        'sinav_toplam': SinavKagidi.query.count(),
        'sinav_sayac': 0
    }
    
    try:
        # Sorular tablosu seq
        res_soru = db.session.execute(text("SELECT seq FROM sqlite_sequence WHERE name='sorular'")).scalar()
        if res_soru: istatistik['soru_sayac'] = res_soru
            
        # Sınav Kağıtları tablosu seq
        res_sinav = db.session.execute(text("SELECT seq FROM sqlite_sequence WHERE name='sinav_kagitlari'")).scalar()
        if res_sinav: istatistik['sinav_sayac'] = res_sinav
            
    except Exception as e:
        print(f"Sayaç okuma hatası: {e}")

    # Yüklenen Dosyaları Listele
    dosyalar_listesi = []
    try:
        klasor_yolu = app.config['UPLOAD_FOLDER']
        if os.path.exists(klasor_yolu):
            for dosya_adi in os.listdir(klasor_yolu):
                if dosya_adi.startswith('.'): continue
                
                tam_yol = os.path.join(klasor_yolu, dosya_adi)
                if os.path.isfile(tam_yol):
                    boyut = os.path.getsize(tam_yol)
                    zaman = os.path.getmtime(tam_yol)
                    tarih_str = datetime.fromtimestamp(zaman).strftime('%d.%m.%Y %H:%M')
                    
                    dosyalar_listesi.append({
                        'ad': dosya_adi,
                        'boyut': f"{boyut / 1024:.1f} KB",
                        'tarih': tarih_str,
                        'uzanti': dosya_adi.rsplit('.', 1)[1].lower() if '.' in dosya_adi else ''
                    })
            
            dosyalar_listesi.sort(key=lambda x: x['tarih'], reverse=True)
            
    except Exception as e:
        print(f"Dosya listeleme hatası: {e}")

    # Hazırlanan Sınavları Çek
    sinavlar = SinavKagidi.query.order_by(SinavKagidi.olusturma_tarihi.desc()).all()

    return render_template('ayarlar.html', ayarlar=ayarlar_obj, istatistik=istatistik, dosyalar=dosyalar_listesi, sinavlar=sinavlar)

@app.route('/sinav-sil/<int:sinav_id>', methods=['DELETE'])
def sinav_sil(sinav_id):
    """Sınav sil"""
    try:
        sinav = SinavKagidi.query.get_or_404(sinav_id)
        db.session.delete(sinav)
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Sınav başarıyla silindi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/api/tum-sinavlari-sil', methods=['POST'])
def tum_sinavlari_sil():
    """Tüm hazırlanan sınavları sil"""
    try:
        SinavKagidi.query.delete()
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Tüm sınavlar başarıyla silindi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

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
        soru.soru_tipi = data.get('soru_tipi', soru.soru_tipi)
        
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Soru güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400
@app.route('/api/sayac-sifirla', methods=['POST'])
def sayac_sifirla():
    """Belirtilen tablonun veya tüm tabloların ID sayacını sıfırlar"""
    try:
        data = request.json
        tablo = data.get('tablo')
        
        if not tablo:
            return jsonify({'basarili': False, 'mesaj': 'Tablo adı belirtilmedi'}), 400
            
        try:
            if tablo == 'hepsi':
                # Tüm sayaçları temizle
                db.session.execute(text("DELETE FROM sqlite_sequence"))
                mesaj = "Tüm sayaçlar başarıyla sıfırlandı."
            else:
                # Belirli bir tabloyu temizle
                gecerli_tablolar = {'sorular', 'sinav_kagitlari', 'sinav_ayarlari'}
                if tablo not in gecerli_tablolar:
                     return jsonify({'basarili': False, 'mesaj': 'Geçersiz tablo adı'}), 400
                     
                db.session.execute(text("DELETE FROM sqlite_sequence WHERE name = :tablo"), {'tablo': tablo})
                mesaj = f"{tablo} tablosunun sayacı sıfırlandı."
        except Exception as seq_err:
             print(f"Sayaç sıfırlama uyarısı: {seq_err}")
             mesaj = "Sayaç zaten başlangıç değerinde (İşlem Gerekmedi)."
            
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': mesaj})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 500
        
@app.route('/sinav-soru-sirala/<int:sinav_id>', methods=['POST'])
def sinav_soru_sirala(sinav_id):
    """Sınavdaki soruların sırasını günceller"""
    try:
        data = request.json
        yeni_siralamas = data.get('siralamas', []) # List of {soru_id: X, sira: Y}
        
        if not yeni_siralamas:
            return jsonify({'basarili': False, 'mesaj': 'Sıralama verisi eksik'}), 400
            
        for s in yeni_siralamas:
            soru_id = s.get('soru_id')
            yeni_sira = s.get('sira')
            
            sinav_sorusu = SinavSorusu.query.filter_by(sinav_id=sinav_id, soru_id=soru_id).first()
            if sinav_sorusu:
                sinav_sorusu.sira = yeni_sira
        
        db.session.commit()
        return jsonify({'basarili': True, 'mesaj': 'Sıralama güncellendi'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/sinav-soru-bosluk-guncelle/<int:sinav_id>/<int:soru_id>', methods=['POST'])
def sinav_soru_bosluk_guncelle(sinav_id, soru_id):
    """Bir sorunun üst boşluğunu günceller"""
    try:
        data = request.json
        ust_bosluk = data.get('ust_bosluk', 0)
        
        sinav_sorusu = SinavSorusu.query.filter_by(sinav_id=sinav_id, soru_id=soru_id).first()
        if sinav_sorusu:
            sinav_sorusu.ust_bosluk = int(ust_bosluk)
            db.session.commit()
            return jsonify({'basarili': True})
        return jsonify({'basarili': False, 'mesaj': 'Soru bulunamadı'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400


@app.route('/not-girisi')
def not_girisi():
    """Not Girişi Sayfası"""
    return render_template('not_girisi.html')

@app.route('/analiz/<string:kod>/<string:sube>')
def analiz_sayfasi(kod, sube):
    """Analiz Sayfası - Yeni Sekmede"""
    return render_template('analiz.html', kod=kod, sube=sube)

# --- YOKLAMA SİSTEMİ ROUTE'LARI ---

@app.route('/yoklama')
def yoklama_paneli():
    """Eğitmen Yoklama Paneli"""
    oturumlar = YoklamaOturumu.query.order_by(YoklamaOturumu.tarih.desc()).all()
    return render_template('yoklama.html', oturumlar=oturumlar)

@app.route('/api/yoklama/oturum-baslat', methods=['POST'])
def yoklama_oturum_baslat():
    """Yeni bir yoklama oturumu başlatır"""
    try:
        data = request.json
        yeni_oturum = YoklamaOturumu(
            baslik=data.get('baslik'),
            aciklama=data.get('aciklama'),
            gecerlilik_suresi=int(data.get('sure', 30)),
            hedef_lat=data.get('lat'),
            hedef_lng=data.get('lng'),
            tolerans_metre=int(data.get('tolerans', 100)),
            token_secret=os.urandom(16).hex()
        )
        db.session.add(yeni_oturum)
        db.session.commit()
        
        # Token oluştur (Kayıt formu için)
        token = create_access_token(identity=str(yeni_oturum.id), additional_claims={"secret": yeni_oturum.token_secret})
        
        return jsonify({'basarili': True, 'oturum_id': yeni_oturum.id, 'token': token})
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/api/yoklama/token-al/<int:oturum_id>')
def yoklama_token_al(oturum_id):
    """Belirli bir oturum için kayıt token'ı üretir"""
    oturum = YoklamaOturumu.query.get_or_404(oturum_id)
    token = create_access_token(identity=str(oturum.id), additional_claims={"secret": oturum.token_secret})
    return jsonify({'token': token})

@app.route('/api/yoklama/qr-kod/<token>')
def yoklama_qr_kod(token):
    """QR kod görseli üretir"""
    # Host bilgisini al (Katılımcıların formu açabilmesi için tam URL gerekiyor)
    base_url = request.host_url.rstrip('/')
    kayit_url = f"{base_url}/yoklama/kayit/{token}"
    
    img = qrcode.make(kayit_url)
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return base64.b64encode(img_io.getvalue()).decode()

@app.route('/yoklama/kayit/<token>')
def yoklama_kayit_formu(token):
    """Katılımcı Kayıt Formu (Mobil)"""
    try:
        # Token'ı doğrula
        decoded = decode_token(token)
        oturum_id = decoded['sub']
        oturum = YoklamaOturumu.query.get(oturum_id)
        
        if not oturum or not oturum.aktif:
            return "Bu yoklama oturumu artık geçerli değil.", 403
            
        return render_template('yoklama_kayit.html', token=token, oturum=oturum)
    except Exception as e:
        return f"Geçersiz veya süresi dolmuş bağlantı: {str(e)}", 400

@app.route('/api/yoklama/kaydet', methods=['POST'])
def yoklama_kaydet():
    """Katılımcı bilgisini doğrular ve kaydeder"""
    try:
        data = request.json
        token = data.get('token')
        
        # Token doğrula
        decoded = decode_token(token)
        oturum_id = decoded['sub']
        oturum = YoklamaOturumu.query.get(oturum_id)
        
        if not oturum or not oturum.aktif:
            return jsonify({'basarili': False, 'mesaj': 'Oturum kapalı veya geçersiz.'}), 403

        # Konum doğrulaması
        katilimci_lat = data.get('lat')
        katilimci_lng = data.get('lng')
        
        if oturum.hedef_lat and oturum.hedef_lng:
            if not katilimci_lat or not katilimci_lng:
                return jsonify({'basarili': False, 'mesaj': 'Konum bilgisi gerekli.'}), 400
            
            mesafe = haversine(oturum.hedef_lng, oturum.hedef_lat, katilimci_lng, katilimci_lat)
            
            if mesafe > oturum.tolerans_metre:
                return jsonify({'basarili': False, 'mesaj': f'Belirlenen alanın dışındasınız. ({int(mesafe)}m uzaktasınız)'}), 403
        else:
            mesafe = 0

        # Mükerrer Kayıt Kontrolü (Aynı oturumda aynı isim/numara)
        mevcut = YoklamaKayit.query.filter_by(
            oturum_id=oturum_id, 
            numara_kurum=data.get('numara_kurum')
        ).first()
        
        if mevcut:
            return jsonify({'basarili': False, 'mesaj': 'Daha önce kayıt yapılmış.'}), 400

        # Kaydet
        yeni_kayit = YoklamaKayit(
            oturum_id=oturum_id,
            ad_soyad=data.get('ad_soyad'),
            numara_kurum=data.get('numara_kurum'),
            lat=katilimci_lat,
            lng=katilimci_lng,
            mesafe=mesafe,
            ip_adresi=request.remote_addr,
            tarayici_bilgisi=request.headers.get('User-Agent')
        )
        db.session.add(yeni_kayit)
        db.session.commit()
        
        return jsonify({'basarili': True, 'mesaj': 'Kaydınız başarıyla alındı.'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'basarili': False, 'mesaj': str(e)}), 400

@app.route('/api/yoklama/katilimcilar/<int:oturum_id>')
def yoklama_katilimcilari(oturum_id):
    """Bir oturuma katılanları listeler"""
    kayitlar = YoklamaKayit.query.filter_by(oturum_id=oturum_id).order_by(YoklamaKayit.giris_saati.desc()).all()
    liste = []
    for k in kayitlar:
        liste.append({
            'ad_soyad': k.ad_soyad,
            'numara': k.numara_kurum,
            'saat': k.giris_saati.strftime('%H:%M:%S'),
            'mesafe': f"{int(k.mesafe)}m" if k.mesafe else "-"
        })
    return jsonify(liste)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, host='0.0.0.0', port=5001)
