import os

# Base URL
BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'soru_bankasi.html')

def fix_script_order():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Include satırını bul
    include_line = "{% include '_soru_guncelle_modal.html' %}"
    
    if include_line in content:
        # Include satırını sil
        content = content.replace(include_line, "")
        
        # Script taginden önceye ekle
        # Dosyada muhtemelen bir tane <script> tagi var (benim eklediğim).
        # Ancak base.html'den gelen scriptler de olabilir mi? Hayır bu child template.
        
        # En mantıklı yer: <!-- Dosya Yükleme Modalı --> nın hemen öncesi.
        # Veya <!-- Soru Ekleme Modalı --> nın öncesi.
        # Modallar body'nin direk çocuğu gibi dursun.
        
        # En basit ve güvenli yer: {% endblock %} öncesine script geliyor. Script'ten hemen önceye ekleyelim.
        # Script başlangıcı: <script>
        
        # Ancak birden fazla script tagi olabilir mi?
        # Benim update_ui fonksiyonlarında replace yaparken dikkat ettim.
        
        # <script> tagini bulup hemen öncesine ekleyelim.
        # Content'i sondan başa doğru arayalım
        last_script_index = content.rfind("<script")
        
        if last_script_index != -1:
            content = content[:last_script_index] + include_line + "\n\n" + content[last_script_index:]
            print("✓ Include satırı scriptten önceye taşındı.")
        else:
            print("⚠ <script> etiketi bulunamadı, işlem yapılmadı.")
            # Belki de script yoktur? Ama JS hatası alıyoruz.
            return
            
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == "__main__":
    fix_script_order()
