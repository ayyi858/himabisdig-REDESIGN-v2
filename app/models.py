from django.db import models
from django.utils.text import slugify

class Jabatan(models.Model):
    nama = models.CharField(max_length=150)

    def __str__(self):
        return self.nama

class Pengurus(models.Model):
    nama = models.CharField(max_length=200)
    jabatan = models.ForeignKey(Jabatan, on_delete=models.SET_NULL, null=True, related_name='anggota')
    foto = models.ImageField(upload_to='pengurus/', blank=True, null=True)
    periode = models.CharField(max_length=50) # ex: 2024/2025

    def __str__(self):
        return self.nama

EKOSISTEM_CHOICES = (
    ('data_analyst', 'Data Analyst & Visualisasi'),
    ('saham_crypto', 'Saham & Cryptocurrency'),
    ('desain_video', 'Desain & Videography'),
    ('humaniora', 'Humaniora'),
    ('minat_bakat', 'Minat & Bakat'),
    ('kewirausahaan', 'Kewirausahaan'),
)

class Kegiatan(models.Model):
    MODE_SELEKSI = (
        ('auto', 'Auto Approve'),
        ('manual', 'Manual Approval'),
    )
    judul = models.CharField(max_length=200)
    ekosistem = models.CharField(max_length=50, choices=EKOSISTEM_CHOICES, blank=True, null=True)
    deskripsi = models.TextField()
    tanggal = models.DateTimeField()
    lokasi = models.CharField(max_length=200)
    poster = models.ImageField(upload_to='kegiatan/', blank=True, null=True)
    mode_seleksi = models.CharField(max_length=20, choices=MODE_SELEKSI, default='manual')
    
    # Brief details
    brief_deskripsi = models.TextField(blank=True, help_text="Deskripsi tugas untuk peserta")
    brief_link_wa = models.URLField(blank=True, help_text="Link Grup WhatsApp")
    brief_deadline = models.DateTimeField(blank=True, null=True)
    brief_instruksi = models.TextField(blank=True)

    def __str__(self):
        return self.judul

class Peserta(models.Model):
    STATUS_P = (
        ('mahasiswa', 'Mahasiswa'),
        ('umum', 'Umum'),
    )
    STATUS_L = (
        ('pending', 'Pending'),
        ('approved', 'Diterima'),
        ('rejected', 'Ditolak'),
    )
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='pendaftar')
    nama = models.CharField(max_length=200)
    email = models.EmailField()
    no_wa = models.CharField(max_length=20)
    status_pendaftar = models.CharField(max_length=20, choices=STATUS_P)
    link_wa = models.URLField(blank=True, help_text="Link Whatsapp Opsional")
    status_kelolosan = models.CharField(max_length=20, choices=STATUS_L, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} - {self.kegiatan.judul}"

class Absensi(models.Model):
    STATUS_K = (
        ('peserta', 'Peserta'),
        ('tamu', 'Tamu'),
    )
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='absensi')
    nama = models.CharField(max_length=200)
    status_kehadiran = models.CharField(max_length=20, choices=STATUS_K)
    tanda_tangan = models.TextField(blank=True, null=True, help_text="Data Base64 Tanda Tangan")
    waktu = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nama} - {self.kegiatan.judul}"

class Berita(models.Model):
    judul = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    gambar = models.ImageField(upload_to='berita/')
    konten = models.TextField()
    ekosistem = models.CharField(max_length=50, choices=EKOSISTEM_CHOICES, blank=True, null=True)
    tanggal = models.DateField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.judul

class Dokumentasi(models.Model):
    kegiatan = models.ForeignKey(Kegiatan, on_delete=models.CASCADE, related_name='dokumentasi', null=True, blank=True)
    ekosistem = models.CharField(max_length=50, choices=EKOSISTEM_CHOICES, blank=True, null=True)
    foto = models.ImageField(upload_to='dokumentasi/')
    deskripsi = models.CharField(max_length=200, blank=True)

class PesanKontak(models.Model):
    nama = models.CharField(max_length=150)
    email = models.EmailField()
    pesan = models.TextField()
    tanggal = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Pesan dari {self.nama}"
