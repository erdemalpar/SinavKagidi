from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        with db.engine.connect() as connection:
            connection.execute(text("ALTER TABLE sinav_kagitlari ADD COLUMN imza_metni VARCHAR(200) DEFAULT 'Öğr.Gör.Erdem ALPAR'"))
            connection.commit()
            print("Veritabanı güncellendi: 'imza_metni' sütunu eklendi.")
    except Exception as e:
        print(f"Hata: {e}")
