from django.contrib import admin
from .models import (
    VehicleModel, EngineModel, TransmissionModel, DriveAxleModel, SteerAxleModel,
    MaintenanceType, FailureNode, RecoveryMethod, ServiceCompany,
    Machine, Maintenance, Reclamation
)

# --- Настройка отображения МАШИН ---
@admin.register(Machine)
class MachineAdmin(admin.ModelAdmin):
    # Какие колонки показывать в списке машин
    list_display = ('serial_number', 'vehicle_model', 'engine_model', 'client', 'service_company', 'shipping_date')
    # По каким полям делать поиск (поиск по зав. номеру машины очень важен)
    search_fields = ('serial_number', 'engine_serial_number', 'consignee')
    # Фильтры в правой панели админки
    list_filter = ('vehicle_model', 'engine_model', 'service_company')

# --- Настройка отображения ТО ---
@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('machine', 'type', 'date', 'operating_hours', 'service_company')
    search_fields = ('machine__serial_number', 'order_number')
    list_filter = ('type', 'service_company')

# --- Настройка отображения РЕКЛАМАЦИЙ ---
@admin.register(Reclamation)
class ReclamationAdmin(admin.ModelAdmin):
    list_display = ('machine', 'refusal_date', 'failure_node', 'recovery_method', 'recovery_date', 'get_downtime')
    search_fields = ('machine__serial_number', 'failure_description')
    list_filter = ('failure_node', 'recovery_method')

    # Выводим наше вычисляемое свойство дней простоя в список
    def get_downtime(self, obj):
        return f"{obj.downtime_days} дн."
    get_downtime.short_description = "Время простоя"

# --- Регистрация простых Справочников (чтобы заполнять их из админки) ---
admin.site.register(VehicleModel)
admin.site.register(EngineModel)
admin.site.register(TransmissionModel)
admin.site.register(DriveAxleModel)
admin.site.register(SteerAxleModel)
admin.site.register(MaintenanceType)
admin.site.register(FailureNode)
admin.site.register(RecoveryMethod)
admin.site.register(ServiceCompany)
