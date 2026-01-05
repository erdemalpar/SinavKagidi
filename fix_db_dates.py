import sys
import os
from datetime import timedelta
from app import app, db
from models import SinavKagidi, Soru, SinavAyarlari

def fix_dates():
    with app.app_context():
        print("--- Veritabanı Tarih Düzeltme İşlemi Başladı ---")
        
        # Sınav Kağıtları
        sinavlar = SinavKagidi.query.all()
        for s in sinavlar:
            if s.olusturma_tarihi:
                # Eğer tarih dünkü ise ve gece yarısına yakınsa dünü gösteriyor olabilir.
                # UTC'den Yerel Saate (GMT+3) geçiş için +3 saat ekliyoruz.
                eski_tarih = s.olusturma_tarihi
                yeni_tarih = s.olusturma_tarihi + timedelta(hours=3)
                s.olusturma_tarihi = yeni_tarih
                print(f"Sınav {s.id}: {eski_tarih} -> {yeni_tarih}")
        
        # Sorular
        sorular = Soru.query.all()
        for s in sorular:
            if s.olusturma_tarihi:
                s.olusturma_tarihi += timedelta(hours=3)
            if s.guncelleme_tarihi:
                s.guncelleme_tarihi += timedelta(hours=3)
        
        db.session.commit()
        print("--- İşlem Başarıyla Tamamlandı ---")

if __name__ == "__main__":
    fix_dates()
