# Proyek Deteksi Plat Nomor dengan OpenCV dan EasyOCR

Proyek ini bertujuan untuk mendeteksi plat nomor kendaraan pada video menggunakan metode **Deteksi Kontur** dan **OCR (Optical Character Recognition)**. Hasil dari setiap tahap pemrosesan gambar, seperti grayscale, peningkatan kontras, deteksi tepi dengan Canny, dan kontur yang terdeteksi, diekspor ke file gambar `.jpg`.

## Kontak & Media Sosial
Nama: Ade Maulana
Instagram: @ademaulana_
TikTok: @ademaulana_4

## Fitur

- **Deteksi Plat Nomor**: Menggunakan metode deteksi kontur untuk mendeteksi area yang kemungkinan merupakan plat nomor kendaraan.
- **Pengolahan Gambar**: Menggunakan OpenCV untuk mengubah gambar menjadi grayscale, meningkatkan kontras, dan mendeteksi tepi.
- **OCR dengan EasyOCR**: Menggunakan EasyOCR untuk mengekstrak teks dari plat nomor yang terdeteksi.
- **Ekspor Hasil Pemrosesan**: Gambar hasil dari setiap tahap pemrosesan (grayscale, enhanced grayscale, edges, dan kontur) diekspor dalam format `.jpg` untuk dianalisis lebih lanjut.
  
## Prasyarat

Sebelum menjalankan proyek ini, pastikan Anda sudah menginstal semua dependensi yang dibutuhkan.

### 1. **Install OpenCV**
   OpenCV digunakan untuk memproses video dan gambar.

   ```bash
   pip install opencv-python

