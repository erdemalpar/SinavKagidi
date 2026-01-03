import os

# Base URL
BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi'
FILE_PATH = os.path.join(BASE_DIR, 'templates/soru_bankasi.html')

def update_ui_v2():
    with open(FILE_PATH, 'r', encoding='utf-8') as f:
        content = f.read()

    # YENİ SORU EKLEME MODALI HTML
    yeni_modal_html = """
<!-- Soru Ekleme Modalı -->
<div id="soruEkleModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-5xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <div class="gradient-primary p-6 text-white flex items-center justify-between sticky top-0 z-10 shadow-md">
            <h2 class="text-xl font-bold flex items-center gap-2">
                <i data-lucide="plus-circle" class="w-6 h-6"></i>
                Yeni Soru Ekle
            </h2>
            <button onclick="kapatSoruEkleModal()"
                class="hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-all">
                <i data-lucide="x" class="w-6 h-6"></i>
            </button>
        </div>

        <form id="soruEkleForm" class="p-6 space-y-8">
            <input type="hidden" id="ekleGorselYolu">

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                <!-- SOL KOLON -->
                <div class="lg:col-span-8 space-y-6">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-2">Soru Metni *</label>
                        <textarea id="ekleSoruMetni" rows="4" class="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-purple-500 shadow-sm transition-all" placeholder="Soru metnini buraya giriniz..." required></textarea>
                    </div>

                    <!-- Şıklar -->
                    <div class="bg-slate-50 rounded-xl p-5 border border-slate-200">
                        <label class="block text-sm font-bold text-slate-800 mb-4 border-b pb-2">Şıklar ve Cevap</label>
                        <div class="space-y-3">
"""
    # Şıklar döngüsü
    for harf in ['A', 'B', 'C', 'D', 'E']:
        checked = 'checked' if harf == 'A' else ''
        placeholder = f"{harf} şıkkı (Opsiyonel)" if harf == 'E' else f"{harf} şıkkı"
        yeni_modal_html += f"""
                            <div class="flex items-center gap-3 group">
                                <div class="w-8 h-8 flex items-center justify-center bg-white border border-slate-300 rounded-full font-bold text-slate-600 group-hover:border-purple-500 group-hover:text-purple-600 transition-colors">{harf}</div>
                                <input type="text" id="ekleSecenek{harf}" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-purple-500 shadow-sm" placeholder="{placeholder}">
                                <label class="cursor-pointer">
                                    <input type="radio" name="ekleDogruCevap" value="{harf}" class="peer hidden" {checked}>
                                    <div class="w-8 h-8 rounded-full border-2 border-slate-300 peer-checked:bg-green-500 peer-checked:border-green-500 text-white flex items-center justify-center transition-all hover:bg-slate-100"><i data-lucide="check" class="w-4 h-4 opacity-0 peer-checked:opacity-100"></i></div>
                                </label>
                            </div>"""
    
    yeni_modal_html += """
                        </div>
                    </div>
                </div>

                <!-- SAĞ KOLON -->
                <div class="lg:col-span-4 space-y-6">
                     <!-- Görsel -->
                     <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <div class="bg-slate-50 px-4 py-3 border-b font-medium text-slate-700 flex items-center gap-2">
                             <i data-lucide="image" class="w-4 h-4 text-purple-600"></i> Görsel
                        </div>
                        <div class="p-4 space-y-4">
                            <div id="ekleGorselArea" class="relative group">
                                <div id="ekleGorselPlaceholder" class="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center cursor-pointer hover:bg-purple-50 hover:border-purple-400 transition-all" onclick="document.getElementById('ekleGorselInput').click()">
                                    <i data-lucide="upload" class="w-8 h-8 mx-auto text-slate-400 mb-2 group-hover:text-purple-500"></i>
                                    <span class="text-xs text-slate-500 block">Görsel Yükle</span>
                                </div>
                                <div id="ekleGorselPreviewContainer" class="hidden relative">
                                    <img id="ekleGorselPreviewImg" src="" class="w-full h-40 object-contain bg-slate-100 rounded-lg border">
                                    <button type="button" onclick="ekleGorselKaldir()" class="absolute top-2 right-2 bg-red-500 text-white p-1 rounded shadow hover:bg-red-600 transition-all"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                                </div>
                                <input type="file" id="ekleGorselInput" class="hidden" accept="image/*" onchange="ekleGorselYukle(this)">
                            </div>
                            <!-- Konum -->
                            <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Konum</label>
                                <select id="ekleGorselKonum" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-purple-500">
                                    <option value="ustte">⬆️ Sorunun Üstünde</option>
                                    <option value="arada" selected>↕️ Metin ve Şıklar Arasında</option>
                                    <option value="yanda">➡️ Sağ Tarafta</option>
                                </select>
                            </div>
                        </div>
                     </div>

                     <!-- Ayarlar -->
                     <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <div class="bg-slate-50 px-4 py-3 border-b font-medium text-slate-700 flex items-center gap-2">
                             <i data-lucide="settings" class="w-4 h-4 text-blue-600"></i> Ayarlar
                        </div>
                        <div class="p-4 space-y-4">
                             <!-- Şık Düzeni -->
                             <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Şık Düzeni</label>
                                <select id="ekleSikDuzeni" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500">
                                    <option value="alt_alta" selected>⬇️ Alt Alta</option>
                                    <option value="yan_yana">➡️ Yan Yana</option>
                                    <option value="iki_sutun">🔲 İki Sütun</option>
                                </select>
                             </div>
                             <!-- Puan -->
                             <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Puan</label>
                                <div class="flex items-center gap-2">
                                    <input type="number" id="eklePuan" class="flex-1 px-3 py-2 border border-slate-200 rounded-lg text-sm font-bold text-center" min="1" value="5">
                                    <span class="text-sm text-slate-500">Puan</span>
                                </div>
                             </div>
                             <!-- Zorluk -->
                             <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Zorluk</label>
                                <select id="ekleZorluk" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm">
                                    <option value="Kolay">🟢 Kolay</option>
                                    <option value="Orta" selected>🟡 Orta</option>
                                    <option value="Zor">🔴 Zor</option>
                                </select>
                             </div>
                             <!-- Konu -->
                             <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Konu</label>
                                <input type="text" id="ekleKonu" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="Konu etiketi">
                            </div>
                        </div>
                     </div>
                </div>
            </div>
            
            <div class="flex justify-end gap-3 pt-4 border-t border-slate-100">
                <button type="button" onclick="kapatSoruEkleModal()" class="px-6 py-2.5 rounded-lg text-slate-600 hover:bg-slate-100 font-medium transition-all text-sm">İptal</button>
                <button type="submit" class="px-8 py-2.5 bg-gradient-to-r from-purple-600 to-indigo-600 text-white rounded-lg font-medium shadow-lg hover:shadow-xl hover:translate-y-[-1px] transition-all text-sm flex items-center gap-2">
                    <i data-lucide="plus" class="w-4 h-4"></i> Soru Ekle
                </button>
            </div>
        </form>
    </div>
</div>
"""
    
    # HTML Değişimi: <!-- Soru Ekleme Modalı --> nı bul ve değiştir
    if '<!-- Soru Ekleme Modalı -->' in content:
        # Eski modalın bitişini bulmak lazım. Manuel olarak önceki kodda bitiş div'ini biliyorum ama riskli.
        # Basitçe: <!-- Soru Ekleme Modalı --> ile başla, <form id="soruEkleForm" ... </form> ... </div> ... </div> kadar git.
        # Güvenli yol: Tüm içeriği satır satır oku, <!-- Soru Ekleme Modalı --> bul, sonraki </div> </div> (ana kapayıcı) kadar atla.
        # Ancak regex veya split safer.
        # Eski modal ID: soruEkleModal
        pass

    # Regex ile eski modalı bul ve değiştir
    import re
    # Pattern: <!-- Soru Ekleme Modalı --> ... <div id="soruEkleModal" ... </div> </div> (not greedy is hard here w/ formatted html)
    # Basit Split: 
    parts = content.split('<!-- Soru Ekleme Modalı -->')
    if len(parts) > 1:
        # İkinci parça (eski modal + kalan dosya). 
        # Eski modalın bitişini şöyle bulalım: id="soruListesi" bloğuna kadar? Hayır.
        # Eski modal koduna bakarsak: en sonda 2 tane </div> var.
        # Ve bir sonraki element genelde <script> veya Soru Listesi
        
        # En temiz yol: Eski modalın içeriğini replace etmek yerine, soru_bankasi.html'yi tamamen baştan kurmak olurdu ama çok büyük.
        # Eski modalın kapanış </form> taginden sonraki 2 tane </div> tagini bulalım.
        
        # Manuel replace deneyelim. Eski modalın başlangıcı belli.
        # Eski modalın içindeki form id="soruEkleForm".
        
        # Mevcut dosya içeriğine baktım (637. adım). Start: 166. satır.
        # Bitiş: </form> sonrası...
        
        # Hadi Python'ın string replace gücünü kullanalım ama "eski content"i tam bilmek lazım.
        # Scripti basitleştirelim:
        # 1. dosya içeriğinde 'id="soruEkleForm"' geçen bloğu bulup JS ile manipüle etmek yerine,
        #    HTML kısmını değiştirmek farz.
        pass

    # Regex ile değiştirelim.
    # <div id="soruEkleModal".*?<\/div>\s*<\/div>\s*(?=<script|<!--|{%|$)
    # Bu riskli.
    
    # KESİN ÇÖZÜM: `templates/soru_bankasi.html` dosyasını `view_file` ile parça parça okuyup birleştirmek yerine
    # Mevcut içeriği okuduk zaten. `parts[0]` + `yeni_modal_html` + `kalan_kisim`.
    # Kalan kısım: Eski modalın bittiği yerden sonrası.
    # Eski modal ne zaman bitiyor?
    # </form> dan sonra 2 tane </div> var.
    # Ayrıca `ac_soru_ekle_modal` butonu da var dosyanın içinde.
    
    # Eski fonksiyonları da güncellememiz lazım (JS).
    
    # JS güncellemesi
    js_update = """
    // Soru Ekleme Görsel Yükle
    async function ekleGorselYukle(input) {
        if (input.files && input.files[0]) {
            const formData = new FormData();
            formData.append('gorsel', input.files[0]);
            try {
                const response = await fetch('/gorsel-yukle', { method: 'POST', body: formData });
                const data = await response.json();
                if (data.basarili) {
                    document.getElementById('ekleGorselYolu').value = data.dosya_yolu;
                    document.getElementById('ekleGorselPreviewImg').src = data.dosya_yolu;
                    document.getElementById('ekleGorselPlaceholder').classList.add('hidden');
                    document.getElementById('ekleGorselPreviewContainer').classList.remove('hidden');
                } else { toastGoster(data.mesaj, 'error'); }
            } catch (error) { toastGoster('Hata oluştu', 'error'); }
        }
    }
    
    function ekleGorselKaldir() {
        document.getElementById('ekleGorselYolu').value = '';
        document.getElementById('ekleGorselInput').value = '';
        document.getElementById('ekleGorselPlaceholder').classList.remove('hidden');
        document.getElementById('ekleGorselPreviewContainer').classList.add('hidden');
    }

    // Modal Açılışında Puan Hafızası
    function acSoruEkleModal() {
        document.getElementById('soruEkleModal').classList.remove('hidden');
        // Hafızadaki puanı getir
        const kayitliPuan = localStorage.getItem('sonAyarlananPuan');
        if (kayitliPuan) {
            document.getElementById('eklePuan').value = kayitliPuan;
        }
        setTimeout(() => lucide.createIcons(), 100);
    }
    
    // Soru Ekle Submit
    document.getElementById('soruEkleForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        
        // Puanı hafızaya al
        const puan = document.getElementById('eklePuan').value;
        localStorage.setItem('sonAyarlananPuan', puan);

        const soruData = {
            soru_metni: document.getElementById('ekleSoruMetni').value,
            // Şıkları dinamik alabiliriz veya tek tek
            secenek_a: document.getElementById('ekleSecenekA').value,
            secenek_b: document.getElementById('ekleSecenekB').value,
            secenek_c: document.getElementById('ekleSecenekC').value,
            secenek_d: document.getElementById('ekleSecenekD').value,
            secenek_e: document.getElementById('ekleSecenekE').value,
            dogru_cevap: document.querySelector('input[name="ekleDogruCevap"]:checked')?.value || 'A',
            konu: document.getElementById('ekleKonu').value,
            zorluk: document.getElementById('ekleZorluk').value,
            puan: parseInt(puan),
            // Yeni Alanlar
            gorsel_yolu: document.getElementById('ekleGorselYolu').value,
            gorsel_konum: document.getElementById('ekleGorselKonum').value,
            sik_duzeni: document.getElementById('ekleSikDuzeni').value
        };

        try {
            const data = await apiIstegi('/soru-ekle', {
                method: 'POST',
                body: JSON.stringify(soruData)
            });
            logger.basarili('Soru eklendi', data);
            toastGoster('Soru başarıyla eklendi!', 'success');
            kapatSoruEkleModal();
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            logger.hata('Soru ekleme hatası', error);
        }
    });
    """

    # Şimdi bu JS'i ve HTML'i mevcut dosyaya enjekte edelim.
    # Oldukça kaba bir yöntem kullanacağım: Eski modalı ve JS'i bulmak zor.
    # Dosyayı "işaretçiler" kullanarak bölüp yeniden inşa edeceğim.
    
    # 1. Kısım: <!-- Soru Ekleme Modalı --> öncesi
    part1 = content.split('<!-- Soru Ekleme Modalı -->')[0]
    
    # 2. Kısım: <!-- Dosya Yükleme Modalı --> sonrası (Çünkü Soru Ekle modalı Soru Listesinden sonra gelmeyebilir ama genelde modallar yan yana olur.
    # Dosya yapısına bakalım (637. adım): Soru Ekleme Modalı (165) -> Form -> ... -> </form> </div> </div> -> <!-- Dosya Yükleme Modalı --> (261. satır)
    # Yani "<!-- Dosya Yükleme Modalı -->" stringi ile bölebiliriz.
    
    if '<!-- Dosya Yükleme Modalı -->' in content:
        rest = content.split('<!-- Dosya Yükleme Modalı -->')[1]
        
        # 3. Kısım: JS güncellemesi.
        # "document.getElementById('soruEkleForm').addEventListener" bloğunu bulup sileceğiz.
        
        # rest içindeki JS bloğunun yeri: <script> taginden sonra.
        
        # Basitçe: Eski JS kodunu etkisiz hale getirip (veya silip) yeni JS kodunu <script> taginin hemen altına ekleyelim.
        # Aslında en güzeli: `function acSoruEkleModal` fonksiyonunu override etmek.
        # Ve event listener'ı tekrar eklemek (eskisi hata verebilir çünkü ID'ler değişti).
        # Eski ID'ler (soruMetni vs) artık yok, o yüzden eski listener hata fırlatır ve durur. Sorun değil.
        
        # Yeni JS kodunu `</script>` taginin hemen öncesine ekleyelim.
        rest = rest.replace('</script>', js_update + '\n</script>')
        
        # Dosyayı birleştir
        new_full_content = part1 + yeni_modal_html + "\n\n<!-- Dosya Yükleme Modalı -->" + rest
        
        with open(FILE_PATH, 'w', encoding='utf-8') as f:
            f.write(new_full_content)
        print("✓ Soru Ekleme Modalı güncellendi")
        
    else:
        print("✗ Dosya yapısı beklendiği gibi değil (Dosya Yükleme Modalı bulunamadı)")

if __name__ == "__main__":
    update_ui_v2()
