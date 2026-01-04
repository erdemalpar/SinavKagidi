import sqlite3
import os

def migrate():
    db_path = 'instance/sinav_kagidi.db'
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(sinav_kagitlari)")
        columns = [info[1] for info in cursor.fetchall()]
        
        if 'ust_bosluk' not in columns:
            print("Adding 'ust_bosluk' column...")
            cursor.execute("ALTER TABLE sinav_kagitlari ADD COLUMN ust_bosluk INTEGER DEFAULT 40")
        else:
            print("'ust_bosluk' column already exists.")

        if 'alt_bosluk' not in columns:
            print("Adding 'alt_bosluk' column...")
            cursor.execute("ALTER TABLE sinav_kagitlari ADD COLUMN alt_bosluk INTEGER DEFAULT 40")
        else:
            print("'alt_bosluk' column already exists.")
            
        conn.commit()
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()

if __name__ == '__main__':
    migrate()
