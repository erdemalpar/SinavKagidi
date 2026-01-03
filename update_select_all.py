import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_hazirlama.html')

def update_select_all():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. HTML Ekle
    html_code = """
            <!-- Toplu İşlemler -->
            <div class="px-6 pt-4 pb-2 flex items-center justify-between border-b border-gray-100 mb-2">
                 <span class="text-xs text-slate-400 font-medium uppercase tracking-wider">Soru Listesi</span>
                 <label class="flex items-center gap-2 cursor-pointer text-sm font-medium text-slate-600 hover:text-purple-600 select-none bg-slate-50 px-3 py-1.5 rounded-lg border border-slate-200 transition-colors">
                    <input type="checkbox" id="tumunuSecCheckbox" class="w-4 h-4 rounded text-purple-600 focus:ring-purple-500 border-gray-300" onchange="tumunuSecToggle(this)">
                    <span>Tümünü Seç</span>
                </label>
            </div>
    """
    
    target_html = '<!-- Sorular Listesi -->'
    if target_html in content and 'tumunuSecToggle' not in content:
        content = content.replace(target_html, html_code + '\n            ' + target_html)
        print("✓ HTML eklendi.")

    # 2. JS Ekle
    js_code = """
    function tumunuSecToggle(checkbox) {
        const checked = checkbox.checked;
        const gorunurKartlar = Array.from(document.querySelectorAll('.soru-kart')).filter(kart => kart.style.display !== 'none');
        
        gorunurKartlar.forEach(kart => {
            const soruId = parseInt(kart.dataset.soruId);
            const kartCheckbox = kart.querySelector('.soru-checkbox');
            
            if (checked) {
                // Seç (eğer seçili değilse)
                if (!secilenSorular.has(soruId)) {
                    secilenSorular.add(soruId);
                    kart.classList.add('soru-secili');
                    kartCheckbox.checked = true;
                }
            } else {
                // Kaldır (eğer seçiliyse)
                if (secilenSorular.has(soruId)) {
                    secilenSorular.delete(soruId);
                    kart.classList.remove('soru-secili');
                    kartCheckbox.checked = false;
                }
            }
        });
        
        secilenSorulariGuncelle();
        
        // Label Güncelleme
        checkbox.nextElementSibling.textContent = checked ? 'Tümünü Kaldır' : 'Tümünü Seç';
    }
    """
    
    if 'function tumunuSecToggle' not in content:
        last_script = content.rfind("</script>")
        if last_script != -1:
            content = content[:last_script] + js_code + "\n" + content[last_script:]
            print("✓ JS kodu eklendi.")
            
    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_select_all()
