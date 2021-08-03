from django.shortcuts import render
from upload_db.models import main_t, amort_t, change_bal_price, type_spisan, type_id, employee_id, depart, company_id, branch_id, history_item
import pandas as pd
import os
from datetime import datetime, date
import html
import xlsxwriter
from dateutil.relativedelta import relativedelta
from django.template.loader import get_template
from django.http import HttpResponse
import operator
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
from transliterate import translit
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.shortcuts import redirect
import numpy
from django.template.loader import get_template, render_to_string
from django.core.files.storage import FileSystemStorage
from weasyprint import HTML
from django.db.models import Q

@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    request.session.set_expiry(2400)
                    login(request, user)
                    return render(request, 'main_os/index.html')
                else:
                    return HttpResponse('Disabled account')
            else:
                message = 'Неверный логин или пароль'
                return render(request, 'main_os/login.html', {'form': form, 'message': message})
    else:
        form = LoginForm()
    return render(request, 'main_os/login.html', {'form': form})

def logout_request(request):
    logout(request)
    return redirect('user_login')

def index(request):
    if request.user.is_authenticated:
        return render (request, 'main_os/index.html')
    else:
        return redirect('user_login')

def test(request):
    main = main_t.objects.filter(inv__gt=20000000,inv__lt=30000000).order_by('-inv')[0]
    inv = main.inv + 1

    return render(request, 'main_os/test1.html', {'inv': inv})

def amort_template(request):
    if request.user.is_authenticated:
        now = datetime.now()
        month = now.month
        if month == 1:
            month = 'Январь'
        if month == 2:
            month = 'Февраль'
        if month == 3:
            month = 'Март'
        if month == 4:
            month = 'Апрель'
        if month == 5:
            month = 'Май'
        if month == 6:
            month = 'Июнь'
        if month == 7:
            month = 'Июль'
        if month == 8:
            month = 'Август'
        if month == 9:
            month = 'Сентябрь'
        if month == 10:
            month = 'Октябрь'
        if month == 11:
            month = 'Ноябрь'
        if month == 12:
            month = 'Декабрь'
        year = now.year
        return render(request, 'main_os/amort_template.html', {'month': month, 'year': year})
    else:
        return redirect('user_login')

def amortizacia(request):
        if request.user.is_authenticated:
            now_t = datetime.now()
            #now_t = datetime(2020,12,18)

            #main = main_t.objects.filter(id_oborud=3487)
            main = main_t.objects.filter(type_id__gt=1)
            for m in main:
                amort = amort_t()
                if m.date_spisan is None:
                    r = round(m.bal_price,1) - round(m.amort_sum,1)
                    if r!=0:
                        b_p = round(m.bal_price,2)
                        a_s = round(m.amort_sum,2)
                        a_s_m = round(m.amort_sum_month,2)
                        ostatok_sroka_new2 = (b_p - a_s) / a_s_m
                        ostatok_sroka_new = round(ostatok_sroka_new2)
                        if amort_t.objects.filter(id_oborud=m.id_oborud).exists():
                            a = amort_t.objects.filter(id_oborud=m.id_oborud).order_by('-date_amort')[0]
                            ost_sum1 = a.ost_sum
                            bal_price = m.bal_price
                            change = change_bal_price.objects.all()
                            ch = 0
                            for c in change:
                                if c.id_oborud == m.id_oborud:
                                    diff = relativedelta(now_t, c.date)
                                    if diff.years==0 and diff.months==0:
                                        if c.change_id==1:
                                            ost_sum1 = ost_sum1 + c.summ
                                            bal_price = bal_price + c.summ
                                            ch = 1
                                        if c.change_id==2:
                                            ost_sum1 = ost_sum1 - c.summ
                                            bal_price = bal_price - c.summ
                                            ch = 1
                            if ch == 1:
                                amort_sum_month1 = ost_sum1 / ostatok_sroka_new
                                ost_sum = ost_sum1 - amort_sum_month1
                                summ_amort = a.amort_sum + amort_sum_month1
                                amort.bal_price = bal_price
                                amort.amort_sum_month = amort_sum_month1
                                amort.amort_sum = summ_amort
                                amort.ost_sum = ost_sum
                                m.amort_sum_month = amort_sum_month1
                                m.amort_sum = summ_amort
                                m.bal_price = bal_price
                                m.save()
                            if ch == 0:
                                amort.amort_sum_month = m.amort_sum_month
                                amort.amort_sum = a.amort_sum + m.amort_sum_month
                                amort.ost_sum = a.ost_sum - m.amort_sum_month
                                amort.bal_price = m.bal_price
                                m.amort_sum = a.amort_sum + m.amort_sum_month
                                m.save()
                            amort.id_oborud = m.id_oborud
                            amort.date_amort = now_t
                            amort.norm_months = m.amort_month
                            amort.save()
                        else:
                            amort.amort_sum_month = m.amort_sum_month
                            amort.amort_sum = m.amort_sum_month
                            amort.ost_sum = m.bal_price - m.amort_sum_month
                            amort.id_oborud = m.id_oborud
                            amort.date_amort = now_t
                            amort.norm_months = m.amort_month
                            amort.bal_price = m.bal_price
                            m.amort_sum = m.amort_sum + m.amort_sum_month
                            m.save()
                            amort.save()

            return render(request, 'main_os/amort.html')
        else:
            return redirect('user_login')


def reports(request, id):
    if request.user.is_authenticated:
        br = branch_id.objects.all()
        spisan = type_spisan.objects.all()
        if id == 1:
            title = 'Ведомость амортизации'
        if id == 2:
            title = 'Ведомость общая'
        if id == 3:
            title = 'Ведомость списания/реализации'
        else:
            title = 'Ведомость амортизации основных средств'
        return render(request, 'main_os/reports.html', {'br': br, 'spisan': spisan, 'id': id, 'title': title})
    else:
        return redirect('user_login')

