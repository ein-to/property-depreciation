from django.shortcuts import render
import pyodbc
from .models import scores
from weasyprint import HTML
from django.template.loader import get_template
from django.http import HttpResponse


# Create your views here.
def index(request):
    #client = client.objects.all()
    return render(request, "scoring/index.html")

def search(request):
    if 'q' in request.GET and request.GET['q']:
        q = request.GET['q']
        fam = q+"%"

        conn = pyodbc.connect('Driver={SQL Server};'
                          'Server=DESKTOP-H5S2LOO\SQLEXPRESS;'
                          'Database=ChgScore;'
                          'Trusted_Connection=yes;')

        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM ChgScore.dbo.customers WHERE Surname LIKE ?;''', fam)
        return render(request, 'scoring/search_results.html', {'cursor': cursor, 'query': fam})
    else:
        return HttpResponse('Please submit a search term.')

def result(request, cl_id):
    try:
        eq = 0
        c1 = scores.objects.all()
        for c2 in c1:
            if c2.id_client == cl_id:
                eq = 1
        id = float(cl_id)
        k=0
        for cl1 in connect_db_id(request, id=id):
            if cl1.Sex == 1: p = 7
            else: p = 9
            if cl1.IsResident == 0: v = 5
            #elif cl1.vozrast < 25: v = 7
            else: v = 9
            k = (p+v)/2
            surname = cl1.Surname
            name = cl1.CustomerName
            otch = cl1.Otchestvo
             #scores.objects.get(id_client=cl_id):
        if eq == 1:
            c3 = scores.objects.get(id_client=cl_id)
            c3.score = k
            c3.save(update_fields=["score"])
        else:
            c3 = scores(id_client=cl_id, score=k)
            c3.save()
    #except cursor.DoesNotExist:
    except Exception:
        raise Http404
    #return render(request, 'scoring/scoring_result.html', {'cursor': cursor, 'k': k})
    return render(request, 'scoring/scoring_result.html',
     {'surname': surname, 'name':name, 'otchestvo': otch, 'k': k, 'cl_id':cl_id})

def report_pdf(request, cl_id):
    id = cl_id
    r = scores.objects.get(id_client=id)
    k = r.score
    for cli in connect_db_id(request, id=id):
        fam = cli.Surname
        name = cli.CustomerName
        otch = cli.Otchestvo
    html_template = get_template('scoring/report.html').render({'fam': fam, 'name': name, 'otch': otch, 'k': k})
    pdf_file = HTML(string=html_template).write_pdf()
    response = HttpResponse(pdf_file, content_type='application/pdf')
    response['Content-Disposition'] = 'filename="home_page.pdf"'
    return response

def connect_db_id(request, id):
    conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=DESKTOP-H5S2LOO\SQLEXPRESS;'
                      'Database=ChgScore;'
                      'Trusted_Connection=yes;')

    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM ChgScore.dbo.customers WHERE CustomerID=?;''', id)
    return cursor
