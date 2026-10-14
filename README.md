# Landing Page DVN × Glow Lab (draft)

Draft LP baru untuk menggantikan https://web.glowlab.id/DVNGlowlab.
Satu file statis (`index.html`): tidak perlu build, bisa di-hosting di mana saja.

## Struktur halaman

| # | Section | Anchor |
|---|---|---|
| 0 | Hero: headline masalah, badge, CTA | `#hero` |
| 1 | Problem | `#masalah` |
| 2 | Solusi (+ kutipan Ce Silvi) | `#solusi` |
| 3 | Komposisi (bahan → fungsi) + cara konsumsi | `#komposisi` |
| 4 | Hasil / testimoni | `#testimoni` |
| 5 | Sertifikat + keaslian + verifikasi distributor | `#sertifikat` |
| 6 | Penawaran + FAQ | `#penawaran`, `#faq` |
| 7 | CTA akhir | `#order` |

Preview: buka `index.html` di browser. Teks berlatar kuning = placeholder, kotak bergaris = gambar yang belum diunggah.

## Checklist sebelum live

**Konfigurasi**
- [ ] `WA_NUMBER` di bagian `<script>` paling bawah: nomor WA Ce Silvi (format `628...`)
- [ ] Meta Pixel di `<head>`: ganti `PIXEL_ID` lalu aktifkan. Setiap klik tombol WA mengirim event `Contact` dengan `content_name` = posisi tombol (`wa_hero`, `wa_testimoni`, dst.)

**Konten & kepatuhan**
- [ ] Konfirmasi kebijakan distributor dari pusat: boleh tampilkan harga/promo/bonus? boleh pakai testimoni?
- [ ] Section Penawaran: isi atau hapus `.price-box`, COD, dan bonus sesuai kebijakan
- [ ] Section Komposisi: cocokkan semua teks dengan klaim yang disetujui di registrasi BPOM
- [ ] Section Problem: validasi 4 keluhan dengan riwayat chat pelanggan
- [ ] Testimoni: ganti semua placeholder dengan testimoni asli + izin tertulis (hindari before–after dramatis)
- [ ] Nomor registrasi BPOM, nomor sertifikat Halal, ID distributor
- [ ] URL website resmi untuk cek QR
- [ ] Kutipan Ce Silvi di section Solusi disetujui oleh Ce Silvi

**Gambar** (taruh di `assets/`, nama file harus sama; otomatis tampil menggantikan placeholder)

| File | Isi | Rasio |
|---|---|---|
| `hero-silvi.webp` | Ce Silvi memegang produk | 4:5 |
| `silvi-avatar.webp` | Foto wajah Ce Silvi | 1:1 |
| `produk-dvn.webp` | Foto produk tanpa teks | 1:1 |
| `testi-1.webp` … `testi-3.webp` | Foto profil pemberi testimoni (opsional) | 1:1 |
| `chat-1.webp` … `chat-3.webp` | Screenshot chat testimoni (blur nama & nomor) | 9:16 |
| `sertifikat-bpom.webp` | Sertifikat BPOM | 3:4 |
| `sertifikat-halal.webp` | Sertifikat Halal | 3:4 |
| `verifikasi-distributor.webp` | Screenshot verifikasi distributor | 9:16 |

Logo DVN & Glow Lab: ganti teks di `<header class="topbar">` dengan file logo.

Kompres gambar ke WebP (target < 200 KB per gambar) supaya halaman cepat dibuka di HP.
