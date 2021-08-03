from django.db import models

# Create your models here.
class accounts(models.Model):
    fio = models.TextField()
    k_account = models.IntegerField()
    ch_account = models.IntegerField()

    def __str__(self):
        return self.fio

class months(models.Model):
    eng = models.CharField(max_length=120)
    rus = models.CharField(max_length=120)

    def __str__(self):
        return self.eng
