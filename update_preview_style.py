import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_onizleme.html')

def update_preview_style():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Okul Adı Değişimi
    old_school = '{{ ayarlar.okul_adi }}'
    new_school = '{{ sinav.okul_adi or ayarlar.okul_adi }}'
    
    if old_school in content:
        content = content.replace(old_school, new_school)
        print("✓ Okul adı logic güncellendi.")

    # 2. Stil Uygulaması
    # Mevcut class'ın önüne style attribute ekle
    style_attr = 'style="font-family: {{ sinav.yazi_fontu }}; font-size: {{ sinav.yazi_boyutu }}px; color: {{ sinav.yazi_rengi }}; font-weight: {{ sinav.yazi_stili }};" '
    
    target_div = 'id="kagitt" class="'
    if target_div in content and 'style="font-family' not in content:
        content = content.replace(target_div, style_attr + target_div)
        print("✓ Kağıt stili eklendi.")
        
    # 3. Görsel Boyutu
    # Tüm soru görsellerine style ekle
    img_tag_start = '<img src="{{ soru.gorsel_yolu }}"'
    img_style = ' style="max-height: 240px; width: {{ sinav.gorsel_boyutu }}%; object-fit: contain;"'
    
    if img_tag_start in content and 'width: {{ sinav.gorsel_boyutu }}%' not in content:
        content = content.replace(img_tag_start, img_tag_start + img_style)
        print("✓ Görsel boyutu stili eklendi.")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_preview_style()
