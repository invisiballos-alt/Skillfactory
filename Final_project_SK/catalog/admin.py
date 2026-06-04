from django.contrib import admin
from .models import (
    VehicleModel, EngineModel, TransmissionModel, DriveAxleModel, SteerAxleModel,
    MaintenanceType, FailureNode, RecoveryMethod, ServiceCompany,
    Machine, Maintenance, Reclamation
)
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    list_display = ('serial_number', 'vehicle_model', 'engine_model', 'client', 'service_company', 'shipping_date')
    search_fields = ('serial_number', 'engine_serial_number', 'consignee')
    list_filter = ('vehicle_model', 'engine_model', 'service_company')
    
    # Группируем поля по блокам (Fieldsets)
    fieldsets = (
        ('Техническая спецификация (Доступно Гостю)', {
            'fields': (
                'vehicle_model', 'serial_number',  
                'engine_model', 'engine_serial_number',
                'transmission_model', 'transmission_serial_number',
                'drive_axle_model', 'drive_axle_serial_number',
                'steer_axle_model', 'steer_axle_serial_number',
                'additional_options' # то самое доп. поле со скриншота!
            )
        }),
        ('Информация о поставке и эксплуатации (Скрыто от Гостя)', {
            'fields': ('supply_contract', 'shipping_date', 'consignee', 'operation_location')
        }),
        ('Управление доступом', {
            'fields': ('client', 'service_company')
        }),
    )

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'type', 'order_number', 'order_date', 'date', 'service_company')
    search_fields = ('machine__serial_number', 'order_number')
    list_filter = ('type', 'service_company')
    
    # Хак: Если зашел автомеханик из сервиса, он не сможет подделать поле сервисной компании
    def save_model(self, request, obj, form, change):
        if hasattr(request.user, 'service_profile') and not request.user.is_superuser:
            obj.service_company = request.user.service_profile
        super().save_model(request, obj, form, change)

@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('machine', 'refusal_date', 'failure_node', 'recovery_date', 'get_downtime')
    search_fields = ('machine__serial_number', 'failure_description')
    list_filter = ('failure_node', 'recovery_method')

    def get_downtime(self, obj):
        return f"{obj.downtime_days} дн."
    get_downtime.short_description = "Время простоя"

# Регистрация справочников (оставляем без изменений)
admin.site.register(VehicleModel)
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteerAxleModel)
admin.site.register(MaintenanceType)
admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)
admin.site.register(ServiceCompany)

# 1. Отменяем стандартную регистрацию пользователей в админке
admin.site.unregister(User)

# 2. Создаем кастомный класс для отображения
@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    # Этот метод заставляет выпадающие списки ForeignKey показывать имя компании
    def get_formset(self, request, obj=None, **kwargs):
        User.__str__ = lambda self_user: self_user.first_name if self_user.first_name else self_user.username
        return super().get_formset(request, obj, **kwargs)

    # Этот метод меняет отображение в выпадающих списках на обычных формах редактирования
    def get_queryset(self, request):
        User.__str__ = lambda self_user: self_user.first_name if self_user.first_name else self_user.username
        return super().get_queryset(request)
