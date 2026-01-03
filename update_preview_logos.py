import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_onizleme.html')

def update_preview_logos():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    start_marker = '<header class="border-b-4 border-slate-900 pb-6 mb-8 text-center">'
    end_marker = '<!-- Öğrenci Bilgi Alanı -->'
    
    new_header_content = """<header class="border-b-4 border-slate-900 pb-6 mb-8">
                    <div class="flex items-center justify-between gap-4">
                        <!-- Sol Logo -->
                        <div class="w-[150px] flex-shrink-0 text-left flex justify-start">
                            {% if sinav.logo_sol %}
                            <img src="{{ sinav.logo_sol }}" alt="" style="height: {{ sinav.logo_boyutu }}px; width: auto; max-width: 100%; object-fit: contain;">
                            {% endif %}
                        </div>
                        
                        <!-- Orta Metin -->
                        <div class="flex-1 text-center">
                            <h1 class="text-2xl font-black text-slate-900 tracking-tight mb-2 uppercase leading-tight">{{ sinav.okul_adi or ayarlar.okul_adi or "" }}</h1>
            
                            <h2 class="text-lg font-bold text-slate-700 mb-1 leading-snug">
                                {{ ayarlar.egitim_yili }} Eğitim Öğretim Yılı {{ ayarlar.donem }} {{ sinav.baslik }}
                            </h2>
                        </div>
                
                        <!-- Sağ Logo -->
                        <div class="w-[150px] flex-shrink-0 text-right flex justify-end">
                            {% if sinav.logo_sag %}
                            <img src="{{ sinav.logo_sag }}" alt="" style="height: {{ sinav.logo_boyutu }}px; width: auto; max-width: 100%; object-fit: contain;">
                            {% endif %}
                        </div>
                    </div>
    """
    
    if start_marker in content and 'logo_sol' not in content:
        parts = content.split(start_marker)
        if len(parts) > 1:
            sub_parts = parts[1].split(end_marker)
            new_content = parts[0] + new_header_content + "\n                " + end_marker + sub_parts[1]
            content = new_content
            print("✓ Önizleme header yapısı güncellendi.")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_preview_logos()
