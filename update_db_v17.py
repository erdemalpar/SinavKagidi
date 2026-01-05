
import os
import sqlite3

db_path = os.path.join(os.getcwd(), 'instance', 'sinav_kagidi.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    # Sınavdaki her bir soru için özel üst boşluk ayarı
    cursor.execute("ALTER TABLE sinav_sorulari ADD COLUMN ust_bosluk INTEGER DEFAULT 0")
    print("sinav_sorulari tablosuna ust_bosluk sütunu başarıyla eklendi.")
except sqlite3.OperationalError as e:
    print(f"Hata veya Sütun Mevcut: {e}")

conn.commit()
conn.close()
