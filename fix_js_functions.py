import os

# Base URL
BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'soru_bankasi.html')

def fix_js_functions():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    js_to_add = ""

    # 1. Kapat Soru Güncelle Modal
    if "function kapatSoruGuncelleModal" not in content:
        print("Eksik fonksiyon ekleniyor: kapatSoruGuncelleModal")
        js_to_add += """
    function kapatSoruGuncelleModal() {
        document.getElementById('soruGuncelleModal').classList.add('hidden');
    }
    """

    # 2. Kapat Soru Ekle Modal (Eğer silindiyse)
    if "function kapatSoruEkleModal" not in content:
        print("Eksik fonksiyon ekleniyor: kapatSoruEkleModal")
        js_to_add += """
    function kapatSoruEkleModal() {
        document.getElementById('soruEkleModal').classList.add('hidden');
        document.getElementById('soruEkleForm').reset();
    }
    """

    # 3. İkon Yükleme (Gecikmeli)
    # Modal açıldığında ikonların yüklenmesi için global bir helper iyi olur
    # Ancak mevcut kodlarda setTimeout ile yapılmış, sorun yok.

    if js_to_add:
        # Scriptin sonuna ekle
        last_script_tag = content.rfind("</script>")
        if last_script_tag != -1:
            content = content[:last_script_tag] + js_to_add + "\n" + content[last_script_tag:]
            
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ JS fonksiyonları dosyaya eklendi.")
        else:
            print("⚠ <script> etiketi bulunamadı!")
    else:
        print("Tüm fonksiyonlar zaten mevcut.")

if __name__ == "__main__":
    fix_js_functions()
