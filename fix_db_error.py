from app import app, db
from models import Ayarlar

with app.app_context():
    try:
        db.create_all()
        print("Tablolar oluşturuldu (varsa eksikler).")
        
        # Ayarlar tablosunu kontrol et
        if not Ayarlar.query.first():
            print("Ayarlar tablosu boş, varsayılan kayıt oluşturuluyor...")
            varsayilan = Ayarlar(imza_metni="Öğr.Gör.Erdem ALPAR")
            db.session.add(varsayilan)
            db.session.commit()
            print("Varsayılan ayarlar eklendi.")
        else:
            print("Ayarlar tablosu zaten dolu.")
            
    except Exception as e:
        print(f"Hata: {e}")
