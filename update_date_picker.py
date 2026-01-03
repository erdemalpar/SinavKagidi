import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_hazirlama.html')

def update_date_picker():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    old_input_part = 'type="text" id="sinavTarih"'
    new_input_part = 'type="date" id="sinavTarih"'
    
    if old_input_part in content:
        content = content.replace(old_input_part, new_input_part)
        content = content.replace('placeholder="Örn: 20 Mayıs 2026"', '')
        
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print("✓ Tarih alanı takvime çevrildi.")
    else:
        print("Bilgi: Tarih alanı zaten güncel veya bulunamadı.")

if __name__ == "__main__":
    update_date_picker()
