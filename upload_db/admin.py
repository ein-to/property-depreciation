from django.contrib import admin

# Register your models here.
from .models import main_t, amort_t, change_bal_price, type_id, type_spisan, company_id

admin.site.register(main_t)
admin.site.register(amort_t)
admin.site.register(change_bal_price)
admin.site.register(type_id)
admin.site.register(type_spisan)
admin.site.register(company_id)
#admin.site.register(months)
