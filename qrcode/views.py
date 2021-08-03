from django.shortcuts import render
import png
import pyqrcode
from pyqrcode import QRCode
from upload_db.models import main_t
# Create your views here.

def qrcode_create(request):
    m = main_t.objects.get(inv=10000612)
    code = pyqrcode.create(m.inv)
    code.png('%s.png' % m.inv, scale=6)
    return render(request, 'qrcode/qrcode_create.html', {'code': code})
