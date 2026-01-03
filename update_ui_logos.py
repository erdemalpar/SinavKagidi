import os

BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi/templates'
FILE_PATH = os.path.join(BASE_DIR, 'sinav_hazirlama.html')

def update_ui_logos():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # HTML: Logolar Paneli
    html_code = """
                <!-- Antet Logoları -->
                <div class="border-t border-slate-200 pt-4 mt-4">
                    <h3 class="text-sm font-bold text-slate-700 mb-3">Antet Logoları</h3>
                    <div class="grid grid-cols-2 gap-4">
                        <!-- Sol Logo -->
                        <div>
                           <label class="block text-xs font-medium text-slate-500 mb-1">Sol Üst Logo</label>
                           <div class="relative group border-2 border-dashed border-slate-300 rounded-lg p-2 text-center hover:bg-slate-50 hover:border-purple-300 transition-all h-24 flex items-center justify-center cursor-pointer" onclick="document.getElementById('solLogoInput').click()">
                                <input type="file" id="solLogoInput" class="hidden" accept="image/*" onchange="logoYukle(this, 'sol')">
                                <input type="hidden" id="sinavLogoSol">
                                <div id="solLogoPlaceholder">
                                    <i data-lucide="upload" class="w-6 h-6 mx-auto text-slate-400 group-hover:text-purple-500"></i>
                                    <span class="text-xs text-slate-400 group-hover:text-purple-500 block mt-1">Logo Seç</span>
                                </div>
                                <div id="solLogoPreviewContainer" class="hidden absolute inset-0 bg-white rounded-lg flex items-center justify-center p-1 border border-slate-200">
                                    <img id="solLogoPreview" class="max-h-full max-w-full object-contain">
                                    <button type="button" onclick="event.stopPropagation(); logoSil('sol')" class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md hover:bg-red-600 transition-all z-10"><i data-lucide="x" class="w-3 h-3"></i></button>
                                </div>
                           </div>
                        </div>
                        <!-- Sağ Logo -->
                        <div>
                           <label class="block text-xs font-medium text-slate-500 mb-1">Sağ Üst Logo</label>
                           <div class="relative group border-2 border-dashed border-slate-300 rounded-lg p-2 text-center hover:bg-slate-50 hover:border-purple-300 transition-all h-24 flex items-center justify-center cursor-pointer" onclick="document.getElementById('sagLogoInput').click()">
                                <input type="file" id="sagLogoInput" class="hidden" accept="image/*" onchange="logoYukle(this, 'sag')">
                                <input type="hidden" id="sinavLogoSag">
                                <div id="sagLogoPlaceholder">
                                    <i data-lucide="upload" class="w-6 h-6 mx-auto text-slate-400 group-hover:text-purple-500"></i>
                                    <span class="text-xs text-slate-400 group-hover:text-purple-500 block mt-1">Logo Seç</span>
                                </div>
                                <div id="sagLogoPreviewContainer" class="hidden absolute inset-0 bg-white rounded-lg flex items-center justify-center p-1 border border-slate-200">
                                    <img id="sagLogoPreview" class="max-h-full max-w-full object-contain">
                                    <button type="button" onclick="event.stopPropagation(); logoSil('sag')" class="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 shadow-md hover:bg-red-600 transition-all z-10"><i data-lucide="x" class="w-3 h-3"></i></button>
                                </div>
                           </div>
                        </div>
                    </div>
                    <!-- Boyut Ayarı -->
                    <div class="mt-3">
                        <label class="block text-sm font-medium text-slate-700 mb-2 flex justify-between">
                            <span>Logo Boyutu (px)</span>
                            <span class="text-slate-500" id="logoBoyutLabel">80px</span>
                        </label>
                        <input type="range" id="sinavLogoBoyutu" min="40" max="250" value="80" 
                               class="w-full h-2 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-purple-600"
                               oninput="document.getElementById('logoBoyutLabel').textContent = this.value + 'px'">
                    </div>
                </div>
    """
    
    # Anchor: Görsel Boyutu input'unun kapanışı
    # Tam stringi bulmak zor olabilir, biraz esnek yapalım.
    anchor_part = "oninput=\"document.getElementById('gorselBoyutuLabel').textContent = '%' + this.value\">"
    
    if 'id="sinavLogoSol"' not in content:
        if anchor_part in content:
            # Anchor'dan sonraki </div> i manuel bulmak yerine replace ile ekleyelim.
            # Şu an dosya yapısı: ... <input ... > </div> ...
            # Biz bu </div>'den sonra yeni HTML'i ekleyeceğiz.
            # Replace: anchor + </div> -> anchor + </div> + html_code
            # Ancak aradaki boşluklar vs sorun olabilir.
            
            # En iyisi: "<!-- Görünüm Ayarları -->" panelinin kapanışına (</div></div>) gitmeden önce.
            # Panel kapanışından önce ekleyelim.
            # "update_sinav_hazirlama_v2.py" de panel şöyle bitiyordu: ... </div> </div> <!-- Seçilen Sorular -->
            # Biz "<!-- Seçilen Sorular -->" stringinden geriye gidip son kapanan div'in içine...
            # Bu çok karmaşık.
            
            # Basit Yöntem: Anchor'a güvenelim.
            content = content.replace(anchor_part, anchor_part + "\n                </div>" + html_code + "\n                <div>")
            # Fazladan <div> </div> çifti oluşabilir mi? 
            # Orijinal: ... > </div>
            # Yeni: ... > </div> ... html ... <div> </div> (fazlalık div açtım kapattım mı? Hayır.)
            # Yukarıdaki replace: input tagini kapatıyor, sonra </div> ekliyor (ama zaten vardı, duplicate </div> oldu).
            # Dikkat: Replace yaparken orijinal </div>'i de korumalıyız veya silmeliyiz.
            # Input taginde > var, kapanış tagi yok (self closing). Sonra </div> geliyor.
            
            # Daha basit bir anchor:  <span class="text-slate-500" id="gorselBoyutuLabel">%100</span>
            # Bu label var. 
            # Biz bu "Görsel Boyutu" div bloğunun TAMAMEN SONRASINA eklemek istiyoruz.
            # Bu div bloğu class="mt-3" veya benzeri değil, scriptte "<div>" ile başlamıştı.
            
            # Anchor: `oninput="document.getElementById('gorselBoyutuLabel').textContent = '%' + this.value">`
            # Bu satırın devamında `</div>` var.
            # Biz `</div>` yerine `</div>` + html_code yaparsak olur mu?
            # Fakat `replace` stringi tam eşleşmeli.
            
            # Dosyayı okuyup split edelim.
            parts = content.split(anchor_part)
            if len(parts) > 1:
                # parts[0] + anchor + </div> + html + parts[1] (ama parts[1] zaten </div> ile başlıyor mu?
                # Hayır parts[1] input taginin kapanışından sonrasıdır.
                # Dosya: ... input ... > \n </div>
                # parts[1] = \n </div> ...
                # Biz parts[1] içindeki ilk </div> stringini bulup sonrasına ekleyelim.
                sub_parts = parts[1].split('</div>', 1)
                new_content = parts[0] + anchor_part + sub_parts[0] + '</div>' + html_code + sub_parts[1]
                content = new_content
                print("✓ HTML Logo paneli eklendi.")


    # JS Kodları
    js_funcs = """
    // Logo Yükleme
    async function logoYukle(input, side) { // side: 'sol' veya 'sag'
        if (input.files && input.files[0]) {
            const formData = new FormData();
            formData.append('gorsel', input.files[0]);
            
            try {
                const response = await fetch('/gorsel-yukle', { method: 'POST', body: formData });
                const data = await response.json();
                
                if (data.basarili) {
                    const path = data.dosya_yolu;
                    document.getElementById(side === 'sol' ? 'sinavLogoSol' : 'sinavLogoSag').value = path;
                    
                    const  preview = document.getElementById(side === 'sol' ? 'solLogoPreview' : 'sagLogoPreview');
                    preview.src = path;
                    
                    document.getElementById(side === 'sol' ? 'solLogoPlaceholder' : 'sagLogoPlaceholder').classList.add('hidden');
                    document.getElementById(side === 'sol' ? 'solLogoPreviewContainer' : 'sagLogoPreviewContainer').classList.remove('hidden');
                    
                    if (window.lucide) lucide.createIcons();
                } else {
                    toastGoster(data.mesaj, 'error');
                }
            } catch (error) {
                console.error(error);
                toastGoster('Logo yüklenirken hata oluştu', 'error');
            }
        }
    }
    
    function logoSil(side) {
        document.getElementById(side === 'sol' ? 'solLogoInput' : 'sagLogoInput').value = '';
        document.getElementById(side === 'sol' ? 'sinavLogoSol' : 'sinavLogoSag').value = '';
        
        document.getElementById(side === 'sol' ? 'solLogoPlaceholder' : 'sagLogoPlaceholder').classList.remove('hidden');
        document.getElementById(side === 'sol' ? 'solLogoPreviewContainer' : 'sagLogoPreviewContainer').classList.add('hidden');
        document.getElementById(side === 'sol' ? 'solLogoPreview' : 'sagLogoPreview').src = '';
    }
    """
    
    js_data_anchor = "gorsel_boyutu: document.getElementById('sinavGorselBoyutu').value,"
    js_data_new = """
            logo_sol: document.getElementById('sinavLogoSol').value,
            logo_sag: document.getElementById('sinavLogoSag').value,
            logo_boyutu: document.getElementById('sinavLogoBoyutu').value,"""
            
    if js_data_anchor in content and 'logo_sol:' not in content:
        content = content.replace(js_data_anchor, js_data_anchor + js_data_new)
        print("✓ JS Data alanları güncellendi.")

    if 'function logoYukle' not in content:
        last_script = content.rfind("</script>")
        if last_script != -1:
            content = content[:last_script] + js_funcs + "\n" + content[last_script:]
            print("✓ JS fonksiyonları eklendi.")

    with open(FILE_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_ui_logos()