@csrf_exempt
def report(request):
    if request.user.is_authenticated:

        choice = request.POST['dropdown']
        date1 = request.POST['month']
        branch = request.POST['dropdown2']
        date = datetime.strptime(date1, "%Y-%m")
        date_year = date.year
        date_month = date.month
        date_month1 = '{:02}'.format(date_month)

        t = type_id.objects.filter(type_id=choice)
        for ty in t:
            type_name = ty.type
        if branch == '0':
            branch_name = 'Все'
        else:
            b = branch_id.objects.get(branch_id=branch)
            branch_name = b.name
        file_name = type_name+" "+str(date1)
        file_name = translit(file_name, "ru", reversed=True)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename={}.xlsx".format(file_name)
        context = {
            'in_memory': True,
            'remove_timezone': True
        }
        workbook = xlsxwriter.Workbook(response, context)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 15)
        worksheet.set_column('I:I', 15)
        style_align_center = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 11})
        style_align_center_border = workbook.add_format({'align': 'center', 'bold': True, 'border': 1, 'text_wrap': True})
        worksheet.merge_range('A1:I1', 'Ведомость амортизации '+type_name+' за '+str(date_month1)+'.'+str(date_year)+' г.'+'        '+branch_name+'', style_align_center)
        format2 = workbook.add_format({'num_format': 'dd-mm-yy', 'border': 1, 'align': 'center'})
        format1 = workbook.add_format({'border': 1, 'align': 'center'})
        format3 = workbook.add_format({'align': 'center', 'border': 1, 'text_wrap': True})
        format4 = workbook.add_format({'align': 'center', 'bold': True})
        format5 = workbook.add_format({'align': 'center'})
        #worksheet.write('A1', 'Ведомость амортизации '+type_name+' за '+str(date_month)+' '+str(date_year)+'', style_align_center)
        worksheet.write('A3', 'Дата ввода в эксплуатацию', style_align_center_border)
        worksheet.write('B3', 'Инвентарный номер', style_align_center_border)
        worksheet.write('C3', 'Наименование', style_align_center_border)
        worksheet.write('D3', 'Срок полезной службы', style_align_center_border)
        worksheet.write('E3', 'Остаток срока службы', style_align_center_border)
        worksheet.write('F3', 'Ежемесячная норма амортизации', style_align_center_border)
        worksheet.write('G3', 'Первоначальная стоимость', style_align_center_border)
        worksheet.write('H3', 'Накопленная амортизация', style_align_center_border)
        worksheet.write('I3', 'Остаточная стоимость', style_align_center_border)
        rows = 3
        col=0
        summa_amort_sum_month = 0
        summa_bal_price = 0
        summa_amort_sum = 0
        summa_ost_sum = 0
        amort = amort_t.objects.all()
        i=0
        if choice == '1':
            main = main_t.objects.filter(type_id=choice, date_vvod__lte=date)
            for m in main:
                if m.type_spisan is None:
                    if len(str(m.inv)) < 8:
                        inv = '{:08}'.format(m.inv)
                    else:
                        inv = m.inv
                    worksheet.write(rows,col,m.date_vvod, format2)
                    worksheet.write(rows,col+1,inv, format1)
                    worksheet.write(rows,col+2,m.name, format3)
                    worksheet.write(rows,col+3,'0', format1)
                    worksheet.write(rows,col+4,'0', format1)
                    worksheet.write(rows,col+5,'0', format1)
                    worksheet.write(rows,col+6,m.bal_price, format1)
                    worksheet.write(rows,col+7,round(m.amort_sum,2), format1)
                    worksheet.write(rows,col+8,'0', format1)
                    rows=rows+1
                    summa_bal_price = summa_bal_price + m.bal_price
        for a in amort:
            if a.date_amort.year == date_year and a.date_amort.month == date_month:
                #r = round(a.bal_price,1) - round(a.amort_sum,1)
                #if r!=0:
                    k = len(amort_t.objects.filter(id_oborud=a.id_oborud))
                    i=i+1
                    a_id = a.id_oborud
                    if branch == '0':
                        main = main_t.objects.filter(id_oborud=a_id, type_id=choice)
                    else:
                        main = main_t.objects.filter(id_oborud=a_id, type_id=choice, branch_id=branch)
                    for m in main:
                            ostatok_sroka_new = round((a.bal_price - a.amort_sum) / a.amort_sum_month)

                            if len(str(m.inv)) < 8:
                                inv = '{:08}'.format(m.inv)
                            else:
                                inv = m.inv

                            worksheet.write(rows,col,m.date_vvod, format2)
                            worksheet.write(rows,col+1,inv, format1)
                            worksheet.write(rows,col+2,m.name, format3)
                            worksheet.write(rows,col+3,a.norm_months, format1)
                            worksheet.write(rows,col+4,ostatok_sroka_new, format1)
                            worksheet.write(rows,col+5,round(a.amort_sum_month,2), format1)
                            worksheet.write(rows,col+6,a.bal_price, format1)
                            worksheet.write(rows,col+7,round(a.amort_sum,2), format1)
                            worksheet.write(rows,col+8,round(a.ost_sum,2), format1)
                            rows=rows+1
                            summa_amort_sum_month = summa_amort_sum_month+round(a.amort_sum_month,2)
                            summa_bal_price = summa_bal_price + a.bal_price
                            summa_amort_sum = summa_amort_sum + round(a.amort_sum,2)
                            summa_ost_sum = summa_ost_sum + round(a.ost_sum,2)

        history = amort_t.objects.filter(date_amort__lte=date)
        for h in history:
            if round(h.bal_price,1) == round(h.amort_sum,1):
                if main_t.objects.filter(id_oborud=h.id_oborud, type_id=choice).exists():
                    m1 = main_t.objects.filter(id_oborud=h.id_oborud, type_id=choice)
                    for m in m1:
                        if m.date_spisan is None:
                            if len(str(m.inv)) < 8:
                                inv = '{:08}'.format(m.inv)
                            else:
                                inv = m.inv
                            worksheet.write(rows,col,m.date_vvod, format2)
                            worksheet.write(rows,col+1,inv, format1)
                            worksheet.write(rows,col+2,m.name, format3)
                            worksheet.write(rows,col+3,m.amort_month, format1)
                            worksheet.write(rows,col+4,'0', format1)
                            worksheet.write(rows,col+5,'0', format1)
                            worksheet.write(rows,col+6,m.bal_price, format1)
                            worksheet.write(rows,col+7,round(m.amort_sum,2), format1)
                            worksheet.write(rows,col+8,'0', format1)
                            rows=rows+1
                            summa_bal_price = summa_bal_price + m.bal_price
                            summa_amort_sum = summa_amort_sum + round(m.amort_sum,2)

        worksheet.write(rows,col+2,'Всего:', format4)
        worksheet.write(rows,col+5,summa_amort_sum_month, format4)
        worksheet.write(rows,col+6,summa_bal_price, format4)
        worksheet.write(rows,col+7,summa_amort_sum, format4)
        worksheet.write(rows,col+8,summa_ost_sum, format4)
        worksheet.merge_range(rows+3,col+2,rows+3,col+3,'Председатель Правления', format5)
        worksheet.merge_range(rows+3,col+6,rows+3,col+7,'Ибраимова А.С.', format5)
        worksheet.merge_range(rows+5,col+2,rows+5,col+3,'Главный бухгалтер', format5)
        worksheet.merge_range(rows+5,col+6,rows+5,col+7,'Шеркулова А.Т.', format5)
        workbook.close()

    #return render(request, 'main_os/report.html', {'i':i, 'a_id': a_id, 'c': choice})
        return response
    else:
        return redirect('user_login')

