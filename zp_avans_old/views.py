from django.shortcuts import render
from .models import accounts, months
import pandas as pd
#import openpyxl
#import smtplib                                      # Импортируем библиотеку по работе с SMTP
import os
#import mimetypes
#import cgi, cgitb
import datetime
import html
import xlsxwriter

# Create your views here.
def glav(request):
    #client = client.objects.all()
    return render(request, "zp_avans/glav.html")

def zp(request):

    month = months.objects.all()
    for m in month:
        if datetime.datetime.today().strftime("%B")== m.eng:
            mon=m.rus
            year=datetime.datetime.today().strftime("%Y")
            m_y= mon+' '+year+' г.'

    workbook = xlsxwriter.Workbook('c:\дсп\Заработная плата за '+m_y+'.xlsx')
    worksheet = workbook.add_worksheet()
    style_align_right = workbook.add_format({'align': 'right', 'bold': True, 'font_size': 10})
    style_align_center = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 10})
    style_align_center_border = workbook.add_format({'align': 'center', 'bold': True, 'border': 1})
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    border = workbook.add_format({'border': 1})
    worksheet.write('D1', 'Приложение 1', style_align_right)
    worksheet.write('D2','к Договору на обслуживание в рамках зарплатного проекта', style_align_right)
    worksheet.write('D3','от «___»_____________20__г.', style_align_right)
    worksheet.write('C6','Ведомость о зачислении денежных средств на счета Сотрудников', style_align_center)
    worksheet.write('C7','со Счета Клиента в Банке № 1130 0200 0018 2126', style_align_center)
    worksheet.write('C8','за '+datetime.datetime.today().strftime("%d-%m-%Y"), style_align_center)
    worksheet.write('A11','№ п/п', style_align_center_border)
    worksheet.write('B11','ФИО работника', style_align_center_border)
    worksheet.write('C11','№ счета работника', style_align_center_border)
    worksheet.write('D11','Сумма, сом', style_align_center_border)

    worksheet.set_column('D:D', 18, format1)
    worksheet.set_column('B:B', 38, None)
    #worksheet.write_string(1, 0, '', cell_format)
    worksheet.set_column('C:C', 20, None)
    worksheet.set_column('A:A', 5, None)
    n=1
    rows=11
    col=0
    summa = 0

    data = pd.read_excel (r'C:\дсп\Заработная плата за '+mon+' '+year+' г. на карточку.xlsx', header=None, names=['Number', 'Sum'])

    for index, row in data.iterrows():
        ch_num = row['Number']
        data = accounts.objects.get(ch_account=ch_num)
        k_acc = data.k_account
        name = data.fio
        sum = row['Sum']
        summ = float('{:.2f}'.format(sum))

        worksheet.write(rows,col,n, border)
        worksheet.write(rows,col+1,name, border)
        worksheet.write(rows,col+2,str(data.k_account), border)
        worksheet.write(rows,col+3,summ, border)
        rows=rows+1
        col=0
        n=n+1
        summa = summa+summ
    worksheet.write(rows,3,float('{:.2f}'.format(summa)))
    worksheet.write(rows+2,0,'Сумма')
    worksheet.write(rows+4,0,'Председатель Правления')
    worksheet.write(rows+4,2,'Жунушалиев Д.Т.')
    worksheet.write(rows+5,3,'МП')
    worksheet.write(rows+6,0,'Главный бухгалтер')
    worksheet.write(rows+6,2,'Шеркулова А.Т.')
    worksheet.write(rows+8,0,'Отметка об исполнении Банка')
    worksheet.write(rows+10,0,'Уполномоченное лицо/лица Банка')
    worksheet.write(rows+10,2,'МП')
    workbook.close()
    workbook.save()
    return render (request, 'zp_avans/result.html', {'k_account': k_acc, 'name': name, 'sum': summ})


def avans(request):

    month = months.objects.all()
    for m in month:
        if datetime.datetime.today().strftime("%B")== m.eng:
            mon=m.rus
            year=datetime.datetime.today().strftime("%Y")
            m_y= mon+' '+year+' г.'

    workbook = xlsxwriter.Workbook('c:\дсп\Аванс за '+m_y+'.xlsx')
    worksheet = workbook.add_worksheet()
    style_align_right = workbook.add_format({'align': 'right', 'bold': True, 'font_size': 10})
    style_align_center = workbook.add_format({'align': 'center', 'bold': True, 'font_size': 10})
    style_align_center_border = workbook.add_format({'align': 'center', 'bold': True, 'border': 1})
    format1 = workbook.add_format({'num_format': '#,##0.00'})
    border = workbook.add_format({'border': 1})
    worksheet.write('D1', 'Приложение 1', style_align_right)
    worksheet.write('D2','к Договору на обслуживание в рамках зарплатного проекта', style_align_right)
    worksheet.write('D3','от «___»_____________20__г.', style_align_right)
    worksheet.write('C6','Ведомость о зачислении денежных средств на счета Сотрудников', style_align_center)
    worksheet.write('C7','со Счета Клиента в Банке № 1130 0200 0018 2126', style_align_center)
    worksheet.write('C8','за '+datetime.datetime.today().strftime("%d-%m-%Y"), style_align_center)
    worksheet.write('A11','№ п/п', style_align_center_border)
    worksheet.write('B11','ФИО работника', style_align_center_border)
    worksheet.write('C11','№ счета работника', style_align_center_border)
    worksheet.write('D11','Сумма, сом', style_align_center_border)

    worksheet.set_column('D:D', 18, format1)
    worksheet.set_column('B:B', 38, None)
    #worksheet.write_string(1, 0, '', cell_format)
    worksheet.set_column('C:C', 20, None)
    worksheet.set_column('A:A', 5, None)
    n=1
    rows=11
    col=0
    summa = 0

    data = pd.read_excel (r'C:\дсп\Аванс за '+mon+' '+year+' г. на карточку.xlsx', header=None, names=['Number', 'Sum'])

    for index, row in data.iterrows():
        ch_num = row['Number']
        data = accounts.objects.get(ch_account=ch_num)
        k_acc = data.k_account
        name = data.fio
        sum = row['Sum']
        summ = float('{:.2f}'.format(sum))

        worksheet.write(rows,col,n, border)
        worksheet.write(rows,col+1,name, border)
        worksheet.write(rows,col+2,str(data.k_account), border)
        worksheet.write(rows,col+3,summ, border)
        rows=rows+1
        col=0
        n=n+1
        summa = summa+summ
    worksheet.write(rows,3,float('{:.2f}'.format(summa)))
    worksheet.write(rows+2,0,'Сумма')
    worksheet.write(rows+4,0,'Председатель Правления')
    worksheet.write(rows+4,2,'Жунушалиев Д.Т.')
    worksheet.write(rows+5,3,'МП')
    worksheet.write(rows+6,0,'Главный бухгалтер')
    worksheet.write(rows+6,2,'Шеркулова А.Т.')
    worksheet.write(rows+8,0,'Отметка об исполнении Банка')
    worksheet.write(rows+10,0,'Уполномоченное лицо/лица Банка')
    worksheet.write(rows+10,2,'МП')
    workbook.close()
    return render (request, 'zp_avans/result.html', {'k_account': k_acc, 'name': name, 'sum': summ})
