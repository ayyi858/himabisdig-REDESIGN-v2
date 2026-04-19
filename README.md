# 🦁 HIMABISDIG UNM CMS v2.0
> **Sistem Manajemen Organisasi & Presensi Digital Terintegrasi**

HIMABISDIG UNM CMS adalah platform manajemen internal organisasi mahasiswa yang dibangun untuk memodernisasi alur kerja administrasi, mulai dari manajemen pengurus hingga sistem presensi digital berbasis QR Code dengan tanda tangan elektronik.

---

## ✨ Fitur Unggulan

- 💻 **Custom CMS Dashboard**: Panel administrasi mandiri yang premium dan responsif (tanpa bergantung pada Django Admin default).
- ✍️ **Digital Signature (Paraf)**: Sistem presensi yang mewajibkan peserta membubuhkan tanda tangan digital langsung di layar perangkat.
- 📊 **Advanced Export**: Unduh data absensi dan peserta dalam format **Excel (.xlsx)** lengkap dengan gambar tanda tangan di dalam sel, serta format **CSV**.
- 🎫 **QR Code Attendance**: Pembuatan QR Code otomatis untuk setiap kegiatan guna mempermudah absensi.
- 📂 **Standalone CRUD**: Manajemen penuh untuk data *Jabatan*, *Pengurus*, *Kegiatan*, *Berita*, *Dokumentasi*, dan *Pesan Masuk*.
- 🔒 **Role-Based Security**: Restriksi akses admin yang ketat untuk memastikan data hanya dikelola oleh staf yang berwenang.

---

## 🛠️ Tech Stack

Sistem ini dibangun menggunakan teknologi modern untuk performa dan skalabilitas:

- **Core Framework**: [Django 6.0.4](https://www.djangoproject.com/) (Python)
- **Database**: MySQL / MariaDB
- **Frontend**: HTML5, Vanilla JavaScript, [Tailwind CSS](https://tailwindcss.com/) (Via CDN)
- **Library Utama**:
  - `openpyxl`: Pembuatan laporan Excel dengan inklusi gambar.
  - `pillow`: Pemrosesan gambar dan foto pengurus/dokumentasi.
  - `qrcode`: Generator kode QR dinamis.
  - `mysqlclient`: Konektor database MySQL berperforma tinggi.

---

## 🚀 Panduan Instalasi (Development)

Pastikan Anda telah menginstal **Python 3.10+** dan **MySQL** di perangkat Anda.

### 1. Clone Repository
```bash
git clone https://github.com/ayyi858/himabisdig-REDESIGN-v2.git
cd himabisdig-REDESIGN-v2
```

### 2. Setup Virtual Environment
```bash
# Windows
python -m venv env
.\env\Scripts\activate

# Linux/Mac
python3 -m venv env
source env/bin/activate
```

### 3. Instal Dependensi
```bash
pip install -r requirements.txt
```
*(Atau instal manual: `django`, `mysqlclient`, `pillow`, `qrcode`, `openpyxl`)*

### 4. Konfigurasi Database
Sesuaikan pengaturan database di `core/settings.py` pada bagian `DATABASES`.

### 5. Migrasi & Run
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---

## 📁 Struktur Folder Utama
```text
HIMASBISDIG V2/
├── app/                # Logika aplikasi Utama (Models, Views, Forms)
├── core/               # Konfigurasi project Django
├── media/              # Folder penyimpanan upload (Foto/Poster/Paraf)
├── static/             # Aset statis (CSS/JS/Images)
├── templates/          # Template HTML (Public & CMS)
└── manage.py           # Django entry point
```

---

## 📝 Catatan Keamanan
- File `.env` atau kredensial database tidak boleh di-commit ke repository publik.
- Akses `/admin/` hanya diberikan kepada **Superuser** untuk manajemen tingkat tinggi.

---

**Made with ❤️ by HIMABISDIG UNM Team**