@csrf_exempt
def report_spis_real(request):
    if request.user.is_authenticated:

        choice = request.POST['dropdown']
        #branch = request.POST['dropdown2']
        type_spis = request.POST['dropdown3']
        date_from = request.POST['month_from']
        date_to = request.POST['month_to']
        date_from = datetime.strptime(date_from, "%Y-%m-%d")
        date_from_year = date_from.year
        date_from_month = date_from.month
        date_from_month = '{:02}'.format(date_from_month)
        date_to = datetime.strptime(date_to, "%Y-%m-%d")
        date_to_year = date_to.year
        date_to_month = date_to.month
        date_to_month = '{:02}'.format(date_to_month)

        if type_spis != '0':
            t = type_spisan.objects.get(type_spisan_id=type_spis)
            type = t.type_name
        else:
            type = 'Списание/Реализация'

        file_name = type +" "+str(date_to)
        file_name = translit(file_name, "ru", reversed=True)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename={}.xlsx".format(file_name)
        context = {
            'in_memory': True,
            'remove_timezone': True
        }
        workbook = xlsxwriter.Workbook(response, context)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 15)
        worksheet.set_column('I:I', 15)
        style_align_center = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 11})
        style_align_center_border = workbook.add_format({'align': 'center', 'bold': True, 'border': 1, 'text_wrap': True})
        worksheet.merge_range('A1:F1', 'Ведомость по списанию/реализации за '+str(date_from_month)+'.'+str(date_from_year)+' г. - '+str(date_to_month)+'.'+str(date_to_year)+' г.', style_align_center)
        format2 = workbook.add_format({'num_format': 'dd-mm-yy', 'border': 1, 'align': 'center'})
        format1 = workbook.add_format({'border': 1, 'align': 'center'})
        format3 = workbook.add_format({'align': 'center', 'border': 1, 'text_wrap': True})
        format4 = workbook.add_format({'align': 'center', 'bold': True})
        format5 = workbook.add_format({'align': 'center'})
        #worksheet.write('A1', 'Ведомость амортизации '+type_name+' за '+str(date_month)+' '+str(date_year)+'', style_align_center)
        worksheet.write('A3', 'Дата ввода в эксплуатацию', style_align_center_border)
        worksheet.write('B3', 'Инвентарный номер', style_align_center_border)
        worksheet.write('C3', 'Наименование', style_align_center_border)
        worksheet.write('D3', 'Балансовая стоимость', style_align_center_border)
        worksheet.write('E3', 'Накопленная амортизация', style_align_center_border)
        worksheet.write('F3', 'Сумма для списания', style_align_center_border)
        worksheet.write('G3', 'Дата списания', style_align_center_border)
        worksheet.write('H3', 'Списание/Реализация', style_align_center_border)
        rows = 3
        col=0
        summa_spisaniya = 0
        sum_bal_price = 0
        sum_amort_sum = 0
        i=0

        if (choice == '0' and type_spis == '0'):
            main = main_t.objects.filter(date_spisan__gte=date_from, date_spisan__lte=date_to)
        if (choice != '0' and type_spis != '0'):
            main = main_t.objects.filter(date_spisan__gte=date_from, date_spisan__lte=date_to, type_id=choice, type_spisan=type_spis)
        if (choice != '0' and type_spis == '0'):
            main = main_t.objects.filter(date_spisan__gte=date_from, date_spisan__lte=date_to, type_id=choice)
        if (choice == '0' and type_spis != '0'):
            main = main_t.objects.filter(date_spisan__gte=date_from, date_spisan__lte=date_to, type_spisan=type_spis)

        for m in main:
            if round(m.bal_price,2) == round(m.amort_sum,2):
                sum = 0
            else:
                sum = round(m.bal_price,2)-round(m.amort_sum,2)
            if m.type_spisan != 0:
                s = type_spisan.objects.get(type_spisan_id=m.type_spisan)
                type_s = s.type_name
            else:
                type_s = ''
            if len(str(m.inv)) < 8:
                inv = '{:08}'.format(m.inv)
            else:
                inv = m.inv
            worksheet.write(rows,col,m.date_vvod, format2)
            worksheet.write(rows,col+1,inv, format1)
            worksheet.write(rows,col+2,m.name, format3)
            worksheet.write(rows,col+3,m.bal_price, format1)
            worksheet.write(rows,col+4,m.amort_sum, format1)
            worksheet.write(rows,col+5,sum, format1)
            worksheet.write(rows,col+6,m.date_spisan, format2)
            worksheet.write(rows,col+7,type_s, format1)
            rows=rows+1
            sum_bal_price = sum_bal_price + m.bal_price
            sum_amort_sum = sum_amort_sum + m.amort_sum
            summa_spisaniya = summa_spisaniya + sum

        worksheet.write(rows,col+2,'Всего:', format4)
        worksheet.write(rows,col+3,sum_bal_price, format4)
        worksheet.write(rows,col+4,sum_amort_sum, format4)
        worksheet.write(rows,col+5,summa_spisaniya, format4)
        worksheet.merge_range(rows+3,col,rows+3,col+1,'Председатель комиссии:', format5)
        worksheet.merge_range(rows+3,col+4,rows+3,col+5,'ФИО', format5)
        worksheet.merge_range(rows+5,col,rows+5,col+1,'Члены комиссии:', format5)
        worksheet.merge_range(rows+5,col+4,rows+5,col+5,'ФИО', format5)
        workbook.close()

    #return render(request, 'main_os/report.html', {'i':i, 'a_id': a_id, 'c': choice})
        return response
    else:
        return redirect('user_login')

