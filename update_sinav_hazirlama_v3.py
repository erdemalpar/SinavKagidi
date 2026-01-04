import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_hazirlama.html')

def update_sinav_hazirlama_v3():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    html_to_add = """
                <!-- Eğitim Yılı ve Dönem -->
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-2">Eğitim - Öğretim Yılı</label>
                        <input type="text" id="sinavEgitimYili" value="{{ ayarlar.egitim_yili }}" placeholder="Örn: 2025-2026"
                               class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none transition-all">
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-2">Dönem / Yazılı Bilgisi</label>
                        <input type="text" id="sinavDonem" value="{{ ayarlar.donem }}" placeholder="Örn: 1. Dönem 1. Yazılı"
                               class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none transition-all">
                    </div>
                </div>
    """
    
    if 'id="sinavEgitimYili"' not in content:
        lines = content.split('\n')
        new_lines = []
        added = False
        
        for i, line in enumerate(lines):
            if 'Sınav Başlığı</label>' in line and not added:
                 # Bir önceki satır muhtemelen `<div>` dir.
                 if i > 0 and '<div>' in lines[i-1]:
                     new_lines.pop() # Remove last <div>
                     new_lines.append(html_to_add) # Add new HTML
                     new_lines.append('<div>') # Add removed <div> back
                 else:
                     new_lines.append(html_to_add)
                 
                 new_lines.append(line)
                 added = True
            else:
                new_lines.append(line)
        
        content = '\n'.join(new_lines)
        print("✓ HTML Eğitim Yılı alanları eklendi.")

    js_data_anchor = "aciklama: document.getElementById('sinavAciklama').value,"
    js_data_new = """
            egitim_yili: document.getElementById('sinavEgitimYili').value,
            donem: document.getElementById('sinavDonem').value,"""
            
    if js_data_anchor in content and 'egitim_yili:' not in content:
        content = content.replace(js_data_anchor, js_data_anchor + js_data_new)
        print("✓ JS Data alanları güncellendi.")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_sinav_hazirlama_v3()
