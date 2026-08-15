# Changelog

Semua perubahan penting pada proyek ini akan dicatat dalam berkas ini.

Format versi mengikuti standar perilisan aplikasi (`x.x.x`).

---

## [2.1.6] - 2026-08-15

### 🌟 Penyempurnaan Robust UI Detection (Elemen UI Permanen)
- **Deteksi Bar Kontrol Dialog Kiri Atas Multi-Icon**:
  - Menambahkan pemindaian icon permanen Log Dialog (`≡`), Sembunyikan UI (`👁️`), dan Audio (`🔊`) di `X ≈ 140, 180, 218; Y ≈ 45` yang selalu ada berwarna putih pada setiap percakapan normal.
- **Deteksi Rentang Vertikal Pilihan Dialog Kanan (1, 2, atau 3 Pilihan)**:
  - Memindai area gelembung chat `💬` (`X ≈ 1285`) dan kotak `[F]` (`X ≈ 1235`) pada rentang vertikal `Y = 710 s.d 830` piksel.
  - Memastikan kondisi **1 pilihan dialog** (`Y ≈ 750`), **2 pilihan**, maupun **3 pilihan** terdeteksi secara presisi.
- **Koreksi Koordinat Nama Pembicara & Garis Emas Bawah**:
  - Mengoreksi posisi nama pembicara (`CHAR_NAME_Y`) ke `Y ≈ 810` dan garis pembatas emas (`GOLDEN_DIVIDER_Y = 835`).

## [2.1.5] - 2026-08-13

### 🌟 Fitur Baru — Deteksi Multi-Indikator Dialog Karakter
- **Deteksi Nama Karakter Kuning/Emas** (`CHAR_NAME_X/Y`):
  - Memindai strip horizontal sekitar area nama karakter di bagian bawah tengah layar (`Y ≈ 435`).
  - Mendeteksi warna kuning/emas teks nama karakter (seperti *"Alyosha"*, *"Lumine"*, dll) yang hanya muncul saat dialog karakter aktif.
- **Deteksi Kotak Tombol `[F]` di Kanan Tengah** (`F_KEY_BOX_X/Y`):
  - Memindai strip vertikal di sekitar `X ≈ 1280, Y ≈ 400` untuk warna putih/abu-abu terang dari kotak UI tombol `[F]` yang muncul saat giliran interaksi dialog.
  - Fungsi pembantu baru `is_light_grey_or_white()` untuk mengenali warna background kotak tombol.

## [2.1.4] - 2026-08-13

### 🌟 Fitur Baru & Deteksi Objek Simbol Diamond Kuning
- **Pendeteksian Khusus Objek Simbol Diamond Kuning (`◇` / `◆`)**:
  - Mengubah logika pendeteksian agar berfokus 100% pada pemindaian **simbol diamond kuning/emas** yang sering muncul di bagian bawah tengah layar pada berbagai adegan sinematik, dialog, dan narasi.
  - Menerapkan *Multi-Point Vertical Scan Array* pada rentang `Y = 910, 925, 940, 950, 960` dengan toleransi warna emas `R >= 170`, `G >= 120`, `B <= 110`.

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
