import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_onizleme.html')

def update_preview_titles():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    start_h2 = '<h2 class="text-lg font-bold text-slate-700 mb-1 leading-snug">'
    end_h2 = '</h2>'
    
    new_titles = """<h2 class="text-lg font-bold text-slate-700 mb-0.5 leading-snug uppercase">
                                {{ sinav.egitim_yili or ayarlar.egitim_yili }} Eğitim Öğretim Yılı
                            </h2>

                            <h3 class="text-base font-bold text-slate-700 mb-0.5 leading-snug uppercase">
                                {{ sinav.donem or ayarlar.donem }}
                            </h3>

                            {% if sinav.baslik %}
                            <h4 class="text-base font-bold text-slate-700 leading-snug">
                                {{ sinav.baslik }}
                            </h4>
                            {% endif %}"""

    if start_h2 in content:
        p1 = content.split(start_h2)
        p2 = p1[1].split(end_h2, 1)
        
        content = p1[0] + new_titles + p2[1]
        print("✓ Başlık hiyerarşisi güncellendi.")
    else:
        print("Hata: h2 etiketi bulunamadı.")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_preview_titles()
