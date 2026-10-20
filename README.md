# Landing Page DVN × Glow Lab

LP baru untuk menggantikan https://web.glowlab.id/DVNGlowlab.
Satu file statis (`index.html`) + gambar di `assets/`: tidak perlu build, tanpa library JS, bisa di-hosting di mana saja.
Desain mobile-first dan adaptif: HP (<640 px), tablet (640–899 px), desktop (≥900 px, header lengket dengan navigasi + tombol WA). Diuji di 390, 768, 1280 dan 1440 px.

## Struktur halaman

| # | Section | Anchor | Interaksi |
|---|---|---|---|
| 0 | Header + hook masalah, foto Ce Silvi, CTA | `#hero` | |
| 1 | Problem: checklist keluhan | `#masalah` | Kartu bisa diketuk, meter & pesan berubah |
| 2 | Solusi: Skincare + DVN, 2 tablet/hari, keunggulan | `#solusi` | |
| 3 | Komposisi: 7 bahan mengorbit botol | `#komposisi` | Auto-tour saat terlihat, ketuk bahan, filter Kelembapan/Antioksidan |
| 4 | Testimoni: screenshot paket diterima | `#testimoni` | Carousel geser + dot |
| 5 | Sertifikat: Halal, BPOM, cek keaslian, dealer terverifikasi | `#sertifikat` | |
| 6 | CTA akhir | `#order` | |

Tombol WhatsApp melayang di kanan bawah tampil di semua ukuran layar (di desktop muncul label "Chat Ce Silvi" saat di-hover). Semua animasi mati otomatis jika perangkat memakai pengaturan *reduce motion*.

Data 7 bahan (nama, deskripsi, warna, gambar) ada di array `INGREDIENTS` di `<script>` paling bawah.

## Checklist sebelum live

**Konfigurasi**
- [x] `WA_NUMBER` sudah diisi: +62 812-8333-5822 (`6281283335822`) untuk semua tombol WhatsApp
- [ ] Meta Pixel di `<head>`: ganti `PIXEL_ID` (ambil dari LP lama / Events Manager) lalu aktifkan. Setiap klik tombol WA mengirim event `Contact` dengan `content_name` = posisi tombol (`wa_header`, `wa_hero`, `wa_solusi`, `wa_testimoni`, `wa_final`, `wa_float`)
- [ ] `og:image` memakai path relatif; ganti ke URL absolut setelah domain final diketahui

**Konten & kepatuhan**
- [ ] Nomor registrasi BPOM & nomor sertifikat Halal (masih `[nomor]`)
- [ ] Cocokkan deskripsi bahan di `INGREDIENTS` dengan klaim yang disetujui BPOM
- [ ] Izin pelanggan untuk 3 screenshot testimoni (foto profil sudah diblur)
- [ ] Konfirmasi Gratis ongkir & COD masih berlaku
- [ ] Hindari kata: kusam, kasar, glowing, cerah. Pakai: sehat, lembap, kenyal
- [x] Copy sudah dievaluasi dengan checklist stop-slop (tanpa kalimat pasif tanpa pelaku, tanpa pull-quote, tanpa em dash)

**Gambar** (`assets/`, semua WebP, total ±330 KB; selain foto hero semuanya lazy-load)

| File | Isi | Catatan |
|---|---|---|
| `hero-silvi.webp` | Silvia memegang botol & kemasan DVN (dari key visual LP lama), background dihapus | |
| `bottle.webp`, `tablets.webp` | Foto produk transparan | |
| `ing-*.webp` | Ikon 7 bahan (dari infografis 7 Kandungan) | `ing-vc.webp` dibuat ulang, belum ada ikon resmi Vitamin C |
| `testi-1.webp` … `testi-3.webp` | Screenshot chat paket diterima | Foto profil diblur |
| `cert-halal-*.webp`, `cert-bpom-*.webp`, `badges.webp`, `verified.webp` | Sertifikat, strip logo, kartu VERIFIED | **Ganti dengan file asli resolusi tinggi** (sekarang crop dari screenshot LP lama) |
| `og-dvn.jpg` | Gambar preview saat link dibagikan | |
