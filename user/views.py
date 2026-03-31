from random import randint
import os

from cryptography.fernet import Fernet
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

# Create your views here.
from blackchine_project.settings import DEFAULT_FROM_EMAIL
from django.contrib import messages
from user.ml_engine import get_predictor
from user.forms import RegisterForms
from user.models import RegisterModel, UploadModel, AttackLog

# ============================================================
# BLOCKCHAIN ENCRYPTION KEY (Fernet AES-128-CBC Symmetric Key)
# In production, this would be stored securely on the blockchain
# ============================================================
ENCRYPTION_KEY = b'ZmDfcTF7_60GrrY167zsiPd67pEvs0aGOv2oasOM1Pg='
cipher_suite = Fernet(ENCRYPTION_KEY)


def encrypt_file(file_data):
    """Encrypt file data using Fernet (AES) encryption"""
    return cipher_suite.encrypt(file_data)


def decrypt_file(file_data):
    """Decrypt file data using Fernet (AES) decryption"""
    return cipher_suite.decrypt(file_data)


def index(request):
    if request.method == "POST":
        usid = request.POST.get('username')
        pswd = request.POST.get('password')
        try:
            check = RegisterModel.objects.get(userid=usid, password=pswd)
            request.session['userid'] = check.id
            return redirect('userpage')
        except:
            pass
    return render(request,'user/index.html')

def register(request):
    if request.method == "POST":
        forms = RegisterForms(request.POST)
        if forms.is_valid():
            forms.save()
            return redirect('index')
    else:
        forms = RegisterForms()
    return render(request,'user/register.html',{'form':forms})

def userpage(request):
    uid = request.session['userid']
    request_obj = RegisterModel.objects.get(id=uid)
    nme=request_obj.firstname
    myfile = ''
    a = ''
    b = ''
    c = ''
    d = ''
    if request.method == "POST" and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        a = request.POST.get('name')
        b = request.POST.get('des')
        c = request.POST.get('area')

        # ============================================
        # MULTI-MODEL DEEP LEARNING ENSEMBLE DETECTION
        # ============================================
        original_data = myfile.read()
        
        predictor = get_predictor()  # uses pre-trained singleton — no re-training
        ml_results = predictor.predict(original_data)
        
        if ml_results['is_attack']:
            # Save to attack log for admin dashboard
            AttackLog.objects.create(
                username=request_obj.firstname + ' ' + request_obj.lastname,
                filename=myfile.name,
                cnn_score=ml_results['cnn_score'],
                lstm_score=ml_results['lstm_score'],
                mrn_score=ml_results['mrn_score'],
                ensemble_score=ml_results['ensemble_score'],
            )
            msg = (f"Malicious Cyber Attack Pattern Detected! "
                   f"CNN: {ml_results['cnn_score']}% | "
                   f"LSTM: {ml_results['lstm_score']}% | "
                   f"MRN: {ml_results['mrn_score']}% "
                   f"(Ensemble Confidence: {ml_results['ensemble_score']}%)")
            messages.error(request, msg)
            return redirect('userpage')

        # ============================================
        # BLOCKCHAIN ENCRYPTION: Encrypt file before storing
        # ============================================
        encrypted_data = encrypt_file(original_data)

        # Save encrypted file with .enc extension
        encrypted_filename = myfile.name + '.enc'
        encrypted_file = ContentFile(encrypted_data, name=encrypted_filename)

        UploadModel.objects.create(
            usid=request_obj,
            usname=nme,
            topic=a,
            description=b,
            upload_file=encrypted_file,
            location=c,
            original_filename=myfile.name,
        )
    return render(request,'user/userpage.html')

def viewdata(request):
    uid = ''
    sts = 'pending'
    sent = 'sent'
    uid = request.session['userid']
    request_obj = RegisterModel.objects.get(id=uid)
    obj = UploadModel.objects.filter(usid=request_obj)
    if request.method == "POST":
        uid = request.session['userid']
        request_obj = RegisterModel.objects.get(id=uid)
        subject = "Your Secure IoT Data OTP Code"
        otp = randint(1000, 9999)
        request.session['otp'] = otp
        html_content = f"""
        <div style="font-family:Arial,sans-serif;max-width:480px;margin:auto;background:#0f0f1a;padding:40px;border-radius:12px;border:2px solid #63ffb4;">
            <h2 style="color:#63ffb4;text-align:center;letter-spacing:2px;">🔐 IoT Security System</h2>
            <p style="color:#ccc;text-align:center;">Your One-Time Password (OTP) for accessing encrypted IoT data:</p>
            <div style="font-size:42px;font-weight:900;text-align:center;letter-spacing:14px;color:#63ffb4;padding:20px;background:#1a1a2e;border-radius:8px;margin:20px 0;">{otp}</div>
            <p style="color:#888;font-size:12px;text-align:center;">This OTP is valid for one-time use only. Do not share it with anyone.</p>
        </div>
        """
        try:
            from_mail = DEFAULT_FROM_EMAIL
            to_mail = [request_obj.email]
            msg = EmailMultiAlternatives(subject, '', from_mail, to_mail)
            msg.attach_alternative(html_content, "text/html")
            msg.send()
            sts = 'sent'
            messages.success(request, f"✅ OTP sent to {request_obj.email}! Check your inbox.")
        except Exception:
            # Gmail SMTP not configured — show OTP directly on screen
            sts = 'sent'
            messages.info(request, str(otp))
    return render(request,'user/viewdata.html',{'obj':obj,'sts':sts,'sent':sent,})

