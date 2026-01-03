from app import app, db
from sqlalchemy import text

def update_db():
    with app.app_context():
        with db.engine.connect() as conn:
            try:
                # Sütunları eklemeye çalış
                print("Sütunlar ekleniyor...")
                conn.execute(text("ALTER TABLE sorular ADD COLUMN gorsel_konum VARCHAR(20) DEFAULT 'arada'"))
                conn.execute(text("ALTER TABLE sorular ADD COLUMN sik_duzeni VARCHAR(20) DEFAULT 'alt_alta'"))
                print("✓ Sütunlar başarıyla eklendi.")
            except Exception as e:
                # Eğer sütunlar zaten varsa hata verebilir, yoksay
                print(f"Bilgi: {e}")
                print("Sütunlar zaten var olabilir veya başka bir hata oluştu.")

if __name__ == "__main__":
    update_db()
