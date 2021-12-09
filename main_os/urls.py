"""osnov_sred URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name = 'index'),
    path('', views.user_login, name = 'user_login'),
    path('logout/', views.logout_request, name='logout_request'),
    path('amortizacia/', views.amortizacia, name='amortizacia'),
    path('amort_template/', views.amort_template, name='amort_template'),
    path('test/', views.test, name='test'),
    path('reports/<int:id>', views.reports, name='reports'),
    path('reports/report', views.report, name='report'),
    path('reports/report_spis_real', views.report_spis_real, name='report_spis_real'),
    path('reports/report_general', views.report_general, name='report_general'),
    path('reports/report_prbo', views.report_prbo, name='report_prbo'),
    path('reports/report_inventory', views.report_inventory, name='report_inventory'),
    path('ch_bal_price/', views.ch_bal_price, name='ch_bal_price'),
    path('ch_bal_price/change_bal_price_def', views.change_bal_price_def, name='change_bal_price_def'),
    path('mbp/', views.mbp, name='mbp'),
    path('mebel/', views.mebel, name='mebel'),
    path('comp/', views.comp, name='comp'),
    path('cap/', views.cap, name='cap'),
    path('transport/', views.transport, name='transport'),
    path('zdaniya/', views.zdaniya, name='zdaniya'),
    path('oborudovanie/', views.oborudovanie, name='oborudovanie'),
    path('nem_actives/', views.nem_actives, name='nem_actives'),
    path('add_os/', views.add_os, name='add_os'),
    path('add_os_finish/', views.add_os_finish, name='add_os_finish'),
    path('<int:id>/', views.directory_list, name='directory_list'),
    path('directory_list_add/<int:id>', views.directory_list_add, name='directory_list_add'),
    path('depart_change/<int:id>', views.depart_change, name='depart_change'),
    path('depart_disable/<int:id>', views.depart_disable, name='depart_disable'),
    path('search/', views.search, name='search'),
    path('spis_real/', views.spis_real, name='spis_real'),
    path('def_spis_real/', views.def_spis_real, name='def_spis_real'),
    path('сards/', views.cards, name='cards'),
    path('сards_change/', views.cards_change, name='cards_change'),
    path('сards_pdf/', views.cards_pdf, name='cards_pdf'),
    path('сards_del_item/<int:inv>', views.cards_del_item, name='cards_del_item'),
    path('сards_add_item/', views.cards_add_item, name='cards_add_item'),
    path('employee_disable/<int:id>', views.employee_disable, name='employee_disable'),
    path('employee_change/<int:id>', views.employee_change, name='employee_change'),
    path('get_history_item/', views.get_history_item, name='get_history_item'),
    path('item_movement/', views.item_movement, name='item_movement'),
    path('invoice/', views.invoice, name='invoice'),
    path('invoice_detail/<int:invoice_number>', views.invoice_detail, name='invoice_detail'),
    path('invoice_pdf/<int:invoice_number>', views.invoice_pdf, name='invoice_pdf'),
    path('change_branch_id', views.change_branch_id, name='change_branch_id'),
]
