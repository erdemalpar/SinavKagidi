import os

# Base URL
BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi'

def fix_base_html():
    file_path = os.path.join(BASE_DIR, 'templates/base.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Sidebar JS kodu
    sidebar_js = """
        // Sidebar Toggle
        const menuToggle = document.getElementById('menuToggle');
        const sidebar = document.getElementById('sidebar');
        const mainContent = document.getElementById('mainContent');
        let sidebarAcik = true;

        if (menuToggle && sidebar && mainContent) {
            menuToggle.addEventListener('click', () => {
                sidebarAcik = !sidebarAcik;
                
                if (sidebarAcik) {
                    sidebar.style.transform = 'translateX(0)';
                    mainContent.style.marginLeft = '16rem'; // ml-64
                    menuToggle.style.left = '17rem'; // butonu da kaydır
                } else {
                    sidebar.style.transform = 'translateX(-100%)';
                    mainContent.style.marginLeft = '0';
                    menuToggle.style.left = '1rem';
                }
                
                logger.bilgi('Sidebar durumu değişti', { acik: sidebarAcik });
            });
        }

        // Aktif sayfa işaretle
        const sidebarLinks = document.querySelectorAll('.sidebar-link');
        const currentPath = window.location.pathname;
        
        sidebarLinks.forEach(link => {
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('bg-indigo-50', 'text-indigo-600');
                link.classList.remove('text-slate-700');
            }
        });

        logger.basarili('Uygulama başlatıldı', {
            sayfa: currentPath,
            zaman: new Date().toLocaleString('tr-TR')
        });
    """

    if "// Sidebar Toggle" not in content:
        # apiIstegi fonksiyonunun sonuna ekle
        target = """            }
        }
    </script>"""
        replacement = """            }
        }
        """ + sidebar_js + """
    </script>"""
        
        if target in content:
            new_content = content.replace(target, replacement)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✓ base.html güncellendi (JS eklendi)")
        else:
            print("✗ base.html hedef bulunamadı")
    else:
        print("✓ base.html zaten güncel")


def fix_soru_bankasi_html():
    file_path = os.path.join(BASE_DIR, 'templates/soru_bankasi.html')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Soru Düzenle JS
    soru_duzenle_js = """
    // Soru Güncelleme Modal Fonksiyonları
    async function soruDuzenle(soruId) {
        try {
            logger.bilgi('Soru bilgileri getiriliyor', { soruId });
            
            // Soru bilgilerini API'den al
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
                document.getElementById('guncelleDogruCevap').value = soru.dogru_cevap || 'A';
                document.getElementById('guncelleKonu').value = soru.konu || '';
                document.getElementById('guncelleZorluk').value = soru.zorluk || 'Orta';
                document.getElementById('guncellePuan').value = soru.puan || 5;
                
                // Modal'ı aç
                document.getElementById('soruGuncelleModal').classList.remove('hidden');
                
                logger.basarili('Soru bilgileri yüklendi', soru);
                
                // İkonları yenile
                setTimeout(() => lucide.createIcons(), 100);
            } else {
                toastGoster(data.mesaj || 'Soru bilgileri alınamadı', 'error');
            }
        } catch (error) {
            logger.hata('Soru bilgileri alınırken hata', error.message);
            toastGoster('Soru bilgileri alınırken hata oluştu', 'error');
        }
    }

    function kapatSoruGuncelleModal() {
        document.getElementById('soruGuncelleModal').classList.add('hidden');
        logger.bilgi('Soru güncelleme modal\\'ı kapatıldı');
    }

    // Soru Güncelleme Form Submit
    document.getElementById('soruGuncelleForm').addEventListener('submit', async (e) => {
        e.preventDefault();

        const soruId = document.getElementById('guncelleSoruId').value;
        const soruData = {
            soru_metni: document.getElementById('guncelleSoruMetni').value,
            secenek_a: document.getElementById('guncelleSecenekA').value,
            secenek_b: document.getElementById('guncelleSecenekB').value,
            secenek_c: document.getElementById('guncelleSecenekC').value,
            secenek_d: document.getElementById('guncelleSecenekD').value,
            secenek_e: document.getElementById('guncelleSecenekE').value,
            dogru_cevap: document.getElementById('guncelleDogruCevap').value,
            konu: document.getElementById('guncelleKonu').value,
            zorluk: document.getElementById('guncelleZorluk').value,
            puan: parseInt(document.getElementById('guncellePuan').value)
        };

        logger.bilgi('Soru güncelleniyor', { soruId, soruData });

        try {
            const data = await apiIstegi(`/soru-guncelle/${soruId}`, {
                method: 'PUT',
                body: JSON.stringify(soruData)
            });

            toastGoster('Soru başarıyla güncellendi!', 'success');
            kapatSoruGuncelleModal();
            
            logger.basarili('Soru güncellendi', { soruId });
            
            // Sayfayı yenile
            setTimeout(() => location.reload(), 1000);
        } catch (error) {
            console.error('Hata:', error);
        }
    });
    """

    # Eski fonksiyonu bul ve değiştir
    if "toastGoster('Düzenleme özelliği yakında eklenecek', 'info');" in content:
        target_func = """    function soruDuzenle(soruId) {
        toastGoster('Düzenleme özelliği yakında eklenecek', 'info');
    }"""
        
        if target_func in content:
            new_content = content.replace(target_func, soru_duzenle_js)
            
            # Modal include ekle
            if "{% include '_soru_guncelle_modal.html' %}" not in new_content:
                new_content = new_content.replace("{% endblock %}", "{% include '_soru_guncelle_modal.html' %}\n\n{% endblock %}")
            
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print("✓ soru_bankasi.html güncellendi")
        else:
            print("✗ soru_bankasi.html fonksiyon bulunamadı")
    else:
        print("✓ soru_bankasi.html zaten güncel")


if __name__ == "__main__":
    fix_base_html()
    fix_soru_bankasi_html()