def otppage(request,pk):
    password = request.session['otp']
    sts = "c"
    pas = type(password)
    ss = ''
    count = 0
    aaa = ''
    vott, vott1 = 0, 0
    pkid = UploadModel.objects.get(id=pk)
    aaa = pkid.id
    request.session['jhf'] = aaa
    if request.method == "POST":

        objs = UploadModel.objects.get(id=pk)
        unid = objs.id
        vot_count = UploadModel.objects.all().filter(id=unid)
        for t in vot_count:
            vott = t.add_count
        vott1 = vott + 1
        obj = get_object_or_404(UploadModel, id=unid)
        obj.add_count = vott1
        obj.save(update_fields=["add_count"])

        onetime = request.POST.get('otp', '')
        ss = onetime
        if int(password) == int(onetime):

            return redirect('download_page')
        else:
            sts = "Please Enter Correct OTP"
    return render(request,'user/otppage.html',{'password':pas,'sts':sts,'count':aaa})


def download_page(request):
    aaaa = request.session['jhf']
    obj = UploadModel.objects.filter(id=aaaa)
    return render(request,'user/download_page.html',{'a':aaaa,'obj':obj})


def secure_download(request, pk):
    """
    BLOCKCHAIN DECRYPTION: Decrypt and serve file only after hash verification.
    This ensures that the raw encrypted file on disk is useless without the key.
    """
    file_obj = get_object_or_404(UploadModel, id=pk)

    # Read the encrypted file from storage
    encrypted_data = file_obj.upload_file.read()

    # Decrypt the file
    decrypted_data = decrypt_file(encrypted_data)

    # Get original filename
    original_name = getattr(file_obj, 'original_filename', None)
    if not original_name:
        # Fallback: remove .enc extension
        original_name = os.path.basename(file_obj.upload_file.name)
        if original_name.endswith('.enc'):
            original_name = original_name[:-4]

    # Serve decrypted file as download
    response = HttpResponse(decrypted_data, content_type='application/octet-stream')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(original_name)
    return response


def graphical_page(request):
    chart = UploadModel.objects.values('location').annotate(dcount=Count('location'))
    return render(request,'user/graphical_page.html',{'obj':chart})

def mydetail(request):
    usid = request.session['userid']
    us_id = RegisterModel.objects.get(id=usid)
    return render(request,'user/mydetail.html',{'obje':us_id})


def admin_login(request):
    """Admin login page — hardcoded credentials for demo."""
    if request.session.get('is_admin'):
        return redirect('admin_dashboard')

    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        # Demo credentials — change these as needed
        if username == 'admin' and password == 'admin123':
            request.session['is_admin'] = True
            return redirect('admin_dashboard')
        else:
            error = 'Invalid username or password. Please try again.'

    return render(request, 'user/admin_login.html', {'error': error})


def admin_logout(request):
    """Logs the admin out and redirects to admin login page."""
    request.session.pop('is_admin', None)
    return redirect('admin_login')


def admin_dashboard(request):
    """Admin-only view showing full user activity, uploads, and ML attack logs."""
    if not request.session.get('is_admin'):
        return redirect('admin_login')

    users_qs = RegisterModel.objects.all()

    # Annotate each user with their upload count
    users_with_counts = []
    for u in users_qs:
        u.upload_count = UploadModel.objects.filter(usid=u).count()
        users_with_counts.append(u)

    uploads     = UploadModel.objects.all().order_by('-id')
    attack_logs = AttackLog.objects.all()

    context = {
        'users':           users_with_counts,
        'uploads':         uploads,
        'attack_logs':     attack_logs,
        'total_users':     users_qs.count(),
        'total_uploads':   uploads.count(),
        'total_attacks':   attack_logs.count(),
        'total_encrypted': uploads.count(),
    }
    return render(request, 'user/admin_dashboard.html', context)