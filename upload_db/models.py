from django.db import models

# Create your models here.
class main_t(models.Model):
    id_oborud = models.IntegerField(null=True)
    name = models.CharField(max_length=120)
    pur_date = models.DateField(null=True)
    inv = models.IntegerField()
    bal_price = models.FloatField()
    type_id = models.IntegerField()
    amort_month = models.FloatField()
    date_vvod = models.DateField(null=True)
    izm = models.IntegerField(null=True)
    dop_month = models.IntegerField(null=True)
    emp_id = models.IntegerField(null=True)
    kol_month = models.IntegerField(null=True)
    amort_sum = models.FloatField()
    amort_sum_month = models.FloatField()
    perehod_m_s = models.FloatField(null=True)
    company_id = models.IntegerField(null=True)
    branch_id = models.IntegerField()
    date_spisan = models.DateField(null=True)
    type_spisan = models.IntegerField(null=True)
    spisan_comm = models.CharField(max_length=120, null=True)

    def __str__(self):
        return self.name

class amort_t(models.Model):
    id_oborud = models.IntegerField()
    date_amort = models.DateField()
    amort_sum_month = models.FloatField()
    ost_sum = models.FloatField()
    amort_sum = models.FloatField()
    norm_months = models.IntegerField()
    bal_price = models.FloatField()
    ostatok_sroka = models.IntegerField(null=True)

    def __str__(self):
        return str(self.id_oborud)

class change_bal_price(models.Model):
    id_oborud = models.IntegerField()
    change_id = models.IntegerField()
    name = models.CharField(max_length=120)
    summ = models.FloatField()
    date = models.DateField()
    summ_before = models. FloatField()

    def __str__(self):
        return self.name

class type_id(models.Model):
    type = models.CharField(max_length=120)
    type_id = models.IntegerField()
    srok_months = models.IntegerField()

    def __str__(self):
        return self.type

class type_spisan(models.Model):
    type_name = models.CharField(max_length=120)
    type_spisan_id = models.IntegerField()

    def __str__(self):
        return self.type_name

class company_id(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

    def __str__(self):
        return self.surname

class branch_id(models.Model):
    branch_id = models.IntegerField()
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class depart(models.Model):
    branch_id = models.ForeignKey(branch_id, on_delete=models.CASCADE, default=1)
    depart_id = models.IntegerField()
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class employee_id(models.Model):
    emp_id = models.IntegerField()
    branch_id = models.ForeignKey(branch_id, on_delete=models.CASCADE, default=1)
    depart_id = models.IntegerField(null=True)
    name = models.CharField(max_length=60)
    surname = models.CharField(max_length=60, null=True)
    lastname = models.CharField(max_length=60, null=True)
    active = models.IntegerField(null=True)

    def __str__(self):
        return self.surname


class history_item(models.Model):
    id_oborud = models.IntegerField()
    inv = models.IntegerField()
    name_item = models.CharField(max_length=120, null=True)
    date_moving = models.DateField()
    ex_emp = models.IntegerField()
    new_emp = models.IntegerField()
    username = models.CharField(max_length=60, null=True)
    invoice_number = models.IntegerField(null=True)

    def __str__(self):
        return self.inv
