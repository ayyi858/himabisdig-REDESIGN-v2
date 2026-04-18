from rest_framework import viewsets, permissions
from .models import Berita, Kegiatan, Divisi, Pengurus, Galeri, Dokumen, Saran
from .serializers import (
    BeritaSerializer, KegiatanSerializer, DivisiSerializer,
    PengurusSerializer, GaleriSerializer, DokumenSerializer, SaranSerializer
)

class BeritaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Berita.objects.all().order_by('-date_published')
    serializer_class = BeritaSerializer

class KegiatanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Kegiatan.objects.all().order_by('-date')
    serializer_class = KegiatanSerializer

class DivisiViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Divisi.objects.prefetch_related('members').all()
    serializer_class = DivisiSerializer

class PengurusViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Pengurus.objects.all()
    serializer_class = PengurusSerializer

class GaleriViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Galeri.objects.all().order_by('-date_added')
    serializer_class = GaleriSerializer

class DokumenViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Dokumen.objects.all().order_by('-date_uploaded')
    serializer_class = DokumenSerializer

class SaranViewSet(viewsets.ModelViewSet):
    queryset = Saran.objects.all()
    serializer_class = SaranSerializer
    permission_classes = [permissions.AllowAny]
