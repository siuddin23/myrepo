# Landing Page DVN × Glow Lab

LP baru untuk menggantikan https://web.glowlab.id/DVNGlowlab.
Satu file statis (`index.html`) + gambar di `assets/`: tidak perlu build, tanpa library JS, bisa di-hosting di mana saja.
Desain mobile-first (diuji di lebar 390 px dan 1280 px).

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

Sticky CTA WhatsApp muncul di HP setelah tombol hero terlewati. Semua animasi mati otomatis jika perangkat memakai pengaturan *reduce motion*.

Data 7 bahan (nama, deskripsi, warna, gambar) ada di array `INGREDIENTS` di `<script>` paling bawah.

## Checklist sebelum live

**Konfigurasi**
- [ ] `WA_NUMBER` di bagian `<script>` paling bawah: nomor WA Ce Silvi (format `628...`)
- [ ] Meta Pixel di `<head>`: ganti `PIXEL_ID` lalu aktifkan. Setiap klik tombol WA mengirim event `Contact` dengan `content_name` = posisi tombol (`wa_hero`, `wa_solusi`, `wa_testimoni`, `wa_final`, `wa_sticky`)
- [ ] `og:image` memakai path relatif; ganti ke URL absolut setelah domain final diketahui

**Konten & kepatuhan**
- [ ] Nomor registrasi BPOM & nomor sertifikat Halal (masih `[nomor]`)
- [ ] Cocokkan deskripsi bahan di `INGREDIENTS` dengan klaim yang disetujui BPOM
- [ ] Izin pelanggan untuk screenshot testimoni (foto profil sudah diblur); isi atau hapus kartu slot ketiga
- [ ] Konfirmasi Free ongkir & COD masih berlaku
- [ ] Hindari kata: kusam, kasar, glowing, cerah. Pakai: sehat, lembap, kenyal

**Gambar** (`assets/`, semua WebP, total ±330 KB; selain foto hero semuanya lazy-load)

| File | Isi | Catatan |
|---|---|---|
| `hero-silvi.webp` | Ce Silvi memegang produk, background sudah dihapus | |
| `bottle.webp`, `tablets.webp` | Foto produk transparan | |
| `ing-*.webp` | Ikon 7 bahan (dari infografis 7 Kandungan) | `ing-vc.webp` dibuat ulang, belum ada ikon resmi Vitamin C |
| `testi-1.webp`, `testi-2.webp` | Screenshot chat paket diterima | Foto profil diblur |
| `cert-halal-*.webp`, `cert-bpom-*.webp`, `badges.webp`, `verified.webp` | Sertifikat, strip logo, kartu VERIFIED | **Ganti dengan file asli resolusi tinggi** (sekarang crop dari screenshot LP lama) |
| `og-dvn.jpg` | Gambar preview saat link dibagikan | |
