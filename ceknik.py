from flask import Flask, request, jsonify
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

app = Flask(__name__)

@app.route('/cek_dpt', methods=['GET'])
def cek_dpt():
    nik = request.args.get('nik')
    if not nik:
        return jsonify({'error': 'Parameter NIK tidak ditemukan'}), 400

    website = 'https://cekdptonline.kpu.go.id/'

    # Gunakan Chrome Headless untuk menjalankan tanpa UI
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    try:
        driver.get(website)
        pencarian = driver.find_element(By.XPATH, '//input[@class="form-control is-valid"]')
        pencarian.clear()
        pencarian.send_keys(nik)
        pencarian.send_keys(Keys.RETURN)

        element = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="row row-1"]')))
        element = driver.find_element("xpath", '//div[@class="row row-1"]')
        hasil = element.text
        lines = hasil.split('\n')
        nama_pemilih = lines[1] if len(lines) > 1 else ''
        tps = lines[3] if len(lines) > 3 else ''

        element_2 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//div[@class="row row-1"]')))
        element_2 = driver.find_element("xpath", '//div[@class="row row-3"]')
        hasil_2 = element_2.text
        lines_2 = hasil_2.split('\n')
        kabupaten = lines_2[1] if len(lines_2) > 1 else ''
        kecamatan = lines_2[3] if len(lines_2) > 3 else ''
        kelurahan = lines_2[5] if len(lines_2) > 5 else ''

        element_3 = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '//p[@class="row--left"]')))
        element_3 = driver.find_elements("xpath", '//p[@class="row--left"]')
        if element_3 and len(element_3) >= 2:
            element_yang_kedua = element_3[1]
            hasil_3 = element_yang_kedua.text
            lines_3 = hasil_3.split('\n')
            alamat = lines_3[1] if len(lines_3) > 1 else ''

        individual_data = {
            'Nama_Pemilih': nama_pemilih,
            'NIK': nik,
            'TPS': tps,
            'Kabupaten': kabupaten,
            'Kecamatan': kecamatan,
            'Kelurahan': kelurahan,
            'Alamat_TPS': alamat
        }

        return jsonify({'data': individual_data}), 200
    except TimeoutException:
        return jsonify({'error': 'NIK tidak terdaftar sebagai DPT'}), 404
    finally:
        driver.quit()

if __name__ == '__main__':
    app.run(debug=False)
