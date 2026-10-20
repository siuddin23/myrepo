# Pasang landing page DVN di Berdu

File di folder ini adalah potongan HTML per section, siap ditempel di blok **HTML / Embed / Kode Kustom** di editor halaman Berdu.

## Pilih salah satu cara

**Cara A: satu blok (paling cepat)**
1. Di Berdu, buat halaman baru, lalu tambahkan satu blok HTML / kode kustom.
2. Buka `lp-lengkap-1-blok.html` dengan Notepad/TextEdit, salin semua isinya, lalu tempel ke blok itu.
3. Simpan dan pratinjau.

**Cara B: per section (bisa diatur ulang urutannya di Berdu)**
1. Tambahkan blok HTML paling atas, lalu tempel isi `00-global.html`. Blok ini wajib dan cukup **sekali** di halaman (berisi font dan semua gaya).
2. Tambahkan blok HTML baru untuk tiap section, urut:

| File | Isi |
|---|---|
| `01-header.html` | Logo + menu + tombol WA. **Opsional**: lewati jika memakai header bawaan Berdu |
| `02-hero.html` | Hero: judul, foto Silvia, Gratis Ongkir / COD, tombol WA |
| `03-problem.html` | Checklist keluhan (interaktif) |
| `04-solusi.html` | Solusi + 2 tablet/hari + keunggulan |
| `05-komposisi.html` | Orbit 7 bahan (interaktif) |
| `06-testimoni.html` | 4 screenshot paket diterima |
| `07-sertifikat.html` | Sertifikat Halal & BPOM, cara cek keaslian, dealer terverifikasi |
| `08-cta.html` | Ajakan akhir |
| `09-tombol-wa-melayang.html` | Tombol WhatsApp bulat di kanan bawah |

Section bisa dihapus atau ditukar urutannya, asal `00-global.html` tetap ada di atas.

## Pengaturan blok di Berdu

- Atur blok/section ke **lebar penuh** dan **padding 0**, supaya latar warna tiap section menyentuh tepi layar.
- Jika Berdu tidak punya opsi lebar penuh, ganti `<div class="dvn-lp">` di awal potongan menjadi `<div class="dvn-lp dvn-full">`.
- Jika setelah itu muncul scroll ke samping, kembalikan ke `<div class="dvn-lp">`.

## Yang perlu diketahui

- **Gambar** diambil dari `https://dvn-glowlab-lp.vercel.app/assets/`. Project Vercel itu harus tetap aktif dan sudah berisi file `assets/` terbaru. Kalau ingin memakai gambar yang diunggah ke Berdu, ganti alamat itu dengan alamat gambar di Berdu (cari & ganti di file).
- **Tombol WhatsApp** sudah berisi nomor +62 812-8333-5822 dan pesan otomatis per tombol. Tombol tetap jalan walau Berdu memblokir script.
- **Meta Pixel**: pasang Pixel lewat pengaturan integrasi/tracking di Berdu. Begitu Pixel aktif, setiap klik tombol WA otomatis mengirim event `Contact` (`wa_hero`, `wa_solusi`, dst.).
- **Bagian interaktif** (checklist keluhan, orbit Komposisi, titik carousel Testimoni) butuh `<script>`. Jika Berdu membuang script, tampilan tetap utuh (bahan pertama tampil di orbit), hanya tidak bisa diklik.
- **Gaya terisolasi**: semua gaya diberi awalan `.dvn-lp`, jadi tidak mengubah tampilan halaman Berdu lain dan tidak mudah tertimpa tema.

## Memperbarui potongan

Semua file di folder ini dibuat otomatis dari `index.html`. Setelah `index.html` diubah, jalankan:

```
python3 tools/build_berdu.py
```

Untuk gambar dari host lain: `python3 tools/build_berdu.py --base https://alamat-gambar-anda/`
