from django.contrib import admin

from .models import ShootNumbers, DecidedNumbers, FormInput

# Register your models here.
@admin.register(ShootNumbers)
class ShootNumbersAdmin(admin.ModelAdmin):
    list_display = ['shooter','lottos','update_date','predict_total_value','predict_total_25','predict_total_75','origin_nums','except_nums','band']
    list_per_page = 20

@admin.register(DecidedNumbers)
class DecidedNumbersAdmin(admin.ModelAdmin):
    list_display = ['count', 'shotDate', 'one', 'two', 'three','four','five','six', 'total', 'band']
    list_per_page = 20
    list_filter = ['band','count']

@admin.register(FormInput)
class FormInputAdmin(admin.ModelAdmin):
    list_display = ['shooter', 'shot_count', 'update_date']
    list_per_page = 20
