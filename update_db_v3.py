from app import app, db
from sqlalchemy import text

def update_db_v3():
    with app.app_context():
        with db.engine.connect() as conn:
            try:
                # Add columns to sinav_kagitlari
                columns = [
                    ("okul_adi", "VARCHAR(200)"),
                    ("yazi_fontu", "VARCHAR(100)"),
                    ("yazi_boyutu", "INTEGER"),
                    ("yazi_rengi", "VARCHAR(20)"),
                    ("yazi_stili", "VARCHAR(20)"),
                    ("gorsel_boyutu", "INTEGER")
                ]
                
                for col_name, col_type in columns:
                    try:
                        conn.execute(text(f"ALTER TABLE sinav_kagitlari ADD COLUMN {col_name} {col_type}"))
                        print(f"✓ {col_name} eklendi.")
                    except Exception as e:
                        print(f"Bilgi: {col_name} zaten var veya hata: {e}")
                        
                print("Veritabanı güncellemesi tamamlandı.")
            except Exception as e:
                print(f"Genel Hata: {e}")

if __name__ == "__main__":
    update_db_v3()
