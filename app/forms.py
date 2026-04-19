from django import forms
from .models import Jabatan, Pengurus, Kegiatan, Berita, Dokumentasi

class JabatanForm(forms.ModelForm):
    class Meta:
        model = Jabatan
        fields = ['nama']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
        }

class PengurusForm(forms.ModelForm):
    class Meta:
        model = Pengurus
        fields = ['nama', 'jabatan', 'periode', 'foto']
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'jabatan': forms.Select(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'periode': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300', 'placeholder': 'Contoh: 2024/2025'}),
            'foto': forms.FileInput(attrs={'class': 'block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100'}),
        }

class KegiatanForm(forms.ModelForm):
    class Meta:
        model = Kegiatan
        fields = ['judul', 'ekosistem', 'deskripsi', 'tanggal', 'lokasi', 'poster', 'mode_seleksi', 'brief_deskripsi', 'brief_link_wa', 'brief_deadline', 'brief_instruksi']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'ekosistem': forms.Select(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'deskripsi': forms.Textarea(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300', 'rows': 4}),
            'tanggal': forms.DateTimeInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'lokasi': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'poster': forms.FileInput(attrs={'class': 'block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100'}),
            'mode_seleksi': forms.Select(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'brief_deskripsi': forms.Textarea(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300', 'rows': 3}),
            'brief_link_wa': forms.URLInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'brief_deadline': forms.DateTimeInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300', 'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'brief_instruksi': forms.Textarea(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300', 'rows': 3}),
        }

class BeritaForm(forms.ModelForm):
    class Meta:
        model = Berita
        fields = ['judul', 'gambar', 'ekosistem', 'konten']
        widgets = {
            'judul': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'gambar': forms.FileInput(attrs={'class': 'block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100'}),
            'ekosistem': forms.Select(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'konten': forms.Textarea(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300', 'rows': 10}),
        }

class DokumentasiForm(forms.ModelForm):
    class Meta:
        model = Dokumentasi
        fields = ['kegiatan', 'ekosistem', 'foto', 'deskripsi']
        widgets = {
            'kegiatan': forms.Select(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'ekosistem': forms.Select(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
            'foto': forms.FileInput(attrs={'class': 'block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-semibold file:bg-primary-50 file:text-primary-700 hover:file:bg-primary-100'}),
            'deskripsi': forms.TextInput(attrs={'class': 'block w-full px-4 py-2 border rounded-lg focus:ring-primary-500 focus:border-primary-500 border-gray-300'}),
        }
