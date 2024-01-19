# Gunakan gambar resmi Python
FROM python:3.8-slim

# Set kerja direktori ke /app
WORKDIR /app

# Salin file dependensi ke direktori kerja
COPY requirements.txt .

# Install dependensi
RUN pip install --no-cache-dir -r requirements.txt

# Salin konten proyek ke dalam image
COPY . .

# Eksekusi aplikasi saat container dimulai
CMD ["python", "app.py"]
