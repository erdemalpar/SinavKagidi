from app import app, db, Soru
from dosya_isleme import json_isle
import os

def verileri_ice_aktar():
    with app.app_context():
        json_yolu = 'temp_sorular.json'
        if not os.path.exists(json_yolu):
            print("Dosya bulunamadı!")
            return
            
        # dosya_isleme.py içindeki yeni json_isle fonksiyonunu kullanıyoruz
        sorular_data = json_isle(json_yolu)
        print(f"{len(sorular_data)} soru işlenmeye hazır.")
        
        eklenen = 0
        mukerrer = 0
        
        for s_data in sorular_data:
            metin = s_data.get('soru_metni')
            # Mükerrer kontrolü (Soru metnine göre)
            mevcut = Soru.query.filter_by(soru_metni=metin).first()
            if mevcut:
                mukerrer += 1
                continue
                
            yeni_soru = Soru(
                soru_metni=metin,
                secenek_a=s_data.get('secenek_a'),
                secenek_b=s_data.get('secenek_b'),
                secenek_c=s_data.get('secenek_c'),
                secenek_d=s_data.get('secenek_d'),
                secenek_e=s_data.get('secenek_e'),
                dogru_cevap=s_data.get('dogru_cevap', 'A'),
                konu=s_data.get('konu', ''),
                zorluk=s_data.get('zorluk', 'Orta'),
                puan=s_data.get('puan', 5),
                gorsel_konum=s_data.get('gorsel_konum', 'yanda'),
                sik_duzeni=s_data.get('sik_duzeni', 'iki_sutun')
            )
            db.session.add(yeni_soru)
            eklenen += 1
            
        db.session.commit()
        print(f"✅ İşlem tamamlandı: {eklenen} soru eklendi, {mukerrer} mükerrer soru atlandı.")

if __name__ == "__main__":
    verileri_ice_aktar()
