import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_hazirlama.html')

def update_sinav_hazirlama_v2():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. HTML: Yeni Paneli Ekle
    new_panel_html = """
        <!-- Görünüm Ayarları -->
        <div class="bg-white rounded-2xl shadow-lg overflow-hidden mt-6">
            <div class="bg-gradient-to-r from-purple-500 to-indigo-600 p-4 text-white">
                <h2 class="text-xl font-bold flex items-center gap-2">
                    <i data-lucide="palette" class="w-6 h-6"></i>
                    Görünüm Ayarları
                </h2>
            </div>
            <div class="p-4 space-y-4">
                <!-- Okul Adı -->
                <div>
                    <label class="block text-sm font-medium text-slate-700 mb-2">Okul Adı (Kağıtta Görünecek)</label>
                    <input type="text" id="sinavOkulAdi" placeholder="{{ ayarlar.okul_adi if ayarlar else 'Okul Adı Giriniz' }}" 
                           class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none transition-all">
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Yazı Tipi -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-2">Yazı Tipi</label>
                        <select id="sinavYaziFontu" class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none transition-all">
                            <option value="font-sans">Arial / Sans Serif</option>
                            <option value="font-serif">Times New Roman / Serif</option>
                            <option value="font-mono">Courier / Monospace</option>
                        </select>
                    </div>
                
                    <!-- Yazı Boyutu -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-2">Yazı Boyutu (px)</label>
                        <input type="number" id="sinavYaziBoyutu" value="12" min="8" max="24"
                               class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none transition-all">
                    </div>
                </div>

                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <!-- Yazı Rengi -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-2">Yazı Rengi</label>
                        <div class="flex items-center gap-2">
                            <input type="color" id="sinavYaziRengi" value="#000000" class="h-10 w-full cursor-pointer rounded-lg border-2 border-slate-200 p-1">
                        </div>
                    </div>
                    
                    <!-- Yazı Stili -->
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-2">Yazı Stili</label>
                         <select id="sinavYaziStili" class="w-full px-4 py-2 border-2 border-slate-200 rounded-lg focus:border-purple-500 focus:outline-none transition-all">
                            <option value="normal">Normal</option>
                            <option value="bold">Kalın (Bold)</option>
                        </select>
                    </div>
                </div>

                <!-- Resim Boyutu -->
                <div>
                     <label class="block text-sm font-medium text-slate-700 mb-2 flex justify-between">
                        <span>Görsel Boyutu (Sorulardaki Resimler)</span>
                        <span class="text-slate-500" id="gorselBoyutuLabel">%100</span>
                    </label>
                    <input type="range" id="sinavGorselBoyutu" min="20" max="100" value="100" 
                           class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
                           oninput="document.getElementById('gorselBoyutuLabel').textContent = '%' + this.value">
                </div>
            </div>
        </div>
    """
    
    # "Sınav Bilgileri" panelinin kapanış div'inden sonra eklemek lazım.
    # Dosyadaki yapı şöyle: <!-- Sınav Bilgileri --> ... </div> (panel kapanış)
    # 120. satır civarı.
    
    # Panel kapanış divini bulmak için, "sinavAciklama" textarea'sının olduğu div'den sonraki 2. kapanış divi.
    # String replace ile yapmak riskli olabilir mi?
    # En güvenli anchor: <!-- Seçilen Sorular --> başlangıcından hemen öncesi.
    
    anchor = '<!-- Seçilen Sorular -->'
    if anchor in content and 'id="sinavOkulAdi"' not in content:
        content = content.replace(anchor, new_panel_html + "\n\n        " + anchor)
        print("✓ HTML Panel Eklendi.")
    
    # 2. JS: Data toplama
    js_anchor = "tarih: document.getElementById('sinavTarih').value,"
    js_new_fields = """
            okul_adi: document.getElementById('sinavOkulAdi').value,
            yazi_fontu: document.getElementById('sinavYaziFontu').value,
            yazi_boyutu: document.getElementById('sinavYaziBoyutu').value,
            yazi_rengi: document.getElementById('sinavYaziRengi').value,
            yazi_stili: document.getElementById('sinavYaziStili').value,
            gorsel_boyutu: document.getElementById('sinavGorselBoyutu').value,"""
            
    if js_anchor in content and 'okul_adi:' not in content:
        content = content.replace(js_anchor, js_anchor + js_new_fields)
        print("✓ JS Data alanları güncellendi.")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_sinav_hazirlama_v2()
