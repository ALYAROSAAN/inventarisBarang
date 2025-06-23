# app/Dockerfile
# Menggunakan base image python
FROM python:3.9-slim

# Set working directory di dalam container
WORKDIR /app

# Salin file requirements dan install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin semua file dari direktori lokal ke working directory di container
COPY . .

# Perintah yang akan dijalankan saat container启动
# Menggunakan host 0.0.0.0 agar bisa diakses dari luar container
CMD ["python", "app.py"]