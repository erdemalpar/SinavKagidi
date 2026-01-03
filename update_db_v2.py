from app import app, db
from sqlalchemy import text

def update_db_v2():
    with app.app_context():
        with db.engine.connect() as conn:
            try:
                # sinav_kagitlari tablosuna tarih sütunu ekle
                print("Sütun ekleniyor...")
                conn.execute(text("ALTER TABLE sinav_kagitlari ADD COLUMN tarih VARCHAR(50)"))
                print("✓ Sütun başarıyla eklendi.")
            except Exception as e:
                print(f"Bilgi: {e}")
                print("Sütun zaten var olabilir.")

if __name__ == "__main__":
    update_db_v2()
