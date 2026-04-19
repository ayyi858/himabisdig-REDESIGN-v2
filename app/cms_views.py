from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import *
from .forms import *
import qrcode
from io import BytesIO
import base64

def is_cms_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

def cms_login(request):
    if request.user.is_authenticated:
        return redirect('cms_dashboard')
    if request.method == 'POST':
        u = request.POST.get('username')
        p = request.POST.get('password')
        user = authenticate(request, username=u, password=p)
        if user is not None:
            login(request, user)
            return redirect('cms_dashboard')
        else:
            messages.error(request, 'Username atau Password salah.')
    return render(request, 'cms/login.html')

def cms_logout(request):
    logout(request)
    return redirect('cms_login')

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def dashboard(request):
    context = {
        'total_pengurus': Pengurus.objects.count(),
        'total_kegiatan': Kegiatan.objects.count(),
        'total_peserta': Peserta.objects.count(),
        'total_absensi': Absensi.objects.count(),
        'total_pesan': PesanKontak.objects.count(),
        'recent_peserta': Peserta.objects.order_by('-created_at')[:5]
    }
    return render(request, 'cms/dashboard.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def manage_kegiatan(request):
    kegiatan = Kegiatan.objects.all().order_by('-tanggal')
    return render(request, 'cms/manage_kegiatan.html', {'kegiatan': kegiatan})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def kegiatan_peserta(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    peserta = Peserta.objects.filter(kegiatan=kegiatan).order_by('-created_at')
    
    if request.method == 'POST':
        peserta_id = request.POST.get('peserta_id')
        action = request.POST.get('action')
        p = get_object_or_404(Peserta, pk=peserta_id)
        
        if action == 'approve':
            p.status_kelolosan = 'approved'
            p.save()
            subject = f"Pendaftaran Berhasil: {kegiatan.judul}"
            message = f"Halo {p.nama},\n\nSelamat, pendaftaran Anda untuk kegiatan '{kegiatan.judul}' telah DITERIMA!\n\n"
            message += f"Berikut adalah detail tugas/brief:\n{kegiatan.brief_deskripsi}\n\n"
            message += f"Instruksi Tambahan:\n{kegiatan.brief_instruksi}\n\n"
            if kegiatan.brief_deadline:
                message += f"Deadline: {kegiatan.brief_deadline.strftime('%d %B %Y %H:%M')}\n\n"
            if kegiatan.brief_link_wa:
                message += f"Silakan bergabung ke grup WA berikut: {kegiatan.brief_link_wa}\n\n"
            message += "Terima kasih,\nHIMABISDIG UNM"
            
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [p.email], fail_silently=True)
            messages.success(request, f'Berhasil menyetujui {p.nama} dan mengirim email.')
            
        elif action == 'reject':
            p.status_kelolosan = 'rejected'
            p.save()
            subject = f"Pembaruan Status Pendaftaran: {kegiatan.judul}"
            message = f"Halo {p.nama},\n\nMohon maaf, pendaftaran Anda untuk kegiatan '{kegiatan.judul}' belum dapat kami terima saat ini.\n\nTerima kasih atas partisipasinya,\nHIMABISDIG UNM"
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [p.email], fail_silently=True)
            messages.warning(request, f'Menenolak {p.nama} dan mengirim email penolakan.')
            
        return redirect('cms_kegiatan_peserta', pk=pk)

    # Generate QR Code image base64
    qr_url = request.build_absolute_uri(f'/absensi/kegiatan/{kegiatan.pk}/')
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(qr_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'kegiatan': kegiatan,
        'peserta': peserta,
        'qr_base64': qr_base64,
        'qr_url': qr_url
    }
    return render(request, 'cms/kegiatan_peserta.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def export_peserta(request, pk):
    import csv
    from django.http import HttpResponse
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="peserta_{kegiatan.id}.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nama', 'Email', 'No WA', 'Status Pendaftar', 'Link WA', 'Status Kelolosan'])
    
    for p in Peserta.objects.filter(kegiatan=kegiatan):
        writer.writerow([p.nama, p.email, p.no_wa, p.get_status_pendaftar_display(), p.link_wa, p.get_status_kelolosan_display()])
        
    return response

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def export_peserta_excel(request, pk):
    from openpyxl import Workbook
    from django.http import HttpResponse
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Daftar Peserta"
    
    # Header
    ws.append(['Nama', 'Email', 'No WA', 'Status Pendaftar', 'Link WA', 'Status Kelolosan'])
    
    for p in Peserta.objects.filter(kegiatan=kegiatan):
        ws.append([p.nama, p.email, p.no_wa, p.get_status_pendaftar_display(), p.link_wa, p.get_status_kelolosan_display()])
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="peserta_{kegiatan.id}.xlsx"'
    wb.save(response)
    return response

def scan_absensi(request, pk):
    kegiatan = get_object_or_404(Kegiatan, pk=pk)
    if request.method == 'POST':
        nama = request.POST.get('nama')
        status_k = request.POST.get('status_kehadiran')
        ttd = request.POST.get('tanda_tangan')
        Absensi.objects.create(kegiatan=kegiatan, nama=nama, status_kehadiran=status_k, tanda_tangan=ttd)
        messages.success(request, 'Absensi berhasil tersimpan.')
        return redirect('scan_absensi', pk=pk)
        
    return render(request, 'public/form_absensi.html', {'kegiatan': kegiatan})

# ==========================================
# DAFTAR ABSENSI (CMS)
# ==========================================
@user_passes_test(is_cms_admin, login_url='/cms/login/')
def list_absensi(request):
    absensi = Absensi.objects.all().order_by('-waktu')
    context = {
        'items': absensi,
        'model_name': 'Absensi',
        'columns': ['Informasi Kehadiran', 'Waktu', 'Paraf/TTD'],
        'add_url': None,
        'export_url': '/cms/absensi/export/',
        'export_excel_url': '/cms/absensi/export-excel/'
    }
    return render(request, 'cms/absensi/list.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def delete_absensi(request, pk):
    obj = get_object_or_404(Absensi, pk=pk)
    obj.delete()
    messages.warning(request, 'Data absensi dihapus.')
    return redirect('cms_list_absensi')

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def export_absensi(request):
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="daftar_absensi.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Nama', 'Kegiatan', 'Status Kehadiran', 'Waktu'])
    
    for a in Absensi.objects.all().order_by('-waktu'):
        writer.writerow([a.nama, a.kegiatan.judul, a.get_status_kehadiran_display(), a.waktu.strftime('%d-%m-%Y %H:%M')])
        
    return response

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def export_absensi_excel(request):
    from openpyxl import Workbook
    from openpyxl.drawing.image import Image as OpenPyxlImage
    from django.http import HttpResponse
    import base64
    from io import BytesIO
    from PIL import Image as PILImage
    
    wb = Workbook()
    ws = wb.active
    ws.title = "Data Absensi"
    
    # Header
    ws.append(['Nama', 'Kegiatan', 'Status Kehadiran', 'Waktu', 'Tanda Tangan'])
    
    # Set column width for signature
    ws.column_dimensions['E'].width = 25
    
    for i, a in enumerate(Absensi.objects.all().order_by('-waktu'), start=2):
        ws.append([a.nama, a.kegiatan.judul, a.get_status_kehadiran_display(), a.waktu.strftime('%d-%m-%Y %H:%M')])
        
        # Add signature image if exists
        if a.tanda_tangan and a.tanda_tangan.startswith('data:image'):
            try:
                # Decode base64
                format, imgstr = a.tanda_tangan.split(';base64,')
                img_data = base64.b64decode(imgstr)
                
                # Create image object and resize
                img = PILImage.open(BytesIO(img_data))
                img.thumbnail((150, 150)) # Resize for Excel cell
                
                # Save to buffer for openpyxl
                temp_buffer = BytesIO()
                img.save(temp_buffer, format='PNG')
                temp_buffer.seek(0)
                
                xl_img = OpenPyxlImage(temp_buffer)
                
                # Calculate placement
                ws.add_image(xl_img, f'E{i}')
                
                # Set row height
                ws.row_dimensions[i].height = 80
            except Exception as e:
                ws.append([f"Error loading image: {str(e)}"])
        
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="daftar_absensi.xlsx"'
    wb.save(response)
    return response

# ==========================================
# CRUD JABATAN
# ==========================================
@user_passes_test(is_cms_admin, login_url='/cms/login/')
def list_jabatan(request):
    jabatan = Jabatan.objects.all().order_by('id')
    context = {
        'items': jabatan, 
        'model_name': 'Jabatan', 
        'columns': ['ID', 'Nama Jabatan'],
        'add_url': '/cms/jabatan/add/'
    }
    return render(request, 'cms/jabatan/list.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def add_jabatan(request):
    form = JabatanForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Berhasil menambah jabatan baru.')
        return redirect('cms_list_jabatan')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Tambah Jabatan', 'list_url': '/cms/jabatan/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def edit_jabatan(request, pk):
    obj = get_object_or_404(Jabatan, pk=pk)
    form = JabatanForm(request.POST or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Jabatan berhasil diperbarui.')
        return redirect('cms_list_jabatan')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Edit Jabatan', 'list_url': '/cms/jabatan/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def delete_jabatan(request, pk):
    obj = get_object_or_404(Jabatan, pk=pk)
    obj.delete()
    messages.warning(request, 'Jabatan telah dihapus.')
    return redirect('cms_list_jabatan')

# ==========================================
# CRUD PENGURUS
# ==========================================
@user_passes_test(is_cms_admin, login_url='/cms/login/')
def list_pengurus(request):
    pengurus = Pengurus.objects.all().order_by('id')
    context = {
        'items': pengurus, 
        'model_name': 'Pengurus', 
        'columns': ['Profil pengurus', 'Jabatan', 'Periode'],
        'add_url': '/cms/pengurus/add/'
    }
    return render(request, 'cms/pengurus/list.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def add_pengurus(request):
    form = PengurusForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pengurus baru berhasil ditambahkan.')
        return redirect('cms_list_pengurus')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Tambah Pengurus', 'list_url': '/cms/pengurus/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def edit_pengurus(request, pk):
    obj = get_object_or_404(Pengurus, pk=pk)
    form = PengurusForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Data pengurus diperbarui.')
        return redirect('cms_list_pengurus')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Edit Pengurus', 'list_url': '/cms/pengurus/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def delete_pengurus(request, pk):
    obj = get_object_or_404(Pengurus, pk=pk)
    obj.delete()
    messages.warning(request, 'Pengurus telah dihapus.')
    return redirect('cms_list_pengurus')

# ==========================================
# CRUD KEGIATAN
# ==========================================
@user_passes_test(is_cms_admin, login_url='/cms/login/')
def add_kegiatan(request):
    form = KegiatanForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kegiatan baru berhasil dibuat.')
        return redirect('cms_manage_kegiatan')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Tambah Kegiatan', 'list_url': '/cms/kegiatan/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def edit_kegiatan(request, pk):
    obj = get_object_or_404(Kegiatan, pk=pk)
    form = KegiatanForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Kegiatan berhasil diperbarui.')
        return redirect('cms_manage_kegiatan')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Edit Kegiatan', 'list_url': '/cms/kegiatan/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def delete_kegiatan(request, pk):
    obj = get_object_or_404(Kegiatan, pk=pk)
    obj.delete()
    messages.warning(request, 'Kegiatan telah dihapus.')
    return redirect('cms_manage_kegiatan')

# ==========================================
# CRUD BERITA
# ==========================================
@user_passes_test(is_cms_admin, login_url='/cms/login/')
def list_berita(request):
    berita = Berita.objects.all().order_by('-tanggal')
    context = {
        'items': berita, 
        'model_name': 'Berita', 
        'columns': ['Info Berita', 'Ekosistem', 'Tanggal Terbit'],
        'add_url': '/cms/berita/add/'
    }
    return render(request, 'cms/berita/list.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def add_berita(request):
    form = BeritaForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Berita baru berhasil diterbitkan.')
        return redirect('cms_list_berita')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Tambah Berita', 'list_url': '/cms/berita/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def edit_berita(request, pk):
    obj = get_object_or_404(Berita, pk=pk)
    form = BeritaForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Berita berhasil diperbarui.')
        return redirect('cms_list_berita')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Edit Berita', 'list_url': '/cms/berita/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def delete_berita(request, pk):
    obj = get_object_or_404(Berita, pk=pk)
    obj.delete()
    messages.warning(request, 'Berita telah dihapus.')
    return redirect('cms_list_berita')

# ==========================================
# CRUD DOKUMENTASI
# ==========================================
@user_passes_test(is_cms_admin, login_url='/cms/login/')
def list_dokumentasi(request):
    dok = Dokumentasi.objects.all().order_by('-id')
    context = {
        'items': dok, 
        'model_name': 'Dokumentasi', 
        'columns': ['Foto', 'Kegiatan / Ekosistem', 'Deskripsi'],
        'add_url': '/cms/dokumentasi/add/'
    }
    return render(request, 'cms/dokumentasi/list.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def add_dokumentasi(request):
    form = DokumentasiForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Dokumentasi berhasil ditambahkan.')
        return redirect('cms_list_dokumentasi')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Tambah Dokumentasi', 'list_url': '/cms/dokumentasi/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def edit_dokumentasi(request, pk):
    obj = get_object_or_404(Dokumentasi, pk=pk)
    form = DokumentasiForm(request.POST or None, request.FILES or None, instance=obj)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Dokumentasi berhasil diperbarui.')
        return redirect('cms_list_dokumentasi')
    return render(request, 'cms/generic_form.html', {'form': form, 'title': 'Edit Dokumentasi', 'list_url': '/cms/dokumentasi/'})

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def delete_dokumentasi(request, pk):
    obj = get_object_or_404(Dokumentasi, pk=pk)
    obj.delete()
    messages.warning(request, 'Dokumentasi telah dihapus.')
    return redirect('cms_list_dokumentasi')

# ==========================================
# PESAN KONTAK
# ==========================================
@user_passes_test(is_cms_admin, login_url='/cms/login/')
def list_pesan(request):
    pesan = PesanKontak.objects.all().order_by('-tanggal')
    context = {
        'items': pesan, 
        'model_name': 'Pesan Masuk', 
        'columns': ['Pengirim', 'Isi Pesan', 'Waktu Kirim'],
        'add_url': None
    }
    return render(request, 'cms/pesan/list.html', context)

@user_passes_test(is_cms_admin, login_url='/cms/login/')
def delete_pesan(request, pk):
    obj = get_object_or_404(PesanKontak, pk=pk)
    obj.delete()
    messages.warning(request, 'Pesan telah dihapus.')
    return redirect('cms_list_pesan')
