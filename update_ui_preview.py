import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
SORU_BANKASI_PATH = os.path.join(BASE_DIR, 'soru_bankasi.html')
MODAL_PATH = os.path.join(BASE_DIR, '_soru_guncelle_modal.html')

def update_ui_preview():
    # 1. _soru_guncelle_modal.html Güncelleme (HTML)
    with open(MODAL_PATH, 'r', encoding='utf-8') as f:
        modal_content = f.read()
    
    preview_html_guncelle = """
            <div class="mt-8 border-t pt-6">
                <h3 class="text-sm font-bold text-slate-500 uppercase mb-4 flex items-center gap-2">
                    <i data-lucide="eye" class="w-4 h-4"></i> Kağıt Görünümü Önizleme
                </h3>
                <div class="bg-white border border-slate-200 p-8 rounded-xl shadow-sm relative overflow-hidden group">
                    <div class="absolute inset-0 opacity-[0.02] pointer-events-none" style="background-image: radial-gradient(#000 1px, transparent 1px); background-size: 20px 20px;"></div>
                    <div id="guncelleCanliOnizleme" class="relative z-10 font-serif">
                        <!-- JS ile dolar -->
                    </div>
                </div>
            </div>
    """
    
    # Form'un bitişinden önce ekleyelim (<div class="flex justify-end gap-3 pt-4 border-t"> öncesi)
    # _soru_guncelle_modal.html yapısına bakmak lazım. Button grubu genelde formun sonundadır.
    target_str = '<div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">'
    if target_str in modal_content and 'id="guncelleCanliOnizleme"' not in modal_content:
        modal_content = modal_content.replace(target_str, preview_html_guncelle + '\n' + target_str)
        with open(MODAL_PATH, 'w', encoding='utf-8') as f:
            f.write(modal_content)
        print("✓ update_soru_guncelle_modal.html güncellendi.")
    
    # 2. soru_bankasi.html Güncelleme (HTML + JS)
    with open(SORU_BANKASI_PATH, 'r', encoding='utf-8') as f:
        sb_content = f.read()

    # Soru Ekle Modalı İçin HTML (Benzer yapı)
    preview_html_ekle = """
            <div class="mt-8 border-t pt-6 bg-slate-50 -mx-6 px-6 pb-6">
                <h3 class="text-sm font-bold text-slate-500 uppercase mb-4 flex items-center gap-2 pt-4">
                    <i data-lucide="eye" class="w-4 h-4"></i> Kağıt Görünümü Önizleme
                </h3>
                <div class="bg-white border border-slate-200 p-8 rounded-xl shadow-sm relative overflow-hidden">
                    <div class="absolute inset-0 opacity-[0.02] pointer-events-none" style="background-image: radial-gradient(#000 1px, transparent 1px); background-size: 20px 20px;"></div>
                    <div id="ekleCanliOnizleme" class="relative z-10 font-serif">
                        <p class="text-slate-400 text-center italic">Önizleme için soru verilerini giriniz...</p>
                    </div>
                </div>
            </div>
    """
    
    # soruEkleModal içinde buton grubunu bul. (class="flex justify-end gap-3 pt-4 border-t border-slate-100")
    target_ekle = '<div class="flex justify-end gap-3 pt-4 border-t border-slate-100">'
    if target_ekle in sb_content and 'id="ekleCanliOnizleme"' not in sb_content:
        sb_content = sb_content.replace(target_ekle, preview_html_ekle + '\n' + target_ekle)
        print("✓ Soru Ekle modalı HTML güncellendi.")

    # JS Kodlarını Ekle
    js_code = """
    // --- CANLI ÖNİZLEME LOGIC ---
    function onizlemeGuncelle(sourceType) {
        const prefix = sourceType === 'ekle' ? 'ekle' : 'guncelle';
        
        // Element Kontrolü
        const onizlemeAlani = document.getElementById(prefix + 'CanliOnizleme');
        if (!onizlemeAlani) return;

        // Verileri Al
        const soruMetniEl = document.getElementById(prefix + 'SoruMetni');
        const soruMetni = soruMetniEl ? soruMetniEl.value : '';
        
        const gorselYolu = document.getElementById(prefix + 'GorselYolu').value;
        const gorselKonum = document.getElementById(prefix + 'GorselKonum').value;
        const sikDuzeni = document.getElementById(prefix + 'SikDuzeni').value;
        
        if (!soruMetni && !gorselYolu) {
            onizlemeAlani.innerHTML = '<p class="text-slate-400 text-center italic">Önizleme için veri giriniz...</p>';
            return;
        }

        const siklar = {};
        ['A', 'B', 'C', 'D', 'E'].forEach(harf => {
            const el = document.getElementById(prefix + 'Secenek' + harf);
            if (el && el.value) siklar[harf] = el.value;
        });

        // HTML Oluştur
        let html = '<div class="flex flex-col sm:flex-row gap-6 items-start">';
        
        // Resim Elementi
        const imgTag = gorselYolu ? `<img src="${gorselYolu}" class="max-w-full h-auto max-h-60 rounded-lg border border-slate-200 object-contain mx-auto mb-4 bg-white">` : '';

        // ** SOL KOLON (Metin + Orta Görsel + Şıklar) **
        let mainContent = `<div class="flex-1 min-w-0 w-full">`;
        
        // Üst Görsel
        if (gorselKonum === 'ustte' && imgTag) {
            mainContent += `<div class="text-center mb-4">${imgTag}</div>`;
        }
        
        // Soru Metni
        mainContent += `<div class="text-[16px] text-slate-900 leading-relaxed font-medium mb-3 text-justify whitespace-pre-line">${soruMetni || 'Soru metni...'}</div>`;
        
        // Ara Görsel
        if ((gorselKonum === 'arada' || !gorselKonum) && imgTag) {
            mainContent += `<div class="text-center my-4">${imgTag}</div>`;
        }
        
        // Şıklar
        if (Object.keys(siklar).length > 0) {
            let sikClass = 'space-y-2'; 
            if (sikDuzeni === 'yan_yana') sikClass = 'flex flex-wrap gap-x-6 gap-y-2';
            else if (sikDuzeni === 'iki_sutun') sikClass = 'grid grid-cols-1 sm:grid-cols-2 gap-x-8 gap-y-2';
            
            mainContent += `<div class="mt-4 ${sikClass} ml-1">`;
            Object.keys(siklar).forEach(harf => {
                mainContent += `
                <div class="flex items-start gap-2 min-w-[100px]">
                    <span class="flex-shrink-0 w-6 h-6 rounded-full border border-slate-400 flex items-center justify-center text-xs font-bold text-slate-700 bg-white">${harf}</span>
                    <span class="text-sm text-slate-900 pt-0.5 leading-snug">${siklar[harf]}</span>
                </div>`;
            });
            mainContent += `</div>`;
        }
        
        mainContent += `</div>`; // End sol kolon
        html += mainContent;

        // ** SAĞ GÖRSEL **
        if (gorselKonum === 'yanda' && imgTag) {
            html += `<div class="flex-shrink-0 w-full sm:w-1/3 ml-0 sm:ml-4 mb-4 sm:mb-0">${imgTag}</div>`;
        }

        html += '</div>'; // End container
        onizlemeAlani.innerHTML = html;
    }

    // Listener Kurulumu
    function setupLivePreview(sourceType) {
        const prefix = sourceType === 'ekle' ? 'ekle' : 'guncelle';
        const inputs = [
            prefix + 'SoruMetni', prefix + 'GorselKonum', prefix + 'SikDuzeni',
            prefix + 'SecenekA', prefix + 'SecenekB', prefix + 'SecenekC', prefix + 'SecenekD', prefix + 'SecenekE'
        ];
        
        inputs.forEach(id => {
            const el = document.getElementById(id);
            if (el) {
                el.addEventListener('input', () => onizlemeGuncelle(sourceType));
                el.addEventListener('change', () => onizlemeGuncelle(sourceType));
            }
        });
        
        // Görsel Yolu (Hidden input) değişimi (MutationObserver ile veya manuel)
        // Biz manuel çağıracağız görsel yüklenince.
    }
    
    // Sayfa Yüklendiğinde Listenerları Başlat
    setTimeout(() => {
        setupLivePreview('ekle');
        setupLivePreview('guncelle');
    }, 1000);
    
    // Modal Açılış Tetikleyicilerine Entegrasyon
    // Mevcut acSoruEkleModal ve soruDuzenle fonksiyonlarına ekleme yapmalıyız.
    // Ancak fonksiyonları override etmek yerine, mutation observer kullanabiliriz veya timer.
    // En basiti: onclick eventlerine ekleme yapmak veya global setInterval (kötü pratik).
    
    // Soru Düzenle için: soruDuzenle fonksiyonu sonunda onizlemeGuncelle('guncelle') çağrılmalı.
    // Soru Ekle için: acSoruEkleModal fonksiyonu sonunda onizlemeGuncelle('ekle') çağrılmalı.
    
    """
    
    # JS kodunu dosya sonuna ekle
    if 'function onizlemeGuncelle' not in sb_content:
        # </script> öncesine ekle
        last_script = sb_content.rfind("</script>")
        if last_script != -1:
            sb_content = sb_content[:last_script] + js_code + "\n" + sb_content[last_script:]
            print("✓ JS kodu eklendi.")

    # Mevcut JS fonksiyonlarını güncellemek gerekiyor (trigger eklemek için)
    # 1. soruDuzenle (Verileri doldurduktan sonra preview çalışsın)
    # Kod içinde: document.getElementById('soruGuncelleModal').classList.remove('hidden'); satırından sonra
    # onizlemeGuncelle('guncelle'); ekle.
    
    trigger_guncelle = "document.getElementById('soruGuncelleModal').classList.remove('hidden');"
    if trigger_guncelle in sb_content:
        sb_content = sb_content.replace(trigger_guncelle, trigger_guncelle + "\n                onizlemeGuncelle('guncelle');")

    # 2. acSoruEkleModal
    trigger_ekle = "document.getElementById('soruEkleModal').classList.remove('hidden');"
    if trigger_ekle in sb_content:
        sb_content = sb_content.replace(trigger_ekle, trigger_ekle + "\n        onizlemeGuncelle('ekle');")
        
    # 3. Görsel Yükleme Callbackleri
    # ekleGorselYukle ve guncelleGorselYukle (input change)
    # gorselYukle (soru_bankasi.html içinde)
    if 'document.getElementById(\'guncelleGorselYolu\').value = data.dosya_yolu;' in sb_content:
         sb_content = sb_content.replace(
             "document.getElementById('guncelleGorselYolu').value = data.dosya_yolu;",
             "document.getElementById('guncelleGorselYolu').value = data.dosya_yolu;\n                    onizlemeGuncelle('guncelle');"
         )
         
    if 'document.getElementById(\'ekleGorselYolu\').value = data.dosya_yolu;' in sb_content:
        sb_content = sb_content.replace(
            "document.getElementById('ekleGorselYolu').value = data.dosya_yolu;",
            "document.getElementById('ekleGorselYolu').value = data.dosya_yolu;\n                    onizlemeGuncelle('ekle');"
        )

    with open(SORU_BANKASI_PATH, 'w', encoding='utf-8') as f:
        f.write(sb_content)

if __name__ == "__main__":
    update_ui_preview()
