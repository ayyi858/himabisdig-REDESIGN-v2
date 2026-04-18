from rest_framework import serializers
from .models import Berita, Kegiatan, Divisi, Pengurus, Galeri, Dokumen, Saran

class BeritaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Berita
        fields = '__all__'

class KegiatanSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kegiatan
        fields = '__all__'

class PengurusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pengurus
        fields = '__all__'

class DivisiSerializer(serializers.ModelSerializer):
    members = PengurusSerializer(many=True, read_only=True)
    class Meta:
        model = Divisi
        fields = '__all__'

class GaleriSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galeri
        fields = '__all__'

class DokumenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dokumen
        fields = '__all__'

class SaranSerializer(serializers.ModelSerializer):
    class Meta:
        model = Saran
        fields = '__all__'
