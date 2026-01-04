from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Soru(db.Model):
    """Soru bankası tablosu"""
    __tablename__ = 'sorular'
    
    id = db.Column(db.Integer, primary_key=True)
    soru_metni = db.Column(db.Text, nullable=False)
    secenek_a = db.Column(db.Text)
    secenek_b = db.Column(db.Text)
    secenek_c = db.Column(db.Text)
    secenek_d = db.Column(db.Text)
    secenek_e = db.Column(db.Text)
    dogru_cevap = db.Column(db.String(1))  # A, B, C, D, E
    konu = db.Column(db.String(200))
    zorluk = db.Column(db.String(50), default='Orta')  # Kolay, Orta, Zor
    puan = db.Column(db.Integer, default=5)
    gorsel_yolu = db.Column(db.String(500))  # Soru görseli varsa
    gorsel_konum = db.Column(db.String(20), default='arada')  # ustte, arada, yanda
    sik_duzeni = db.Column(db.String(20), default='alt_alta')  # alt_alta, yan_yana
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    sinav_sorulari = db.relationship('SinavSorusu', back_populates='soru', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Soru {self.id}: {self.soru_metni[:50]}...>'
    
    def sozluk_olustur(self):
        """Soru nesnesini sözlüğe çevir"""
        return {
            'id': self.id,
            'soru_metni': self.soru_metni,
            'secenek_a': self.secenek_a,
            'secenek_b': self.secenek_b,
            'secenek_c': self.secenek_c,
            'secenek_d': self.secenek_d,
            'secenek_e': self.secenek_e,
            'dogru_cevap': self.dogru_cevap,
            'konu': self.konu,
            'zorluk': self.zorluk,
            'puan': self.puan,
            'gorsel_yolu': self.gorsel_yolu,
            'gorsel_konum': self.gorsel_konum,
            'sik_duzeni': self.sik_duzeni,
            'olusturma_tarihi': self.olusturma_tarihi.isoformat() if self.olusturma_tarihi else None
        }


class SinavAyarlari(db.Model):
    """Sınav kağıdı antet ayarları"""
    __tablename__ = 'sinav_ayarlari'
    
    id = db.Column(db.Integer, primary_key=True)
    okul_adi = db.Column(db.String(200), default='Okul Adı')
    egitim_yili = db.Column(db.String(50), default='2025-2026')
    donem = db.Column(db.String(100), default='1. Dönem 1. Yazılı')
    tarih = db.Column(db.String(50))
    salon = db.Column(db.String(50))
    puan_goster = db.Column(db.Boolean, default=True)
    logo_yolu = db.Column(db.String(500))
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<SinavAyarlari {self.okul_adi} - {self.egitim_yili}>'
    
    def sozluk_olustur(self):
        """Ayarları sözlüğe çevir"""
        return {
            'id': self.id,
            'okul_adi': self.okul_adi,
            'egitim_yili': self.egitim_yili,
            'donem': self.donem,
            'tarih': self.tarih,
            'salon': self.salon,
            'puan_goster': self.puan_goster,
            'logo_yolu': self.logo_yolu
        }


class SinavKagidi(db.Model):
    """Oluşturulan sınav kağıtları"""
    __tablename__ = 'sinav_kagitlari'
    
    id = db.Column(db.Integer, primary_key=True)
    baslik = db.Column(db.String(200), nullable=True) # Artık zorunlu değil (App seviyesinde)
    egitim_yili = db.Column(db.String(50))
    donem = db.Column(db.String(100))
    aciklama = db.Column(db.Text)
    tarih = db.Column(db.String(50))
    saat = db.Column(db.String(10)) # Sınav saati
    # Görünüm Ayarları
    okul_adi = db.Column(db.String(200))
    yazi_fontu = db.Column(db.String(100), default='font-sans')
    yazi_boyutu = db.Column(db.Integer, default=12)
    yazi_rengi = db.Column(db.String(20), default='#000000')
    yazi_stili = db.Column(db.String(20), default='normal')
    gorsel_boyutu = db.Column(db.Integer, default=100) # Yüzde olarak
    logo_sol = db.Column(db.String(500))
    logo_sag = db.Column(db.String(500))
    logo_boyutu = db.Column(db.Integer, default=80) # Pixel olarak
    imza_metni = db.Column(db.String(200), default='Öğr.Gör.Erdem ALPAR')
    
    olusturma_tarihi = db.Column(db.DateTime, default=datetime.utcnow)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # İlişkiler
    sorular = db.relationship('SinavSorusu', back_populates='sinav', cascade='all, delete-orphan', order_by='SinavSorusu.sira')
    
    def __repr__(self):
        return f'<SinavKagidi {self.id}: {self.baslik}>'
    
    def sozluk_olustur(self):
        """Sınav kağıdını sözlüğe çevir"""
        return {
            'id': self.id,
            'baslik': self.baslik,
            'aciklama': self.aciklama,
            'soru_sayisi': len(self.sorular),
            'toplam_puan': sum([ss.soru.puan for ss in self.sorular if ss.soru]),
            'olusturma_tarihi': self.olusturma_tarihi.isoformat() if self.olusturma_tarihi else None
        }


class SinavSorusu(db.Model):
    """Sınav kağıdı ile sorular arasındaki ilişki tablosu"""
    __tablename__ = 'sinav_sorulari'
    
    id = db.Column(db.Integer, primary_key=True)
    sinav_id = db.Column(db.Integer, db.ForeignKey('sinav_kagitlari.id'), nullable=False)
    soru_id = db.Column(db.Integer, db.ForeignKey('sorular.id'), nullable=False)
    sira = db.Column(db.Integer, default=1)  # Sorunun sınav kağıdındaki sırası
    ozel_puan = db.Column(db.Integer)  # Bu sınav için özel puan (opsiyonel)
    
    # İlişkiler
    sinav = db.relationship('SinavKagidi', back_populates='sorular')
    soru = db.relationship('Soru', back_populates='sinav_sorulari')
    
    def __repr__(self):
        return f'<SinavSorusu Sınav:{self.sinav_id} Soru:{self.soru_id} Sıra:{self.sira}>'


class Ayarlar(db.Model):
    """Genel uygulama ayarları"""
    __tablename__ = 'ayarlar'
    
    id = db.Column(db.Integer, primary_key=True)
    imza_metni = db.Column(db.String(200), default='Öğr.Gör.Erdem ALPAR')
    cizgi_rengi = db.Column(db.String(7), default='#CCCCCC')
    cizgi_kalinlik = db.Column(db.Float, default=1.0)
    metin_boyutu = db.Column(db.Integer, default=12)
    guncelleme_tarihi = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Ayarlar {self.imza_metni}>'
    
    def sozluk_olustur(self):
        return {
            'id': self.id,
            'imza_metni': self.imza_metni,
            'cizgi_rengi': self.cizgi_rengi,
            'cizgi_kalinlik': self.cizgi_kalinlik,
            'metin_boyutu': self.metin_boyutu
        }
