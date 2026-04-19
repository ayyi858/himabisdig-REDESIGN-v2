from django.urls import path
from . import views, cms_views

urlpatterns = [
    path('', views.home, name='home'),
    path('tentang-kami/', views.tentang_kami, name='tentang_kami'),
    path('ekosistem/<str:ekosistem_slug>/', views.ekosistem_detail, name='ekosistem_detail'),
    path('berita/', views.berita_list, name='berita_list'),
    path('berita/<slug:slug>/', views.berita_detail, name='berita_detail'),
    path('kegiatan/', views.kegiatan_list, name='kegiatan_list'),
    path('kegiatan/<int:pk>/', views.kegiatan_detail, name='kegiatan_detail'),
    path('dokumentasi/', views.dokumentasi, name='dokumentasi'),
    path('kontak/', views.kontak, name='kontak'),

    # CMS Routes
    path('cms/login/', cms_views.cms_login, name='cms_login'),
    path('cms/logout/', cms_views.cms_logout, name='cms_logout'),
    path('cms/', cms_views.dashboard, name='cms_dashboard'),

    # CRUD Jabatan
    path('cms/jabatan/', cms_views.list_jabatan, name='cms_list_jabatan'),
    path('cms/jabatan/add/', cms_views.add_jabatan, name='cms_add_jabatan'),
    path('cms/jabatan/<int:pk>/edit/', cms_views.edit_jabatan, name='cms_edit_jabatan'),
    path('cms/jabatan/<int:pk>/delete/', cms_views.delete_jabatan, name='cms_delete_jabatan'),

    # CRUD Pengurus
    path('cms/pengurus/', cms_views.list_pengurus, name='cms_list_pengurus'),
    path('cms/pengurus/add/', cms_views.add_pengurus, name='cms_add_pengurus'),
    path('cms/pengurus/<int:pk>/edit/', cms_views.edit_pengurus, name='cms_edit_pengurus'),
    path('cms/pengurus/<int:pk>/delete/', cms_views.delete_pengurus, name='cms_delete_pengurus'),

    # CRUD Kegiatan
    path('cms/kegiatan/', cms_views.manage_kegiatan, name='cms_manage_kegiatan'),
    path('cms/kegiatan/add/', cms_views.add_kegiatan, name='cms_add_kegiatan'),
    path('cms/kegiatan/<int:pk>/edit/', cms_views.edit_kegiatan, name='cms_edit_kegiatan'),
    path('cms/kegiatan/<int:pk>/delete/', cms_views.delete_kegiatan, name='cms_delete_kegiatan'),
    path('cms/kegiatan/<int:pk>/peserta/', cms_views.kegiatan_peserta, name='cms_kegiatan_peserta'),
    path('cms/kegiatan/<int:pk>/export/', cms_views.export_peserta, name='cms_export_peserta'),
    path('cms/kegiatan/<int:pk>/export-excel/', cms_views.export_peserta_excel, name='cms_export_peserta_excel'),

    # CRUD Berita
    path('cms/berita/', cms_views.list_berita, name='cms_list_berita'),
    path('cms/berita/add/', cms_views.add_berita, name='cms_add_berita'),
    path('cms/berita/<int:pk>/edit/', cms_views.edit_berita, name='cms_edit_berita'),
    path('cms/berita/<int:pk>/delete/', cms_views.delete_berita, name='cms_delete_berita'),

    # CRUD Dokumentasi
    path('cms/dokumentasi/', cms_views.list_dokumentasi, name='cms_list_dokumentasi'),
    path('cms/dokumentasi/add/', cms_views.add_dokumentasi, name='cms_add_dokumentasi'),
    path('cms/dokumentasi/<int:pk>/edit/', cms_views.edit_dokumentasi, name='cms_edit_dokumentasi'),
    path('cms/dokumentasi/<int:pk>/delete/', cms_views.delete_dokumentasi, name='cms_delete_dokumentasi'),

    # Pesan Kontak
    path('cms/pesan/', cms_views.list_pesan, name='cms_list_pesan'),
    path('cms/pesan/<int:pk>/delete/', cms_views.delete_pesan, name='cms_delete_pesan'),

    # Daftar Absensi
    path('cms/absensi/', cms_views.list_absensi, name='cms_list_absensi'),
    path('cms/absensi/export/', cms_views.export_absensi, name='cms_export_absensi'),
    path('cms/absensi/export-excel/', cms_views.export_absensi_excel, name='cms_export_absensi_excel'),
    path('cms/absensi/<int:pk>/delete/', cms_views.delete_absensi, name='cms_delete_absensi'),

    # Absensi Route (Public)
    path('absensi/kegiatan/<int:pk>/', cms_views.scan_absensi, name='scan_absensi'),
]
