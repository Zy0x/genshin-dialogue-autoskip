# Changelog

Semua perubahan penting pada proyek ini akan dicatat dalam berkas ini.

Format versi mengikuti standar perilisan aplikasi (`x.x.x`).

---

## [2.1.1] - 2026-08-12

### 🌟 Fitur Baru
- **Smart Auto-Pause & Smart Auto-Resume**:
  - Otomatis menangguhkan (*suspend*) simulasi tombol saat jendela *Genshin Impact* kehilangan fokus layar (misalnya saat pengguna berpindah ke Browser, Discord, atau aplikasi lain).
  - Otomatis melanjutkan (*resume*) auto-skip saat jendela *Genshin Impact* kembali menjadi fokus aktif.
  - Menampilkan indikasi konsol visual yang jelas (`[SMART AUTO-PAUSE]` dan `[SMART AUTO-RESUME]`) untuk mencegah pengetikan tidak sengaja pada aplikasi lain.

### ⚙️ Pembaruan & Peningkatan
- Pembaruan versi proyek ke `v2.1.1` pada `pyproject.toml` dan skrip utama `autoskip_dialogue.py`.
- Penambahan dokumentasi fitur *Smart Auto-Pause* pada `README.md`.
