import os

# Base URL
BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_hazirlama.html')

def update_sinav_hazirlama():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. HTML: Tarih Inputu Ekle
    input_html = """
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-2">Sınav Tarihi</label>
                    <input type="text" id="sinavTarih" placeholder="Örn: 20 Mayıs 2026"
                        class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none transition-all">
                </div>"""
                
    target_html = """                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-2">Açıklama (Opsiyonel)</label>
                    <textarea id="sinavAciklama" rows="2" placeholder="Sınav hakkında notlar..."
                        class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none"></textarea>
                </div>"""
    
    if 'id="sinavTarih"' not in content:
        content = content.replace(target_html, target_html + "\n" + input_html)
        print("HTML input eklendi.")

    # 2. JS: Sınav Kaydet
    target_js = """            aciklama: document.getElementById('sinavAciklama').value,"""
    new_js = """            aciklama: document.getElementById('sinavAciklama').value,
            tarih: document.getElementById('sinavTarih').value,"""
            
    if 'tarih: document.getElementById' not in content:
        content = content.replace(target_js, new_js)
        print("JS güncellendi.")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_sinav_hazirlama()
