# Changelog

Semua perubahan penting pada proyek ini akan dicatat dalam berkas ini.

Format versi mengikuti standar perilisan aplikasi (`x.x.x`).

---

## [2.1.3] - 2026-08-13

### 🌟 Fitur Baru & Peningkatan Kecepatan
- **Pendeteksian Layar Narasi Hitam (*"Tekan untuk melanjutkan"*)**:
  - Menambahkan koordinat `YELLOW_INDICATOR_X` dan `YELLOW_INDICATOR_Y` untuk mendeteksi warna kuning/emas dari simbol diamond & teks pada layar narasi hitam.
  - Memungkinkan skrip melompati layar narasi cerita latar hitam secara otomatis.
- **Peningkatan Kecepatan Penekanan F (8–12 Clicks/sec)**:
  - Mengatur interval penekanan tombol `F` ke **8 s.d 12 kali per detik** (`0.080s - 0.125s`), memberikan respon cepat yang mulus saat men-skip dialog.

## [2.1.2] - 2026-08-13

### ⚡ Optimasi Kecepatan Pengetukan & Performa
- **Optimasi Penekanan Tombol F (5–8 Clicks/sec)**:
  - Mengubah interval penekanan tombol `F` menjadi **5 s.d 8 kali per detik** (`0.125s - 0.200s`), menyerupai kecepatan pengetukan jari manusia secara alami.
- **Peningkatan Pemindaian Piksel Single-Pass (`get_dialogue_state`)**:
  - Menggabungkan pengecekan status dialog menjadi 1 kali pemindaian gambar per loop.
  - Memangkas keterlambatan *screenshot* berulang hingga 70% dan mempercepat penanganan transisi dialog tanpa lag.

## [2.1.1] - 2026-08-12

### 🌟 Fitur Baru
- **Smart Auto-Pause & Smart Auto-Resume**:
  - Otomatis menangguhkan (*suspend*) simulasi tombol saat jendela *Genshin Impact* kehilangan fokus layar (misalnya saat pengguna berpindah ke Browser, Discord, atau aplikasi lain).
  - Otomatis melanjutkan (*resume*) auto-skip saat jendela *Genshin Impact* kembali menjadi fokus aktif.
  - Menampilkan indikasi konsol visual yang jelas (`[SMART AUTO-PAUSE]` dan `[SMART AUTO-RESUME]`) untuk mencegah pengetikan tidak sengaja pada aplikasi lain.

### ⚙️ Pembaruan & Peningkatan
- Pembaruan versi proyek ke `v2.1.1` pada `pyproject.toml` dan skrip utama `autoskip_dialogue.py`.
- Penambahan dokumentasi fitur *Smart Auto-Pause* pada `README.md`.