@csrf_exempt
def report_general(request):
    if request.user.is_authenticated:

        choice = request.POST['dropdown']

        if choice != '0':
            t = type_id.objects.get(type_id=choice)
            type = t.type
        else:
            type = 'общая'

        file_name = 'Ведомость '+ type
        file_name = translit(file_name, "ru", reversed=True)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename={}.xlsx".format(file_name)
        context = {
            'in_memory': True,
            'remove_timezone': True
        }
        workbook = xlsxwriter.Workbook(response, context)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 15)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 25)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        worksheet.set_column('H:H', 15)
        worksheet.set_column('I:I', 15)
        style_align_center = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 11})
        style_align_center_border = workbook.add_format({'align': 'center', 'bold': True, 'border': 1, 'text_wrap': True})
        worksheet.merge_range('A1:I1', 'Ведомость '+ str(type), style_align_center)
        format2 = workbook.add_format({'num_format': 'dd-mm-yy', 'border': 1, 'align': 'center'})
        format1 = workbook.add_format({'border': 1, 'align': 'center'})
        format3 = workbook.add_format({'align': 'center', 'border': 1, 'text_wrap': True})
        format4 = workbook.add_format({'align': 'center', 'bold': True})
        format5 = workbook.add_format({'align': 'center'})
        #worksheet.write('A1', 'Ведомость амортизации '+type_name+' за '+str(date_month)+' '+str(date_year)+'', style_align_center)
        worksheet.write('A3', 'Дата ввода в эксплуатацию', style_align_center_border)
        worksheet.write('B3', 'Инвентарный номер', style_align_center_border)
        worksheet.write('C3', 'Наименование', style_align_center_border)
        worksheet.write('D3', 'Срок полезной службы', style_align_center_border)
        worksheet.write('E3', 'Остаток срока службы', style_align_center_border)
        worksheet.write('F3', 'Ежемесячная норма амортизации', style_align_center_border)
        worksheet.write('G3', 'Первоначальная стоимость', style_align_center_border)
        worksheet.write('H3', 'Накопленная амортизация', style_align_center_border)
        worksheet.write('I3', 'Остаточная стоимость', style_align_center_border)
        rows = 3
        col=0
        summa_amort_sum_month = 0
        summa_bal_price = 0
        summa_amort_sum = 0
        summa_ost_sum = 0
        i=0

        if choice == '0':
            main = main_t.objects.filter(date_spisan=None)
        else:
            main = main_t.objects.filter(type_id=choice, date_spisan=None)


        for m in main:
            if len(str(m.inv)) < 8:
                inv = '{:08}'.format(m.inv)
            else:
                inv = m.inv
            if m.type_id != 1:
                ostatok_sroka_new = round((m.bal_price - m.amort_sum) / m.amort_sum_month)
                ost_sum = round(m.bal_price - m.amort_sum,2)
            else:
                ostatok_sroka_new = 0
                ost_sum = 0

            worksheet.write(rows,col,m.date_vvod, format2)
            worksheet.write(rows,col+1,inv, format1)
            worksheet.write(rows,col+2,m.name, format3)
            worksheet.write(rows,col+3,m.amort_month, format1)
            worksheet.write(rows,col+4,ostatok_sroka_new, format1)
            worksheet.write(rows,col+5,round(m.amort_sum_month,2), format1)
            worksheet.write(rows,col+6,m.bal_price, format1)
            worksheet.write(rows,col+7,round(m.amort_sum,2), format1)
            worksheet.write(rows,col+8,ost_sum, format1)
            rows=rows+1
            summa_amort_sum_month = summa_amort_sum_month+round(m.amort_sum_month,2)
            summa_bal_price = summa_bal_price + m.bal_price
            summa_amort_sum = summa_amort_sum + round(m.amort_sum,2)
            summa_ost_sum = summa_ost_sum + ost_sum

        worksheet.write(rows,col+2,'Всего:', format4)
        worksheet.write(rows,col+5,summa_amort_sum_month, format4)
        worksheet.write(rows,col+6,summa_bal_price, format4)
        worksheet.write(rows,col+7,summa_amort_sum, format4)
        worksheet.write(rows,col+8,summa_ost_sum, format4)
        worksheet.merge_range(rows+3,col,rows+3,col+1,'Председатель комиссии:', format5)
        worksheet.merge_range(rows+3,col+4,rows+3,col+5,'ФИО', format5)
        worksheet.merge_range(rows+5,col,rows+5,col+1,'Члены комиссии:', format5)
        worksheet.merge_range(rows+5,col+4,rows+5,col+5,'ФИО', format5)
        workbook.close()

    #return render(request, 'main_os/report.html', {'i':i, 'a_id': a_id, 'c': choice})
        return response
    else:
        return redirect('user_login')

