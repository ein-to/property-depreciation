from django import template
from upload_db.models import employee_id, main_t
from datetime import datetime, date

register = template.Library()

@register.filter
def add_zeros_inv(value):
    if len(str(value)) < 8:
        inv = '{:08}'.format(value)
    else:
        inv = value
    return inv

@register.filter
def get_name(value):
    if value != 1:
        emp = employee_id.objects.get(emp_id=value)
        name = emp.surname+' '+emp.name[0]+'.'+emp.lastname[0]
    if value == 1:
        name = 'Склад'
    if value == 682:
        name = 'ОИТ'
    return name

@register.filter
def date_format(value):
    date = datetime.strftime(value, '%d-%m-%Y')
    return date

@register.filter
def show_emp_name(value):
    m = main_t.objects.get(inv=value)
    try:
        emp = employee_id.objects.get(emp_id=m.emp_id)
        if emp.lastname != '':
            name = emp.surname + ' ' + emp.name[0] + '.' + emp.lastname[0] +'.'
        else:
            name = emp.surname + ' ' + emp.name[0] + '.'
        if emp.name == 'Склад' or emp.name == 'ОИТ':
            name = emp.name
    except:
        name = ''
    return name

@register.filter
def show_spisan_date(value):
    m = main_t.objects.get(inv=value)
    if m.date_spisan != None:
        date = datetime.strftime(m.date_spisan, '%d-%m-%Y')
    else:
        date = ''
    return date

@register.filter
def pur_date(value):
    date = main_t.objects.get(id_oborud=value)
    date = date.pur_date
    date = datetime.strftime(date, '%d-%m-%Y')
    return date

@register.filter
def bal_price(value):
    price = main_t.objects.get(id_oborud=value)
    price = price.bal_price
    return price

@register.filter
def ifnull(value):
    if value is None:
        invoice_number = 0
    else:
        invoice_number = value
    return invoice_number
