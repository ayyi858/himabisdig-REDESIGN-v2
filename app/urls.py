from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'berita', views.BeritaViewSet)
router.register(r'kegiatan', views.KegiatanViewSet)
router.register(r'divisi', views.DivisiViewSet)
router.register(r'pengurus', views.PengurusViewSet)
router.register(r'galeri', views.GaleriViewSet)
router.register(r'dokumen', views.DokumenViewSet)
router.register(r'saran', views.SaranViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