@csrf_exempt
def report_prbo(request):
    if request.user.is_authenticated:

        date = request.POST['month']

        file_name = 'PRBO_' + str(date)
        file_name = translit(file_name, "ru", reversed=True)
        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = "attachment; filename={}.xlsx".format(file_name)
        context = {
            'in_memory': True,
            'remove_timezone': True
        }
        workbook = xlsxwriter.Workbook(response, context)
        worksheet = workbook.add_worksheet()
        worksheet.set_column('A:A', 25)
        worksheet.set_column('B:B', 15)
        worksheet.set_column('C:C', 15)
        worksheet.set_column('D:D', 15)
        worksheet.set_column('E:E', 15)
        worksheet.set_column('F:F', 15)
        worksheet.set_column('G:G', 15)
        style_align_center = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 11})
        style_align_center_border = workbook.add_format({'align': 'center', 'bold': True, 'border': 1, 'text_wrap': True})
        worksheet.merge_range('A1:I1', 'Ведомость амортизации основных средств ' + str(date), style_align_center)
        format2 = workbook.add_format({'num_format': 'dd-mm-yy', 'border': 1, 'align': 'center'})
        format1 = workbook.add_format({'border': 1, 'align': 'center'})
        format3 = workbook.add_format({'align': 'center', 'border': 1, 'text_wrap': True})
        format4 = workbook.add_format({'align': 'center', 'bold': True})
        format5 = workbook.add_format({'align': 'center'})
        worksheet.write('A3', 'Наименование', style_align_center_border)
        worksheet.write('B3', 'Срок полезной службы', style_align_center_border)
        worksheet.write('C3', 'Остаток срока службы', style_align_center_border)
        worksheet.write('D3', 'Ежемесячная норма амортизации', style_align_center_border)
        worksheet.write('E3', 'Первоначальная стоимость', style_align_center_border)
        worksheet.write('F3', 'Накопленная амортизация', style_align_center_border)
        worksheet.write('G3', 'Остаточная стоимость', style_align_center_border)
        rows = 3
        col=0
        summa_amort_sum_month = 0
        summa_bal_price = 0
        summa_amort_sum = 0
        summa_ost_sum = 0
        i=0

        main = main_t.objects.filter(type_id__gt=1, type_spisan=None)
        for m in main:
            if round(m.bal_price,1) != round(m.amort_sum,1):
                ostatok_sroka_new = round((m.bal_price - m.amort_sum) / m.amort_sum_month)
                ost_sum = round(m.bal_price - m.amort_sum,2)

                worksheet.write(rows,col,m.name, format3)
                worksheet.write(rows,col+1,m.amort_month, format1)
                worksheet.write(rows,col+2,ostatok_sroka_new, format1)
                worksheet.write(rows,col+3,round(m.amort_sum_month,2), format1)
                worksheet.write(rows,col+4,m.bal_price, format1)
                worksheet.write(rows,col+5,round(m.amort_sum,2), format1)
                worksheet.write(rows,col+6,ost_sum, format1)
                rows=rows+1
                summa_amort_sum_month = summa_amort_sum_month+round(m.amort_sum_month,2)
                summa_bal_price = summa_bal_price + m.bal_price
                summa_amort_sum = summa_amort_sum + round(m.amort_sum,2)
                summa_ost_sum = summa_ost_sum + ost_sum

        worksheet.write(rows,col+2,'Всего:', format4)
        worksheet.write(rows,col+3,summa_amort_sum_month, format4)
        worksheet.write(rows,col+4,summa_bal_price, format4)
        worksheet.write(rows,col+5,summa_amort_sum, format4)
        worksheet.write(rows,col+6,summa_ost_sum, format4)
        worksheet.merge_range(rows+3,col,rows+3,col+1,'Председатель комиссии:', format5)
        worksheet.merge_range(rows+3,col+4,rows+3,col+5,'ФИО', format5)
        worksheet.merge_range(rows+5,col,rows+5,col+1,'Члены комиссии:', format5)
        worksheet.merge_range(rows+5,col+4,rows+5,col+5,'ФИО', format5)
        workbook.close()
        return response
    else:
        return redirect('user_login')

def ch_bal_price(request):
    if request.user.is_authenticated:
        return render(request, 'main_os/ch_bal_price.html')
    else:
        return redirect('user_login')

@csrf_exempt
def change_bal_price_def(request):
    if request.user.is_authenticated:
        choice = request.POST['dropdown']
        date1 = request.POST['date']
        inv_num = request.POST['inv_num']
        change_sum = request.POST['change_sum']
        comment = request.POST['comment']


        if int(choice) == 1:
            ch_id = 1
        else:
            ch_id = 2

        if main_t.objects.filter(inv=inv_num).exists():
            m = main_t.objects.get(inv=inv_num)
            id_oborud1 = m.id_oborud
            bal_price1 = m.bal_price

            change = change_bal_price(id_oborud=id_oborud1, name=comment, summ=change_sum,
                                        date=date1, summ_before=bal_price1, change_id=ch_id)
            change.save()
            message = "OK"
        else:
            message = "Неверный инвентарный номер"

        return render(request, 'main_os/change_bal_price.html', {'message': message})
    else:
        return redirect('user_login')

def mbp(request):
    if request.user.is_authenticated:
        id = 1
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def mebel(request):
    if request.user.is_authenticated:
        id = 2
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def comp(request):
    if request.user.is_authenticated:
        id = 3
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def transport(request):
    if request.user.is_authenticated:
        id = 4
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def cap(request):
    if request.user.is_authenticated:
        id = 5
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def nem_actives(request):
    if request.user.is_authenticated:
        id = 6
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def oborudovanie(request):
    if request.user.is_authenticated:
        id = 7
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def zdaniya(request):
    if request.user.is_authenticated:
        id = 8
        response = list(request, id)
        return response
    else:
        return redirect('user_login')

def list(request, id):
    if request.user.is_authenticated:
        main = main_t.objects.filter(type_id=id)

        t = type_id.objects.get(type_id=id)
        s = 0
        for y in main:
            s = s+1
        response = union_list(request, s, main, t)
        return response

    else:
        return redirect('user_login')

def union_list(request, s, main, t):
    sum_amort_sum_month = 0
    sum_bal_price = 0
    sum_amort_sum = 0
    sum_ost_sum = 0
    r=0
    m = numpy.chararray((s,11),unicode=True, itemsize=100)
    for i in main:
        if amort_t.objects.filter(id_oborud=i.id_oborud).exists():
            amort = amort_t.objects.filter(id_oborud=i.id_oborud).order_by('-date_amort')[0]
            ost_sum = amort.ost_sum
        else:
            ost_sum = 0
        dep = branch_id.objects.get(branch_id=i.branch_id)
        #name = str(i.name)
        if len(str(i.inv)) < 8:
            inv = '{:08}'.format(i.inv)
        else:
            inv = i.inv
        m[r][0] = str(i.date_vvod)
        m[r][1] = inv
        m[r][2] = i.name
        m[r][3] = round(i.amort_month)
        m[r][4] = round(i.amort_sum_month,2)
        m[r][5] = round(i.bal_price,2)
        m[r][6] = round(i.amort_sum,2)
        m[r][7] = round(ost_sum,2)
        m[r][8] = t.type
        m[r][9] = dep.name
        sum_bal_price = round((sum_bal_price +i.bal_price),2)
        sum_amort_sum_month = round((sum_amort_sum_month + i.amort_sum_month),2)
        sum_amort_sum = round((sum_amort_sum + i.amort_sum),2)
        sum_ost_sum = round((sum_ost_sum + ost_sum),2)
        r = r + 1

    caption = t.type
    paginator = Paginator(m, 30)
    page = request.GET.get('page')
    m = paginator.get_page(page)

    return render(request, 'main_os/list.html', {'m':m, 'sum_ost_sum': sum_ost_sum,
            'sum_amort_sum': sum_amort_sum, 'sum_bal_price': sum_bal_price, 'sum_amort_sum_month': sum_amort_sum_month, 'caption': caption})

