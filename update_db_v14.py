import sqlite3
import os

db_path = 'instance/sinav_kagidi.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # soru_tipi kolonunu ekle
        cursor.execute("ALTER TABLE sorular ADD COLUMN soru_tipi VARCHAR(20) DEFAULT 'test'")
        conn.commit()
        print("✅ 'soru_tipi' kolonu 'sorular' tablosuna başarıyla eklendi.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("ℹ️ 'soru_tipi' kolonu zaten mevcut.")
        else:
            print(f"❌ Hata: {e}")
    finally:
        conn.close()
else:
    print(f"❌ Veritabanı dosyası bulunamadı: {db_path}")
