from app import app, db
from sqlalchemy import text

def update_db_v5():
    with app.app_context():
        with db.engine.connect() as conn:
            try:
                # Add columns to sinav_kagitlari
                columns = [
                    ("egitim_yili", "VARCHAR(50)"),
                    ("donem", "VARCHAR(100)")
                ]
                
                for col_name, col_type in columns:
                    try:
                        conn.execute(text(f"ALTER TABLE sinav_kagitlari ADD COLUMN {col_name} {col_type}"))
                        print(f"✓ {col_name} eklendi.")
                    except Exception as e:
                        print(f"Bilgi: {col_name} zaten var.")
                        
                print("Veritabanı güncellemesi tamamlandı.")
            except Exception as e:
                print(f"Genel Hata: {e}")

if __name__ == "__main__":
    update_db_v5()