def add_os(request):
    if request.user.is_authenticated:
        emp = employee_id.objects.all()
        br = branch_id.objects.all()
        return render(request, 'main_os/add_os.html', {'emp': emp, 'br':br})
    else:
        return redirect('user_login')

@csrf_exempt
def add_os_finish(request):
    if request.user.is_authenticated:
        name = request.POST['name_os']
        date = request.POST['date']
        bal_price = request.POST['bal_price_os']
        type = request.POST['dropdown']
        date_vvod = request.POST['date_vvod']
        #emp = request.POST.get('dropdown1')
        br = request.POST.get('dropdown2')
        a_m = request.POST['srok']
        emp = 0

        if type == '3':
            main = main_t.objects.filter(inv__gte=20000000,inv__lt=30000000).order_by('-inv')[0]
            new_inv = main.inv + 1
        else:
            m = main_t.objects.filter(type_id=int(type)).order_by('-inv')[0]
            new_inv = m.inv + 1
            while main_t.objects.filter(inv=new_inv).exists() is True:
                new_inv = new_inv + 1
        m1 = main_t.objects.all().order_by('-id_oborud')[0]
        id_o1 = m1.id_oborud + 1
        if len(str(id_o1)) < 8:
            id_o2 = '{:08}'.format(id_o1)
            id_o = str(id_o2)
        else:
            id_o = id_o1
        if int(type) != 1:
            a_s_m = float(bal_price)/int(a_m)

            add = main_t(name=name, pur_date=date, inv=new_inv, bal_price=bal_price, type_id=type, amort_month=a_m,
                     date_vvod=date_vvod, emp_id=emp, amort_sum=0, amort_sum_month=a_s_m, branch_id=br,
                     id_oborud=id_o, izm=0, dop_month=0, kol_month=0, company_id=0)
            add.save()

        else:
            add = main_t(name=name, pur_date=date, inv=new_inv, bal_price=bal_price, type_id=type, amort_month=0,
                     date_vvod=date_vvod, emp_id=emp, amort_sum=0, amort_sum_month=0, branch_id=br,
                     id_oborud=id_o, izm=0, dop_month=0, kol_month=0, company_id=0)
            add.save()

        return render(request, 'main_os/add_os_finish.html', {'m1':new_inv, 'name': name})
    else:
        return redirect('user_login')

def directory_list(request, id):
    if request.user.is_authenticated:
        if id == 1:
            m = employee_id.objects.filter(~Q(active=0)).order_by('surname')
            caption = 'Сотрудники'
        if id == 2:
            m = depart.objects.all()
            caption = 'Отделы'
        if id == 3:
            m = branch_id.objects.all()
            caption = 'Точки обслуживания'
        if id == 4:
            m = company_id.objects.all()
            caption = 'Поставщики'

        paginator = Paginator(m, 30)
        page = request.GET.get('page')
        m = paginator.get_page(page)
        return render(request,  'main_os/list_directory.html', {'m':m, 'id': id, 'caption': caption})
    else:
        return redirect('user_login')

def search(request):
    if request.user.is_authenticated:
        m = {}
        search = request.GET.get('search')
        #if search.isdigit() == True:
        try:
            search = int(search)
            #main_t.objects.filter(inv=search).exists():
            main = main_t.objects.filter(inv=search)
            s=0
            for y in main:
                s=s+1
                t = type_id.objects.get(type_id=y.type_id)
            response = union_list(request, s, main, t)
        except:
            #if isinstance(search,str) == True:
            if main_t.objects.filter(name__icontains=search).exists():
                main = main_t.objects.filter(name__icontains=search)
                s = 0
                for y in main:
                    s=s+1
                    t = type_id.objects.get(type_id=y.type_id)
                response = union_list(request, s, main, t)
            else:
                return render(request, 'main_os/list.html', {'m':m})
        return response
    else:
        return redirect('user_login')

def spis_real(request):
    if request.user.is_authenticated:
        type = type_spisan.objects.all()
        return render(request, 'main_os/spis_real.html', {'type':type})
    else:
        return redirect('user_login')

@csrf_exempt
def def_spis_real(request):
    if request.user.is_authenticated:
        type = request.POST['dropdown']
        inv = request.POST['inv_num']
        date = request.POST['date']
        comment = request.POST['comment']

        if main_t.objects.filter(inv=inv).exists():
            t = type_spisan.objects.get(type_spisan_id=type)
            m = main_t.objects.get(inv=inv)
            m.date_spisan = date
            m.spisan_comm = comment
            m.type_spisan = type
            m.save()
            message = t.type_name + " " + m.name + " инвентарный номер:" + " " + str(m.inv) + " | Статус: ОК"
        else:
            message = "Введите корректный инвентарный номер"

        return render(request, 'main_os/spis_real_finish.html', {'message': message})
    else:
        return redirect('user_login')

def cards(request):
    if request.user.is_authenticated:
        response = cards_table_create(request, 0)
        return  render(request, 'main_os/cards_template.html', response)
    else:
        return redirect('user_login')

