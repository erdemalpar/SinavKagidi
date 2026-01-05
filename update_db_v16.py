
import os
import sqlite3

db_path = os.path.join(os.getcwd(), 'instance', 'sinav_kagidi.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # SinavKagidi tablosuna yeni sütun ekle
    cursor.execute("ALTER TABLE sinav_kagitlari ADD COLUMN sayfa2_ust_bosluk INTEGER DEFAULT 40")
    print("sayfa2_ust_bosluk sütunu başarıyla eklendi.")
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e).lower():
        print("Sütun zaten mevcut.")
    else:
        print(f"Hata oluştu: {e}")

conn.commit()
conn.close()
