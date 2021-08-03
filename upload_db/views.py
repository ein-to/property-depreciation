from django.shortcuts import render
from .models import main_t, amort_t, change_bal_price, branch_id, company_id, employee_id, depart
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
def upload(request):

    data = pd.read_excel (r'C:\virtualenv\hello\projects\osnov_sred\OS1.xlsx')
    data2 = data.fillna(0)
    for index, row in data2.iterrows():
        name = row['name']
        inv = row['inv']
        bal_price = row['bal_price']
        type_id = row['type_id']
        amort_month = row['amort_month']
        izm = row['izm']
        dop_month = row['dop_month']
        emp_id = row['empl_id']
        kol_month = row['kol_month']
        amort_sum = row['amort_sum']
        amort_sum_month = row['amort_m_s']
        perehod_m_s = row['perehod_m_s']
        company_id = row['company_id']
        branch_id = row['branch_id']
        pur_date = row['pur_date']
        date_vvod = row['date_vvod']
        id_oborud = row['id']
        #date_spisan = row['date_spisan']
        #type_spisan = row['type_spisan']
        #spisan_comm = row['spisan_comm']

        data1 = main_t()
        data1.name = name
        data1.inv = inv
        data1.bal_price = bal_price
        data1.type_id = type_id
        data1.amort_month = amort_month
        data1.izm = izm
        data1.dop_month = dop_month
        data1.emp_id = emp_id
        data1.kol_month = kol_month
        data1.amort_sum = amort_sum
        data1.amort_sum_month = amort_sum_month
        data1.perehod_m_s = perehod_m_s
        data1.company_id = company_id
        data1.branch_id = branch_id
        data1.pur_date = pur_date
        data1.date_vvod = date_vvod
        data1.id_oborud = id_oborud
        #data1.date_spisan = date_spisan
        #data1.type_spisan = type_spisan
        #data1.spisan_comm = spisan_comm
        data1.save()

    return render (request, 'upload_db/test.html', {'name': name, 'name1': data1.name})

def data(request):
    return render (request, 'upload_db/data.html')

def upload_amort_history(request):

    data = pd.read_excel (r'C:\virtualenv\hello\projects\osnov_sred\export.xlsx')
    data.fillna(0)

    for index, row in data.iterrows():
        id_oborud = row['MAIN_ID']
        date_amort = row['DATE_AMORT']
        amort_sum_month = row['MONTH_SUM']
        ost_sum = row['OST_SUM']
        amort_sum = row['SUM_AMORT']
        norm_months = row['NORM_M']
        bal_price = row['BAL_PRICE']

        data1 = amort_t()
        data1.id_oborud = id_oborud
        data1.date_amort = date_amort
        data1.amort_sum_month = amort_sum_month
        data1.ost_sum = ost_sum
        data1.amort_sum = amort_sum
        data1.norm_months = norm_months
        data1.bal_price = bal_price
        data1.save()

    return render(request, 'upload_db/test.html', {'name': id_oborud, 'name1': bal_price})

def upload_change_bal_price(request):

    data = pd.read_excel (r'C:\virtualenv\hello\projects\osnov_sred\bal_price.xlsx')
    data.fillna(0)

    for index, row in data.iterrows():
        id_oborud = row['MAIN_ID']
        change_id = row['TYPE']
        name = row['COMM']
        summ = row['SUMMA']
        date = row['DATE_TIME']
        summ_before = row['SUMMA_DO']

        data1 = change_bal_price()
        data1.id_oborud = id_oborud
        data1.change_id = change_id
        data1.name = name
        data1.summ = summ
        data1.date = date
        data1.summ_before = summ_before
        data1.save()

    return render(request, 'upload_db/test.html', {'name': id_oborud, 'name1': summ})

def upload_spisan(request):
    data = pd.read_excel (r'C:\virtualenv\hello\projects\osnov_sred\OS1_spisan.xlsx')
    data1 = data.fillna(0)
    for index, row in data1.iterrows():
        id = row['id']
        m = main_t.objects.get(id_oborud=id)
        m.date_spisan = row['date_spisan']
        m.type_spisan = row['type_spisan']
        m.spisan_comm = row['spisan_comm']
        m.save()

    return render(request, 'main_os/test.html')


def delete_data_main_t(request):
    main_t.objects.all().delete()
    return render(request, 'upload_db/delete.html')

def delete_data_amort_t(request):
    amort_t.objects.all().delete()
    return render(request, 'upload_db/delete.html')

def upload_employees(request):
    data = pd.read_excel (r'C:\virtualenv\hello\projects\osnov_sred\employee.xlsx')
    data.fillna(0)
    for index, row in data.iterrows():
        emp_id1 = row['ID']
        depart_id1 = row['DEPART_ID']
        name1 = row['F_NAME']
        surname1 = row['S_NAME']
        lastname1 = row['L_NAME']

        data1 = employee_id()
        data1.emp_id = emp_id1
        data1.depart_id = depart_id1
        data1.name = name1
        data1.surname = surname1
        data1.lastname = lastname1
        data1.save()

    return render(request, 'main_os/test.html')
