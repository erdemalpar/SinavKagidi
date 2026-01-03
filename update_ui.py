import os

# Base URL
BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi'

def update_modal_html():
    file_path = os.path.join(BASE_DIR, 'templates/_soru_guncelle_modal.html')
    
    html_content = """
<!-- Soru Güncelleme Modal'ı -->
<div id="soruGuncelleModal" class="hidden fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-5xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        <!-- Header -->
        <div class="gradient-primary p-6 text-white flex items-center justify-between sticky top-0 z-10 shadow-md">
            <div class="flex items-center gap-3">
                <div class="p-2 bg-white bg-opacity-20 rounded-lg">
                    <i data-lucide="edit-3" class="w-6 h-6"></i>
                </div>
                <div>
                    <h2 class="text-xl font-bold leading-tight">Soru Düzenle</h2>
                    <p class="text-xs opacity-80">ID: <span id="guncellenecekSoruId" class="font-mono">#</span></p>
                </div>
            </div>
            <button onclick="kapatSoruGuncelleModal()" class="hover:bg-white hover:bg-opacity-20 p-2 rounded-lg transition-all">
                <i data-lucide="x" class="w-6 h-6"></i>
            </button>
        </div>

        <form id="soruGuncelleForm" class="p-6 space-y-8">
            <input type="hidden" id="guncelleSoruId">
            <input type="hidden" id="guncelleGorselYolu">

            <div class="grid grid-cols-1 lg:grid-cols-12 gap-8">
                
                <!-- SOL KOLON: Soru İçeriği (8 birim) -->
                <div class="lg:col-span-8 space-y-6">
                    <!-- Soru Metni -->
                    <div>
                        <label class="flex items-center justify-between text-sm font-medium text-slate-700 mb-2">
                            <span>Soru Metni</span>
                            <span class="text-xs text-slate-400">Zorunlu Alan</span>
                        </label>
                        <textarea id="guncelleSoruMetni" rows="4"
                            class="w-full px-4 py-3 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 focus:border-transparent transition-all shadow-sm text-slate-700 placeholder-slate-400"
                            placeholder="Soru metnini buraya giriniz..." required></textarea>
                    </div>

                    <!-- Şıklar -->
                    <div class="bg-slate-50 rounded-xl p-5 border border-slate-200">
                        <label class="block text-sm font-bold text-slate-800 mb-4 border-b pb-2">Şıklar ve Cevap</label>
                        
                        <div class="space-y-3">
                            <!-- A Şıkkı -->
                            <div class="flex items-center gap-3 group">
                                <div class="w-8 h-8 flex items-center justify-center bg-white border border-slate-300 rounded-full font-bold text-slate-600 group-hover:border-indigo-400 group-hover:text-indigo-600 transition-colors shadow-sm">A</div>
                                <input type="text" id="guncelleSecenekA" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all shadow-sm" placeholder="A şıkkı">
                                <label class="cursor-pointer">
                                    <input type="radio" name="dogruCevap" value="A" class="peer hidden">
                                    <div class="w-8 h-8 rounded-full border-2 border-slate-300 peer-checked:border-green-500 peer-checked:bg-green-500 text-white flex items-center justify-center transition-all hover:bg-slate-100">
                                        <i data-lucide="check" class="w-4 h-4 opacity-0 peer-checked:opacity-100"></i>
                                    </div>
                                </label>
                            </div>
                            
                            <!-- B Şıkkı -->
                            <div class="flex items-center gap-3 group">
                                <div class="w-8 h-8 flex items-center justify-center bg-white border border-slate-300 rounded-full font-bold text-slate-600 group-hover:border-indigo-400 group-hover:text-indigo-600 transition-colors shadow-sm">B</div>
                                <input type="text" id="guncelleSecenekB" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all shadow-sm" placeholder="B şıkkı">
                                <label class="cursor-pointer">
                                    <input type="radio" name="dogruCevap" value="B" class="peer hidden">
                                    <div class="w-8 h-8 rounded-full border-2 border-slate-300 peer-checked:border-green-500 peer-checked:bg-green-500 text-white flex items-center justify-center transition-all hover:bg-slate-100">
                                        <i data-lucide="check" class="w-4 h-4 opacity-0 peer-checked:opacity-100"></i>
                                    </div>
                                </label>
                            </div>

                            <!-- C Şıkkı -->
                            <div class="flex items-center gap-3 group">
                                <div class="w-8 h-8 flex items-center justify-center bg-white border border-slate-300 rounded-full font-bold text-slate-600 group-hover:border-indigo-400 group-hover:text-indigo-600 transition-colors shadow-sm">C</div>
                                <input type="text" id="guncelleSecenekC" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all shadow-sm" placeholder="C şıkkı">
                                <label class="cursor-pointer">
                                    <input type="radio" name="dogruCevap" value="C" class="peer hidden">
                                    <div class="w-8 h-8 rounded-full border-2 border-slate-300 peer-checked:border-green-500 peer-checked:bg-green-500 text-white flex items-center justify-center transition-all hover:bg-slate-100">
                                        <i data-lucide="check" class="w-4 h-4 opacity-0 peer-checked:opacity-100"></i>
                                    </div>
                                </label>
                            </div>

                            <!-- D Şıkkı -->
                            <div class="flex items-center gap-3 group">
                                <div class="w-8 h-8 flex items-center justify-center bg-white border border-slate-300 rounded-full font-bold text-slate-600 group-hover:border-indigo-400 group-hover:text-indigo-600 transition-colors shadow-sm">D</div>
                                <input type="text" id="guncelleSecenekD" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all shadow-sm" placeholder="D şıkkı">
                                <label class="cursor-pointer">
                                    <input type="radio" name="dogruCevap" value="D" class="peer hidden">
                                    <div class="w-8 h-8 rounded-full border-2 border-slate-300 peer-checked:border-green-500 peer-checked:bg-green-500 text-white flex items-center justify-center transition-all hover:bg-slate-100">
                                        <i data-lucide="check" class="w-4 h-4 opacity-0 peer-checked:opacity-100"></i>
                                    </div>
                                </label>
                            </div>

                            <!-- E Şıkkı -->
                            <div class="flex items-center gap-3 group">
                                <div class="w-8 h-8 flex items-center justify-center bg-white border border-slate-300 rounded-full font-bold text-slate-600 group-hover:border-indigo-400 group-hover:text-indigo-600 transition-colors shadow-sm">E</div>
                                <input type="text" id="guncelleSecenekE" class="flex-1 px-4 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-indigo-500 transition-all shadow-sm" placeholder="E şıkkı (Opsiyonel)">
                                <label class="cursor-pointer">
                                    <input type="radio" name="dogruCevap" value="E" class="peer hidden">
                                    <div class="w-8 h-8 rounded-full border-2 border-slate-300 peer-checked:border-green-500 peer-checked:bg-green-500 text-white flex items-center justify-center transition-all hover:bg-slate-100">
                                        <i data-lucide="check" class="w-4 h-4 opacity-0 peer-checked:opacity-100"></i>
                                    </div>
                                </label>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- SAĞ KOLON: Görsel ve Ayarlar (4 birim) -->
                <div class="lg:col-span-4 space-y-6">
                    
                    <!-- Görsel Alanı -->
                    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <div class="bg-slate-50 px-4 py-3 border-b border-slate-200 font-medium text-slate-700 flex items-center gap-2">
                            <i data-lucide="image" class="w-4 h-4 text-purple-600"></i>
                            Görsel Ayarları
                        </div>
                        <div class="p-4 space-y-4">
                            <!-- Görsel Yükle -->
                            <div id="gorselArea" class="relative group">
                                <div id="gorselPlaceholder" class="border-2 border-dashed border-slate-300 rounded-lg p-6 text-center hover:border-purple-400 hover:bg-purple-50 transition-all cursor-pointer" onclick="document.getElementById('guncelleGorselInput').click()">
                                    <i data-lucide="upload" class="w-8 h-8 mx-auto text-slate-400 mb-2 group-hover:text-purple-500"></i>
                                    <p class="text-xs text-slate-500">Görsel yüklemek için tıklayın</p>
                                </div>
                                <div id="gorselPreviewContainer" class="hidden relative">
                                    <img id="gorselPreviewImg" src="" class="w-full h-40 object-contain bg-slate-100 rounded-lg border">
                                    <button type="button" onclick="gorselKaldir()" class="absolute top-2 right-2 bg-red-500 text-white p-1 rounded shadow hover:bg-red-600 transition-all">
                                        <i data-lucide="trash-2" class="w-4 h-4"></i>
                                    </button>
                                </div>
                                <input type="file" id="guncelleGorselInput" class="hidden" accept="image/*" onchange="gorselYukle(this)">
                            </div>

                            <!-- Görsel Konumu -->
                            <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Konum</label>
                                <select id="guncelleGorselKonum" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-purple-500">
                                    <option value="ustte">⬆️ Sorunun Üstünde</option>
                                    <option value="arada" selected>↕️ Metin ve Şıklar Arasında</option>
                                    <option value="yanda">➡️ Sağ Tarafta</option>
                                </select>
                            </div>
                        </div>
                    </div>

                    <!-- Düzen Ayarları -->
                    <div class="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
                        <div class="bg-slate-50 px-4 py-3 border-b border-slate-200 font-medium text-slate-700 flex items-center gap-2">
                            <i data-lucide="settings-2" class="w-4 h-4 text-blue-600"></i>
                            Diğer Ayarlar
                        </div>
                        <div class="p-4 space-y-4">
                            <!-- Şık Düzeni -->
                            <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Şık Düzeni</label>
                                <select id="guncelleSikDuzeni" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm focus:outline-none focus:border-blue-500">
                                    <option value="alt_alta" selected>⬇️ Alt Alta (Standart)</option>
                                    <option value="yan_yana">➡️ Yan Yana (Tek Satır)</option>
                                    <option value="iki_sutun">🔲 İki Sütun</option>
                                </select>
                            </div>

                            <!-- Puan -->
                            <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Puan</label>
                                <div class="flex items-center gap-2">
                                    <input type="number" id="guncellePuan" class="flex-1 px-3 py-2 border border-slate-200 rounded-lg text-sm font-bold text-center" min="1" max="100">
                                    <span class="text-sm text-slate-500">Puan</span>
                                </div>
                            </div>
                            
                            <!-- Zorluk -->
                            <div>
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Zorluk</label>
                                <select id="guncelleZorluk" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm">
                                    <option value="Kolay">🟢 Kolay</option>
                                    <option value="Orta">🟡 Orta</option>
                                    <option value="Zor">🔴 Zor</option>
                                </select>
                            </div>

                            <div class="mt-2">
                                <label class="text-xs font-semibold text-slate-500 uppercase mb-1 block">Konu</label>
                                <input type="text" id="guncelleKonu" class="w-full px-3 py-2 border border-slate-200 rounded-lg text-sm" placeholder="Konu etiketi">
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Footer Buttons -->
            <div class="flex items-center justify-end gap-3 pt-4 border-t border-slate-100">
                <button type="button" onclick="kapatSoruGuncelleModal()"
                    class="px-6 py-2.5 rounded-lg text-slate-600 hover:bg-slate-100 font-medium transition-all text-sm">
                    İptal
                </button>
                <button type="submit"
                    class="px-8 py-2.5 rounded-lg bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-medium shadow-lg hover:shadow-xl hover:translate-y-[-1px] transition-all text-sm flex items-center gap-2">
                    <i data-lucide="save" class="w-4 h-4"></i>
                    Kaydet
                </button>
            </div>
        </form>
    </div>
</div>
"""
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def update_soru_bankasi_js():
    file_path = os.path.join(BASE_DIR, 'templates/soru_bankasi.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    js_code = """
    // Görsel Yükleme Fonksiyonu
    async function gorselYukle(input) {
        if (input.files && input.files[0]) {
            const formData = new FormData();
            formData.append('gorsel', input.files[0]);

            logger.bilgi('Görsel yükleniyor...');
            
            try {
                const response = await fetch('/gorsel-yukle', {
                    method: 'POST',
                    body: formData
                });
                const data = await response.json();

                if (data.basarili) {
                    document.getElementById('guncelleGorselYolu').value = data.dosya_yolu;
                    document.getElementById('gorselPreviewImg').src = data.dosya_yolu;
                    document.getElementById('gorselPlaceholder').classList.add('hidden');
                    document.getElementById('gorselPreviewContainer').classList.remove('hidden');
                    toastGoster('Görsel başarıyla yüklendi', 'success');
                } else {
                    toastGoster(data.mesaj, 'error');
                }
            } catch (error) {
                console.error('Yükleme hatası:', error);
                toastGoster('Görsel yüklenirken hata oluştu', 'error');
            }
        }
    }

    function gorselKaldir() {
        document.getElementById('guncelleGorselYolu').value = '';
        document.getElementById('guncelleGorselInput').value = '';
        document.getElementById('gorselPlaceholder').classList.remove('hidden');
        document.getElementById('gorselPreviewContainer').classList.add('hidden');
    }

    // Puan değişince hafızaya al
    document.getElementById('guncellePuan').addEventListener('change', (e) => {
        localStorage.setItem('sonAyarlananPuan', e.target.value);
    });

    // Soru Güncelleme Modal Fonksiyonları
    async function soruDuzenle(soruId) {
        try {
            logger.bilgi('Soru bilgileri getiriliyor', { soruId });
            
            const response = await fetch(`/soru/${soruId}`);
            const data = await response.json();
            
            if (data.basarili) {
                const soru = data.soru;
                
                // Form alanlarını doldur
                document.getElementById('guncelleSoruId').value = soru.id;
                document.getElementById('guncellenecekSoruId').textContent = soru.id;
                document.getElementById('guncelleSoruMetni').value = soru.soru_metni || '';
                
                document.getElementById('guncelleSecenekA').value = soru.secenek_a || '';
                document.getElementById('guncelleSecenekB').value = soru.secenek_b || '';
                document.getElementById('guncelleSecenekC').value = soru.secenek_c || '';
                document.getElementById('guncelleSecenekD').value = soru.secenek_d || '';
                document.getElementById('guncelleSecenekE').value = soru.secenek_e || '';
                
                // Radyo butonu seçimi (Doğru Cevap)
                const cevap = soru.dogru_cevap || 'A';
                const radyo = document.querySelector(`input[name="dogruCevap"][value="${cevap}"]`);
                if (radyo) radyo.checked = true;

                document.getElementById('guncelleKonu').value = soru.konu || '';
                document.getElementById('guncelleZorluk').value = soru.zorluk || 'Orta';
                document.getElementById('guncellePuan').value = soru.puan || 5;

                // Yeni Alanlar
                document.getElementById('guncelleGorselKonum').value = soru.gorsel_konum || 'arada';
                document.getElementById('guncelleSikDuzeni').value = soru.sik_duzeni || 'alt_alta';
                
                // Görsel alanı
                if (soru.gorsel_yolu) {
                    document.getElementById('guncelleGorselYolu').value = soru.gorsel_yolu;
                    document.getElementById('gorselPreviewImg').src = soru.gorsel_yolu;
                    document.getElementById('gorselPlaceholder').classList.add('hidden');
                    document.getElementById('gorselPreviewContainer').classList.remove('hidden');
                } else {
                    gorselKaldir();
                }
                
                document.getElementById('soruGuncelleModal').classList.remove('hidden');
                setTimeout(() => lucide.createIcons(), 100);
            }
        } catch (error) {
            console.error(error);
            toastGoster('Soru bilgileri alınırken hata oluştu', 'error');
        }
    }

    // Submit Handler
    document.getElementById('soruGuncelleForm').addEventListener('submit', async (e) => {
        e.preventDefault();
        const soruId = document.getElementById('guncelleSoruId').value;
        
        // Doğru cevabı al
        const secilenCevap = document.querySelector('input[name="dogruCevap"]:checked')?.value || 'A';

        const soruData = {
            soru_metni: document.getElementById('guncelleSoruMetni').value,
            secenek_a: document.getElementById('guncelleSecenekA').value,
            secenek_b: document.getElementById('guncelleSecenekB').value,
            secenek_c: document.getElementById('guncelleSecenekC').value,
            secenek_d: document.getElementById('guncelleSecenekD').value,
            secenek_e: document.getElementById('guncelleSecenekE').value,
            dogru_cevap: secilenCevap,
            konu: document.getElementById('guncelleKonu').value,
            zorluk: document.getElementById('guncelleZorluk').value,
            puan: parseInt(document.getElementById('guncellePuan').value),
            
            // Yeni alanlar
            gorsel_yolu: document.getElementById('guncelleGorselYolu').value,
            gorsel_konum: document.getElementById('guncelleGorselKonum').value,
            sik_duzeni: document.getElementById('guncelleSikDuzeni').value
        };

        try {
            const response = await apiIstegi(`/soru-guncelle/${soruId}`, {
                method: 'PUT',
                body: JSON.stringify(soruData)
            });

            toastGoster('Soru başarıyla güncellendi!', 'success');
            kapatSoruGuncelleModal();
            setTimeout(() => location.reload(), 500);
        } catch (error) {
            console.error('Hata:', error);
        }
    });
"""

    # Eski kodu bulup değiştireceğiz ama çok uzun olduğu için fonksiyon bloklarını değiştirelim
    
    # 1. soruDuzenle fonksiyonunu değiştir
    start_tag = "// Soru Güncelleme Modal Fonksiyonları"
    if start_tag in content:
        # Regex kullanmadan basitçe bul ve değiştir denemesi
        # Bu biraz riskli çünkü tüm içeriği match etmek zor.
        # En iyisi dosyayı JS kısmına kadar okuyup, scriptin içini tamamen yenisiyle değiştirmek.
        pass

    # Kısmi değiştirme yapalım
    # soruDuzenle fonksiyonunu eskisi ile değiştir
    if "async function soruDuzenle(soruId)" in content:
        # Eski fonksiyonun bitişini bulmak zor olabilir.
        # Dosyanın sonundaki scripti tamamen değiştirelim?
        # En güvenlisi bu scripti dosyanın sonundaki script bloğuna eklemek.
        # Sadece soruDuzenle'yi değiştirmeliyiz.
        pass
        
    # Python ile içeriği değiştirmek zor olacağı için, basit replace yapalım
    new_content = content.replace("async function soruDuzenle(soruId) {", js_code + "\n\n/* Eski Fonksiyon Override Edildi */ \nasync function eskiSoruDuzenle(id) {")
    
    # Aslında daha temiz yöntem: soru_bankasi.html'deki <script> bloğunu komple yenisiyle değiştirmek.
    # Ancak içinde filtreleme, silme vb. diğer fonksiyonlar da var.
    
    # Çözüm: "Soru Güncelleme Modal Fonksiyonları" comment'inden sonrasını silip yenisini eklemek.
    if "// Soru Güncelleme Modal Fonksiyonları" in content:
        parts = content.split("// Soru Güncelleme Modal Fonksiyonları")
        new_content = parts[0] + js_code + "\n\n    function filtreleriTemizle" + parts[1].split("function filtreleriTemizle")[1]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

if __name__ == "__main__":
    update_modal_html()
    update_soru_bankasi_js()
