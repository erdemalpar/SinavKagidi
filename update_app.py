import os

# Base URL
BASE_DIR = '/Users/erdem/.gemini/antigravity/scratch/sinav-kagidi'

def update_app_py():
    file_path = os.path.join(BASE_DIR, 'app.py')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Yeni import gerekli mi?
    if "from werkzeug.utils import secure_filename" not in content:
         # genelde app.py başında importlar olur ama fonksiyon içinde import yapacağız simple olsun diye
         pass

    # gorsel_yukle fonksiyonu
    gorsel_yukle_func = """
@app.route('/gorsel-yukle', methods=['POST'])
def gorsel_yukle():
    \"\"\"Soru görseli yükle\"\"\"
    if 'gorsel' not in request.files:
        return jsonify({'basarili': False, 'mesaj': 'Dosya bulunamadı'}), 400
    
    dosya = request.files['gorsel']
    if dosya.filename == '':
        return jsonify({'basarili': False, 'mesaj': 'Dosya seçilmedi'}), 400
        
    if dosya and izin_verilen_dosya(dosya.filename):
        import uuid
        from werkzeug.utils import secure_filename
        
        dosya_adi = secure_filename(dosya.filename)
        ext = dosya_adi.rsplit('.', 1)[1].lower()
        if ext not in {'png', 'jpg', 'jpeg', 'gif'}:
            return jsonify({'basarili': False, 'mesaj': 'Sadece resim dosyaları yüklenebilir'}), 400
            
        yeni_ad = f"soru_{uuid.uuid4().hex[:8]}.{ext}"
        
        # uploads klasörüne kaydet
        kayit_yolu = os.path.join(app.root_path, 'static', 'uploads')
        os.makedirs(kayit_yolu, exist_ok=True)
        dosya.save(os.path.join(kayit_yolu, yeni_ad))
        
        return jsonify({'basarili': True, 'dosya_yolu': f'/static/uploads/{yeni_ad}'})
    
    return jsonify({'basarili': False, 'mesaj': 'Geçersiz dosya'}), 400
"""

    if "@app.route('/gorsel-yukle'" not in content:
        # soru_guncelle'den önce ekle
        if "@app.route('/soru-guncelle" in content:
            content = content.replace("@app.route('/soru-guncelle", gorsel_yukle_func + "\n\n@app.route('/soru-guncelle")
            print("✓ gorsel_yukle eklendi")
    
    # soru_guncelle güncellemesi
    old_update = """        soru.puan = data.get('puan', soru.puan)
        
        db.session.commit()"""
    
    new_update = """        soru.puan = data.get('puan', soru.puan)
        
        # Yeni alanlar
        soru.gorsel_yolu = data.get('gorsel_yolu', soru.gorsel_yolu)
        soru.gorsel_konum = data.get('gorsel_konum', soru.gorsel_konum)
        soru.sik_duzeni = data.get('sik_duzeni', soru.sik_duzeni)
        
        db.session.commit()"""
    
    if old_update in content and "# Yeni alanlar" not in content:
        content = content.replace(old_update, new_update)
        print("✓ soru_guncelle güncellendi")

    # soru_ekle güncellemesi
    old_insert = """            dogru_cevap=data.get('dogru_cevap', 'A'),
            konu=data.get('konu'),
            zorluk=data.get('zorluk', 'Orta'),
            puan=data.get('puan', 5)
        )"""

    new_insert = """            dogru_cevap=data.get('dogru_cevap', 'A'),
            konu=data.get('konu'),
            zorluk=data.get('zorluk', 'Orta'),
            puan=data.get('puan', 5),
            gorsel_yolu=data.get('gorsel_yolu'),
            gorsel_konum=data.get('gorsel_konum', 'arada'),
            sik_duzeni=data.get('sik_duzeni', 'alt_alta')
        )"""

    if old_insert in content and "gorsel_konum=data.get" not in content:
        content = content.replace(old_insert, new_insert)
        print("✓ soru_ekle güncellendi")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    update_app_py()
