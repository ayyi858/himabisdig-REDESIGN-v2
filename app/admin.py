from django.contrib import admin
from .models import *

# ==========================================
# KONFIGURASI ADMIN SITE (RESTRIKSI)
# ==========================================
admin.site.site_header = "Super Admin HIMABISDIG"
admin.site.index_title = "Database & Management System"
admin.site.site_title = "HIMABISDIG Admin"

# Membatasi akses Admin Panel (hanya untuk Superuser)
# CMS Admin (Staff) menggunakan dashboard kustom /cms/
admin.site.has_permission = lambda request: request.user.is_superuser

# ==========================================
# REGISTRASI MODELS
# ==========================================

@admin.register(Jabatan)
class JabatanAdmin(admin.ModelAdmin):
    list_display = ('id', 'nama')
    search_fields = ('nama',)

@admin.register(Pengurus)
class PengurusAdmin(admin.ModelAdmin):
    list_display = ('nama', 'jabatan', 'periode')
    list_filter = ('jabatan', 'periode')
    search_fields = ('nama',)

@admin.register(Kegiatan)
class KegiatanAdmin(admin.ModelAdmin):
    list_display = ('judul', 'ekosistem', 'tanggal', 'lokasi', 'mode_seleksi')
    list_filter = ('ekosistem', 'mode_seleksi', 'tanggal')
    search_fields = ('judul', 'lokasi')

@admin.register(Peserta)
class PesertaAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kegiatan', 'email', 'status_kelolosan', 'created_at')
    list_filter = ('kegiatan', 'status_kelolosan', 'status_pendaftar')
    search_fields = ('nama', 'email', 'no_wa')

@admin.register(Berita)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ('judul', 'ekosistem', 'tanggal')
    list_filter = ('ekosistem', 'tanggal')
    prepopulated_fields = {'slug': ('judul',)}
    search_fields = ('judul', 'konten')

@admin.register(Dokumentasi)
class DokumentasiAdmin(admin.ModelAdmin):
    list_display = ('id', 'kegiatan', 'ekosistem', 'deskripsi')
    list_filter = ('ekosistem', 'kegiatan')

@admin.register(Absensi)
class AbsensiAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kegiatan', 'status_kehadiran', 'waktu')
    list_filter = ('kegiatan', 'status_kehadiran', 'waktu')
    search_fields = ('nama',)

@admin.register(PesanKontak)
class PesanKontakAdmin(admin.ModelAdmin):
    list_display = ('nama', 'email', 'tanggal')
    readonly_fields = ('nama', 'email', 'pesan', 'tanggal')
    search_fields = ('nama', 'email')