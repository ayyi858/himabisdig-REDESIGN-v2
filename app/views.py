from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Pengurus, Kegiatan, Peserta, Berita, Dokumentasi, PesanKontak, EKOSISTEM_CHOICES

def home(request):
    pengurus_count = Pengurus.objects.count()
    kegiatan_count = Kegiatan.objects.count()
    peserta_count = Peserta.objects.count()
    
    # Previews
    latest_kegiatan = Kegiatan.objects.order_by('-tanggal')[:3]
    latest_berita = Berita.objects.order_by('-tanggal')[:3]
    
    context = {
        'pengurus_count': pengurus_count,
        'kegiatan_count': kegiatan_count,
        'peserta_count': peserta_count,
        'latest_kegiatan': latest_kegiatan,
        'latest_berita': latest_berita,
    }
    return render(request, 'public/home.html', context)

def tentang_kami(request):
    pengurus = Pengurus.objects.all().order_by('id')
    return render(request, 'public/tentang_kami.html', {'pengurus': pengurus})

def ekosistem_detail(request, ekosistem_slug):
    ekosistem_dict = dict(EKOSISTEM_CHOICES)
    if ekosistem_slug not in ekosistem_dict:
        return redirect('home')
        
    nama_ekosistem = ekosistem_dict[ekosistem_slug]
    kegiatan_terkait = Kegiatan.objects.filter(ekosistem=ekosistem_slug).order_by('-tanggal')
    berita_terkait = Berita.objects.filter(ekosistem=ekosistem_slug).order_by('-tanggal')
    dokumentasi_terkait = Dokumentasi.objects.filter(ekosistem=ekosistem_slug)
    
    context = {
        'ekosistem_slug': ekosistem_slug,
        'nama_ekosistem': nama_ekosistem,
        'kegiatan_terkait': kegiatan_terkait,
        'berita_terkait': berita_terkait,
        'dokumentasi_terkait': dokumentasi_terkait,
    }
    return render(request, 'public/ekosistem.html', context)

def berita_list(request):
    berita = Berita.objects.all().order_by('-tanggal')
    return render(request, 'public/berita_list.html', {'berita': berita})

def berita_detail(request, slug):
    b = get_object_or_404(Berita, slug=slug)
    return render(request, 'public/berita_detail.html', {'berita': b})

def kegiatan_list(request):
    kegiatan = Kegiatan.objects.all().order_by('-tanggal')
    return render(request, 'public/kegiatan_list.html', {'kegiatan': kegiatan})

def kegiatan_detail(request, pk):
    k = get_object_or_404(Kegiatan, pk=pk)
    
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        no_wa = request.POST.get('no_wa')
        status_p = request.POST.get('status_pendaftar')
        link_wa = request.POST.get('link_wa', '')
        
        # Check Mode Seleksi
        if k.mode_seleksi == 'auto':
            status_kelolosan = 'approved'
        else:
            status_kelolosan = 'pending'
            
        peserta = Peserta.objects.create(
            kegiatan=k,
            nama=nama,
            email=email,
            no_wa=no_wa,
            status_pendaftar=status_p,
            link_wa=link_wa,
            status_kelolosan=status_kelolosan
        )
        
        # Auto Email Logic
        if status_kelolosan == 'approved':
            subject = f"Pendaftaran Berhasil: {k.judul}"
            message = f"Halo {nama},\n\nSelamat, pendaftaran Anda untuk kegiatan '{k.judul}' telah DITERIMA!\n\n"
            message += f"Berikut adalah detail tugas/brief:\n{k.brief_deskripsi}\n\n"
            message += f"Instruksi Tambahan:\n{k.brief_instruksi}\n\n"
            if k.brief_deadline:
                message += f"Deadline: {k.brief_deadline.strftime('%d %B %Y %H:%M')}\n\n"
            if k.brief_link_wa:
                message += f"Silakan bergabung ke grup WA berikut: {k.brief_link_wa}\n\n"
            message += "Terima kasih,\nHIMABISDIG UNM"
            
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
            messages.success(request, 'Pendaftaran berhasil dan Anda telah otomatis diterima. Silakan cek email Anda untuk detail briefing (Jika email tidak masuk, periksa tab spam).')
        else:
            messages.success(request, 'Pendaftaran berhasil. Silakan tunggu informasi kelolosan selanjutnya melalui email Anda.')
            
        return redirect('kegiatan_detail', pk=pk)

    return render(request, 'public/kegiatan_detail.html', {'kegiatan': k})

def dokumentasi(request):
    kegiatan_id = request.GET.get('kegiatan')
    terkait_kegiatan = Kegiatan.objects.filter(dokumentasi__isnull=False).distinct()
    
    if kegiatan_id:
        dok = Dokumentasi.objects.filter(kegiatan_id=kegiatan_id)
    else:
        dok = Dokumentasi.objects.all().order_by('-id')
        
    return render(request, 'public/dokumentasi.html', {
        'dokumentasi': dok,
        'terkait_kegiatan': terkait_kegiatan,
        'selected_kegiatan': kegiatan_id
    })

def kontak(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        email = request.POST.get('email')
        pesan = request.POST.get('pesan')
        PesanKontak.objects.create(nama=nama, email=email, pesan=pesan)
        messages.success(request, 'Pesan Anda telah berhasil dikirim!')
        return redirect('kontak')
    return render(request, 'public/kontak.html')
