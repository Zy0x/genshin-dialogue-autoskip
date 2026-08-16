# Changelog

Semua perubahan penting pada proyek ini akan dicatat dalam berkas ini.

Format versi mengikuti standar perilisan aplikasi (`x.x.x`).

---

## [2.1.10] - 2026-08-16

### 🛡️ Peningkatan Menu Shield (Pengaturan Party & Menu Action Buttons Protection)
- **Multi-Point Scan Tombol Tutup `[X]` Kanan Atas**:
  - Memindai rentang horizontal `X = 1830 s.d 1875` pada `Y ≈ 45` untuk menjamin deteksi tombol Tutup `[X]` pada layar Pengaturan Party (*Party Setup*), Domain, Inventori, Karakter, dan Event.
- **Deteksi Tombol Aksi Menu Pojok Kanan Bawah (`X ≈ 1750, Y ≈ 950`)**:
  - Mendeteksi keberadaan tombol menu bawah seperti `[F] Mulai`, `[F] Solo`, dan `[F] Konfirmasi Simpan`.
  - Mencegah penekanan tombol `F` otomatis saat berada di layar Pengaturan Party sehingga pemain bebas mengatur komposisi tim tanpa tertekan *"Mulai"*.

## [2.1.9] - 2026-08-16

### 🛡️ Dual Master Safety Shield (Eksplorasi Open-World & Menu Domain Protection)
- **Shield 1: Open-World Exploration Immunity (`is_open_world_hud_active`)**:
  - Mendeteksi keberadaan HUD dunia terbuka (Minimap, icon Tas/Wish di kanan atas, dan slot Party 1-2-3-4 di kanan).
  - Menghentikan total penekanan tombol `F` saat pemain sedang bebas menjelajah dunia terbuka, mencegah interaksi tidak sengaja dengan pintu domain liar (*"Binding Field..."*), peti, atau NPC.
- **Shield 2: Menu / Domain Entrance Protection (`is_menu_screen_active`)**:
  - Mendeteksi tombol Tutup `[X]` di pojok kanan atas (`X ≈ 1840, Y ≈ 45`) pada menu Pintu Domain, inventori, dan event.
  - Menjamin pemain bebas memilih tingkat kesulitan domain, mode Co-Op/Solo, dan melihat hadiah tanpa terganggu auto-skip.

## [2.1.8] - 2026-08-15

### 🛡️ Anti-False Positive Shield (Menu/Inventori/Modal Popup Protection)
- **Verifikasi Kontras Gelembung Pilihan Dialog (*Dark Pill Contrast Check*)**:
  - Menambahkan fungsi validasi `is_valid_dialogue_choice()` yang memeriksa apakah icon putih pilihan dialog berada di atas bar pil gelap (`RGB < 130`).
  - Mencegah salah deteksi (*false positive*) dan penekanan tombol `F` yang tidak diinginkan pada popup modal inventori/penyimpanan item/toko yang berlatar belakang krem/putih terang.

## [2.1.7] - 2026-08-15

### ⚡ Peningkatan Kecepatan Deteksi Fokus Jendela (Ultra-Fast Win32)
- **Direct Native Win32 API Window Detection**:
  - Mengganti wrapper judul jendela dengan panggilan kernel langsung `win32gui.GetWindowText(win32gui.GetForegroundWindow())` (latensi < 1 milidetik).
- **Peningkatan Frekuensi Polling Fokus (30ms Polling)**:
  - Memangkas delay tidur saat jendela tidak aktif dari `500ms` menjadi **`30ms`**.
  - Memberikan respon seketika (*instant/real-time*) saat pengguna berpindah ke browser (`[SMART AUTO-PAUSE]`) maupun saat kembali ke Genshin Impact (`[SMART AUTO-RESUME]`).

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