def cards_table_create(request, ch):
    if request.method == 'GET':
        if request.GET.get('dropdown') is not None:
            e_id = request.GET['dropdown']
            request.session['emp_id'] = e_id
            m = main_t.objects.filter(emp_id=e_id, date_spisan=None).order_by('-type_id')
            e = employee_id.objects.get(emp_id=e_id)
            s = e.surname + ' ' + e.name + ' ' + e.lastname
            if e.lastname != '':
                name = 'Card:'+ e.surname + ' ' + e.name[0] + '.' + e.lastname[0]
            else:
                name = 'Card:'+ e.surname + ' ' + e.name[0] + '.'
            request.session['name'] = name
            o = depart.objects.get(depart_id=e.depart_id)
            otdel = o.name
            change = ch
        else:
            try:
                e_id = request.session['emp_id']
                m = main_t.objects.filter(emp_id=e_id, date_spisan=None).order_by('-type_id')
                e = employee_id.objects.get(emp_id=e_id)
                s = e.surname + ' ' + e.name + ' ' + e.lastname
                if e.lastname != '':
                    name = 'Card:'+ e.surname + ' ' + e.name[0] + '.' + e.lastname[0]
                else:
                    name = 'Card:'+ e.surname + ' ' + e.name[0] + '.'
                request.session['name'] = name
                o = depart.objects.get(depart_id=e.depart_id)
                otdel = o.name
                change = ch
            except:
                s = ''
                m = {}
                e_id =''
                otdel = ''
                change = ''
        emp = employee_id.objects.filter(~Q(active=0)).order_by('surname')
        date = datetime.now()
        date = datetime.strftime(date, '%d-%m-%Y')
    return {'emp': emp, 'm':m, 's':s, 'e_id': e_id, 'otdel': otdel, 'ch':change, 'date': date}

def cards_pdf(request):
    if request.user.is_authenticated:
        response = cards_table_create(request, 0)
        html_string = render_to_string('main_os/cards_pdf_template.html', response)

        html = HTML(string=html_string)
        html.write_pdf(target='c:/test-dir/mypdf.pdf');

        name = request.session['name']
        file_name = str(name)
        file_name = translit(file_name, "ru", reversed=True)

        fs = FileSystemStorage('/test-dir')
        with fs.open('mypdf.pdf') as pdf:
            result = HttpResponse(pdf, content_type='application/pdf')
            result['Content-Disposition'] = 'attachment; filename={}.pdf'.format(file_name)
            return result

        return result
    else:
        return redirect('user_login')

def cards_change(request):
    if request.user.is_authenticated:
        response = cards_table_create(request, 1)
        return  render(request, 'main_os/cards_template.html', response)
    else:
        return redirect('user_login')

def cards_del_item(request, inv):
    if request.user.is_authenticated:
        username = request.user.username
        date = datetime.now()
        m = main_t.objects.get(inv=inv)
        h = history_item()
        h.ex_emp = m.emp_id
        h.new_emp = 1
        h.inv = inv
        h.date_moving = date
        h.id_oborud = m.id_oborud
        h.name_item = m.name
        h.username = username
        m.emp_id = 1
        h.save()
        m.save()
        response = cards_table_create(request, 1)
        return  render(request, 'main_os/cards_template.html', response)
    else:
        return redirect('user_login')

def cards_add_item(request):
    if request.user.is_authenticated:
        username = request.user.username
        inv = request.GET.get('inv_item')
        e_id = request.session['emp_id']
        date = datetime.now()
        h = history_item()
        m = main_t.objects.get(inv=inv)
        h.ex_emp = m.emp_id
        h.new_emp = e_id
        h.inv = inv
        h.date_moving = date
        h.id_oborud = m.id_oborud
        h.name_item = m.name
        h.username = username
        m.emp_id = e_id
        h.save()
        m.save()
        response = cards_table_create(request, 1)
        return  render(request, 'main_os/cards_template.html', response)
    else:
        return redirect('user_login')

def employee_disable(request, id):
    if request.user.is_authenticated:
            emp = employee_id.objects.get(emp_id=id)
            emp.active = 0
            emp.save()
            response = directory_list(request, 1)
            return response
    else:
        return redirect('user_login')

def depart_disable(request, id):
    if request.user.is_authenticated:
            depart.objects.get(depart_id=id).delete()
            response = directory_list(request, 2)
            return response
    else:
        return redirect('user_login')

def employee_change(request, id):
    if request.user.is_authenticated:
        try:
            emp_surname = request.GET.get('change_surname')
            emp_name = request.GET.get('change_name')
            emp_lastname = request.GET.get('change_lastname')
            emp_id = id
            dep_id = request.GET.get('dropdown')
            emp_depart_id = dep_id
            e = employee_id.objects.get(emp_id=emp_id)
            e.depart_id  = dep_id
            e.surname = emp_surname
            e.name = emp_name
            e.lastname = emp_lastname
            e.save()
            message = 'Изменения сохранены'
        except:
            emp = employee_id.objects.get(emp_id=id)
            emp_depart_id = emp.depart_id
            emp_id = emp.emp_id
            emp_surname = emp.surname
            emp_name = emp.name
            emp_lastname = emp.lastname
            message = ''
        dep = depart.objects.get(depart_id=emp_depart_id)
        dep_name = dep.name
        dep_id = dep.depart_id
        departs = depart.objects.all()
        flag = 1
        return render(request, 'main_os/employee_change_template.html', {'emp_surname': emp_surname, 'emp_name': emp_name, 'emp_lastname': emp_lastname,
                    'emp_id': emp_id, 'dep_name': dep_name, 'dep_id': dep_id, 'departs': departs, 'message': message, 'flag': flag})
    else:
        return redirect('user_login')

