import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_onizleme.html')

def update_preview_style_v2():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # Stil Uygulaması
    style_attr = 'style="font-family: {{ sinav.yazi_fontu or "inherit" }}; font-size: {{ sinav.yazi_boyutu or 12 }}px; color: {{ sinav.yazi_rengi or "#000000" }}; font-weight: {{ sinav.yazi_stili or "normal" }};" '
    
    target_div = '<div id="sinavKagidi" class="sinav-kagidi">'
    
    if target_div in content:
        # Style zaten var mı kontrol et (basitçe)
        if 'style="font-family' not in content:
            new_div = f'<div id="sinavKagidi" {style_attr}class="sinav-kagidi">'
            content = content.replace(target_div, new_div)
            
            with open(FILE_PATH, 'w', encoding='utf-8') as f:
                f.write(content)
            print("✓ Kağıt stili düzeltildi ve eklendi.")
        else:
            print("Bilgi: Stil zaten eklenmiş görünüyor.")
    else:
        print(f"Hata: Hedef div '{target_div}' bulunamadı.")

if __name__ == "__main__":
    update_preview_style_v2()
