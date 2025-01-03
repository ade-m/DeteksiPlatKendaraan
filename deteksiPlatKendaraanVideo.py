import cv2
import numpy as np
import easyocr

# Path ke file video
video_path = "/Users/ademaulana/Documents/OCRImg/plate/mobil.mov"

# Inisialisasi EasyOCR Reader
reader = easyocr.Reader(['en'])

def process_frame(frame):
    # Ubah gambar ke grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Meningkatkan kontras gambar untuk membantu deteksi lebih baik
    enhanced_gray = cv2.equalizeHist(gray)
    
    # Canny Edge Detection (lebih baik untuk mendeteksi tepi)
    edges = cv2.Canny(enhanced_gray, threshold1=100, threshold2=200)
    
    # Temukan kontur untuk mendeteksi plat nomor
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Gambar kontur pada frame
    contour_frame = frame.copy()  # Buat salinan frame untuk menggambar kontur
    cv2.drawContours(contour_frame, contours, -1, (0, 255, 0), 2)  # Gambar semua kontur dengan warna hijau dan ketebalan 2
    
    plat = ""

    # Gambar kontur yang ditemukan
    for contour in contours:
        # Hitung bounding box untuk setiap kontur
        x, y, w, h = cv2.boundingRect(contour)

        # Tentukan area yang bisa jadi plat nomor berdasarkan ukuran dan rasio aspek
        aspect_ratio = w / h
        if 2 < aspect_ratio < 5:  # Rasio yang biasanya ditemukan pada plat nomor
            # Ekstrak bagian gambar yang dicurigai sebagai plat nomor
            plate_region = frame[y:y+h, x:x+w]
            
            # Gunakan EasyOCR untuk membaca teks pada area tersebut
            result = reader.readtext(plate_region)
            plat = ""
            # Jika ada teks yang terdeteksi
            if result:                
                for detection in result:
                    text = detection[1]
                    plat += text + " "

                # Menampilkan kotak hijau di sekitar plat nomor
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
                # Menambahkan latar belakang hijau dan teks putih
                font = cv2.FONT_HERSHEY_SIMPLEX
                font_scale = 0.9
                font_thickness = 2
                text_size = cv2.getTextSize(plat, font, font_scale, font_thickness)[0]

                # Gambar rectangle hijau sebagai latar belakang teks
                text_x = x
                text_y = y - 10
                text_width = text_size[0]
                text_height = text_size[1]
                cv2.rectangle(frame, (text_x, text_y - text_height), (text_x + text_width, text_y + 5), (0, 255, 0), -1)

                # Tampilkan teks dengan warna putih di atas latar belakang hijau
                cv2.putText(frame, plat, (text_x, text_y), font, font_scale, (255, 255, 255), font_thickness)
                print(plat)
    return frame

# Muat video
cap = cv2.VideoCapture(video_path)

# Periksa apakah video berhasil dimuat
if not cap.isOpened():
    print("Gagal membuka video.")
    exit()

# Ambil frame rate video (frames per second)
fps = cap.get(cv2.CAP_PROP_FPS)
# Tentukan interval waktu (1 detik)
interval = 1  # Interval waktu dalam detik

# Ambil resolusi video asli
frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# Tentukan resolusi baru (1/2 dari resolusi asli)
new_width = frame_width // 2
new_height = frame_height // 2

# Variabel untuk menghitung waktu yang telah berlalu dalam milidetik
current_time = 0  # Mulai dari detik 0

while True:
    # Atur posisi ke waktu yang diinginkan (setiap 1 detik)
    cap.set(cv2.CAP_PROP_POS_MSEC, current_time * 1000)

    # Baca frame dari video
    
    ret, frame = cap.read()
    
    if not ret:
        print("Video selesai atau tidak bisa dibaca.")
        break

    # Ubah ukuran frame menjadi setengah dari resolusi aslinya
    resized_frame = cv2.resize(frame, (new_width, new_height))

    # Proses frame untuk deteksi plat nomor
    processed_frame = process_frame(resized_frame)

    # Tampilkan frame hasil deteksi
    cv2.imshow("Detected License Plate", processed_frame)

    # Tunggu input tombol
    key = cv2.waitKey(1) & 0xFF

    # Tombol 'q' untuk keluar
    if key == ord('q'):
        break

    # Pindah ke detik berikutnya
    current_time += interval

# Tutup semua jendela OpenCV dan video capture
cap.release()
cv2.destroyAllWindows()