@csrf_exempt
def directory_list_add(request, id):
    if request.user.is_authenticated:
        #if id == 1 or 2:
            if id == 1:
                if request.method == 'POST':
                    surname = request.POST['add_surname']
                    name = request.POST['add_name']
                    lastname = request.POST['add_lastname']
                    if employee_id.objects.filter(surname=surname, name=name, lastname=lastname).exists():
                        message = 'Сотрудник с таким ФИО уже существует'
                    else:
                        dep = request.POST['dropdown']
                        e = employee_id.objects.order_by('-emp_id')[0]
                        emp = employee_id()
                        emp.surname = str(surname)
                        emp.name = str(name)
                        emp.lastname = str(lastname)
                        emp.emp_id = e.emp_id + 1
                        emp.depart_id = dep
                        emp.active = 1
                        emp.save()
                        message = str(surname)+' '+str(name)+' '+str(lastname)+' добавлен'
                else:
                    message = 'Добавление нового сотрудника:'
            if id == 2:
                if request.method == 'POST':
                    name = request.POST['add_depart']
                    d = depart.objects.order_by('-depart_id')[0]
                    dep = depart()
                    dep.name = name
                    dep.depart_id = d.depart_id + 1
                    dep.save()
                    message = str(name)+' добавлен'
                else:
                    message = 'Добавление нового подразделения:'
            if id == 3:
                if request.method == 'POST':
                    name = request.POST['add_branch']
                    br = branch_id.objects.order_by('-branch_id')[0]
                    branch = branch_id()
                    branch.name = name
                    branch.branch_id = br.branch_id+1
                    branch.save()
                    message = str(name)+ ' добавлен'
                else:
                    message = 'Добавление новой точки обслуживания:'
            departs = depart.objects.all()
            return  render(request, 'main_os/directory_list_add_template.html', {'message': message, 'departs': departs,'id': id})
    else:
        return redirect('user_login')

def depart_change(request, id):
    if request.user.is_authenticated:
        flag = 2
        try:
            dep_name = request.GET['change_dep_name']
            dep = depart.objects.get(depart_id=id)
            dep.name = dep_name
            dep.save()
            message = 'Изменения сохранены'
        except:
            dep = depart.objects.get(depart_id=id)
            dep_name = dep.name
            dep_id = id
            message = ''
        return  render(request, 'main_os/employee_change_template.html', {'dep_name':dep_name, 'id': id, 'flag': flag, 'message': message})
    else:
        return redirect('user_login')

def get_history_item(request):
    if request.user.is_authenticated:
        try:
            inv = request.GET['inv']
            h = history_item.objects.filter(inv=inv)
            flag = 1
            message = inv
        except:
            inv =''
            flag = 0
            h = ''
            message = ''
        return  render(request, 'main_os/history_item_template.html', {'flag': flag, 'inv': inv, 'h': h, 'message': message})
    else:
        return redirect('user_login')

def item_movement(request):
    if request.user.is_authenticated:
        date = datetime.now()
        username = request.user.username
        emp_id = request.POST.get('emp_id')
        emp = employee_id.objects.get(emp_id=emp_id)
        name = emp.name
        inv_list = request.POST.getlist('list[]')
        if inv_list:
            i=0
            for i in range(len(inv_list)):
                item = main_t.objects.get(inv=inv_list[i])
                id_item = item.id_oborud
                name_item = item.name
                ex_emp = item.emp_id
                item.emp_id = emp_id
                item.save()
                try:
                    check_invoice = history_item.objects.filter(date_moving=date, ex_emp=ex_emp, new_emp=emp_id).order_by('-invoice_number')[0]
                    print(check_invoice.invoice_number)
                    h = history_item(id_oborud=id_item, inv=inv_list[i], name_item=name_item, date_moving=date, ex_emp=ex_emp, new_emp=emp_id, username=username, invoice_number=check_invoice.invoice_number)
                except:
                    last_invoice_number = history_item.objects.all().order_by('-invoice_number')[0]
                    next_invoice_number = int(last_invoice_number.invoice_number) + 1
                    h = history_item(id_oborud=id_item, inv=inv_list[i], name_item=name_item, date_moving=date, ex_emp=ex_emp, new_emp=emp_id, username=username, invoice_number=next_invoice_number)
                h.save()
            return HttpResponse('УСПЕШНО ПЕРЕДАНО!')
        else:
            return HttpResponse('НЕОБХОДИМО ВЫБРАТЬ ОСНОВНЫЕ СРЕДСТВА!')
    else:
        return redirect('user_login')

def invoice(request):
    if request.user.is_authenticated:
        #try:
        if request.GET.get('date') is not None:
            date = request.GET.get('date')
            #invoices = history_item.objects.filter(date_moving=date)
            #invoices = history_item.objects.values('invoice_number').filter(date_moving=date)
            invoices = history_item.objects.raw(('SELECT * FROM upload_db_history_item WHERE date_moving="%s" GROUP BY invoice_number') % date)
            if not invoices:
                msg = 'НИЧЕГО НЕ НАЙДЕНО'
            else:
                msg = ''
        #except:
        else:
            invoices = ''
            date = ''
            msg = ''
        return render(request, 'main_os/invoice.html', {'invoices': invoices, 'date': date, 'msg': msg})
    else:
        return redirect('user_login')

def invoice_detail(request, invoice_number):
    if request.user.is_authenticated:
        data = history_item.objects.filter(invoice_number=invoice_number)[0]
        ex_emp = data.ex_emp
        new_emp = data.new_emp
        invoice_number = data.invoice_number
        date = data.date_moving
        invoice = history_item.objects.filter(invoice_number=invoice_number)
        return render(request, 'main_os/invoice_detail.html', {'invoice': invoice, 'invoice_number': invoice_number,
                        'ex_emp':ex_emp, 'new_emp': new_emp, 'date': date})
    else:
        return redirect('user_login')

def invoice_pdf(request, invoice_number):
    if request.user.is_authenticated:
        data = history_item.objects.filter(invoice_number=invoice_number)[0]
        ex_emp = data.ex_emp
        new_emp = data.new_emp
        invoice_number = data.invoice_number
        date = data.date_moving
        response = history_item.objects.filter(invoice_number=invoice_number)
        html_string = render_to_string('main_os/invoice_detail_pdf.html', {'invoice': response,
                        'invoice_number': invoice_number,'ex_emp':ex_emp, 'new_emp': new_emp, 'date': date})

        html = HTML(string=html_string)
        html.write_pdf(target='c:/test-dir/mypdf.pdf');

        #name = request.session['name']
        #file_name = 'Накладная № '+ str(invoice_number)
        file_name = "Invoice # %s" % invoice_number
        #file_name = translit(file_name, "ru", reversed=True)

        fs = FileSystemStorage('/test-dir')
        with fs.open('mypdf.pdf') as pdf:
            result = HttpResponse(pdf, content_type='application/pdf')
            result['Content-Disposition'] = 'attachment; filename={}.pdf'.format(file_name)
            return result

        return result
    else:
        return redirect('user_login')
