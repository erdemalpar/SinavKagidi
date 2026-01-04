from app import app, db
from sqlalchemy import text

with app.app_context():
    try:
        with db.engine.connect() as connection:
            connection.execute(text('ALTER TABLE sinav_kagitlari ADD COLUMN saat VARCHAR(10)'))
            connection.commit()
            print("Veritabanı güncellendi: 'saat' sütunu eklendi.")
    except Exception as e:
        print(f"Hata: {e}")
