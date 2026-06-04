from django.db import models
from django.contrib.auth.models import User

# ==========================================
# БАЗОВЫЙ СПРАВОЧНИК (По ТЗ: 3 обязательных поля)
# ==========================================

class BaseDirectory(models.Model):
    directory_name = models.CharField(max_length=100, verbose_name="Название справочника", editable=False)
    name = models.CharField(max_length=100, verbose_name="Название")
    description = models.TextField(blank=True, verbose_name="Описание")

    class Meta:
        abstract = True  # Шаблон, не создает отдельную таблицу

    def save(self, *args, **kwargs):
        if not self.directory_name:
            self.directory_name = self._meta.verbose_name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Конкретные справочники проекта
class VehicleModel(BaseDirectory):
    class Meta: verbose_name = "Модель техники"; verbose_name_plural = "Справочник: Модели техники"

class EngineModel(BaseDirectory):
    class Meta: verbose_name = "Модель двигателя"; verbose_name_plural = "Справочник: Модели двигателей"

class TransmissionModel(BaseDirectory):
    class Meta: verbose_name = "Модель трансмиссии"; verbose_name_plural = "Справочник: Модели трансмиссий"

class DriveAxleModel(BaseDirectory):
    class Meta: verbose_name = "Модель ведущего моста"; verbose_name_plural = "Справочник: Модели ведущих мостов"

class SteerAxleModel(BaseDirectory):
    class Meta: verbose_name = "Модель управляемого моста"; verbose_name_plural = "Справочник: Модели управляемых мостов"

class MaintenanceType(BaseDirectory):
    class Meta: verbose_name = "Вид ТО"; verbose_name_plural = "Справочник: Виды ТО"

class FailureNode(BaseDirectory):
    class Meta: verbose_name = "Узел отказа"; verbose_name_plural = "Справочник: Узлы отказа"

class RecoveryMethod(BaseDirectory):
    class Meta: verbose_name = "Способ восстановления"; verbose_name_plural = "Справочник: Способы восстановления"

class ServiceCompany(BaseDirectory):
    # Связываем сервисную компанию с пользователем Django (для ограничения прав)
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="service_profile")
    
    class Meta: verbose_name = "Сервисная организация"; verbose_name_plural = "Справочник: Сервисные организации"


# ==========================================
# КЛЮЧЕВАЯ СУЩНОСТЬ: МАШИНА
# ==========================================

class Machine(models.Model):
    # Поля 1-10 (Техническая комплектация, доступная Гостю по ТЗ)
    vehicle_model = models.ForeignKey(VehicleModel, on_delete=models.PROTECT, verbose_name="Модель техники")
    serial_number = models.CharField(max_length=100, unique=True, verbose_name="Зав. № машины")
    engine_model = models.ForeignKey(EngineModel, on_delete=models.PROTECT, verbose_name="Модель двигателя")
    engine_serial_number = models.CharField(max_length=100, verbose_name="Зав. № двигателя")
    transmission_model = models.ForeignKey(TransmissionModel, on_delete=models.PROTECT, verbose_name="Модель трансмиссии")
    transmission_serial_number = models.CharField(max_length=100, verbose_name="Зав. № трансмиссии")
    drive_axle_model = models.ForeignKey(DriveAxleModel, on_delete=models.PROTECT, verbose_name="Модель ведущего моста")
    drive_axle_serial_number = models.CharField(max_length=100, verbose_name="Зав. № ведущего моста")
    steer_axle_model = models.ForeignKey(SteerAxleModel, on_delete=models.PROTECT, verbose_name="Модель управляемого моста")
    steer_axle_serial_number = models.CharField(max_length=100, verbose_name="Зав. № управляемого моста")
    additional_options = models.TextField(blank=True, default="Стандарт", verbose_name="Комплектация (доп. опции)")

    
    # Специфичные данные (Конфиденциальные, скрыты от Гостя)
    supply_contract = models.CharField(max_length=200, verbose_name="Договор поставки №, дата")
    shipping_date = models.DateField(verbose_name="Дата отгрузки с завода")
    consignee = models.CharField(max_length=255, verbose_name="Грузополучатель (конечный потребитель)")
    operation_location = models.CharField(max_length=255, verbose_name="Место эксплуатации (адрес)")
    
    # Привязка к роли "Клиент" и "Сервисная организация"
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name="machines", verbose_name="Клиент")
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.PROTECT, related_name="machines", verbose_name="Сервисная организация")

    class Meta:
        verbose_name = "Машина"
        verbose_name_plural = "Машины"
        ordering = ['shipping_date']

    def __str__(self):
        return f"{self.vehicle_model.name} (Зав. № {self.serial_number})"


# ==========================================
# СУЩНОСТЬ: ТО (Техническое обслуживание)
# ==========================================

class Maintenance(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="maintenances", verbose_name="Машина")
    type = models.ForeignKey(MaintenanceType, on_delete=models.PROTECT, verbose_name="Вид ТО")
    date = models.DateField(verbose_name="Дата проведения ТО")
    operating_hours = models.IntegerField(verbose_name="Наработка, м/час")
    order_number = models.CharField(max_length=100, verbose_name="№ заказ-наряда")
    order_date = models.DateField(verbose_name="Дата заказ-наряда")
    service_company = models.ForeignKey(ServiceCompany, on_delete=models.PROTECT, verbose_name="Организация, проводившая ТО")

    class Meta:
        verbose_name = "Техническое обслуживание"
        verbose_name_plural = "Технические обслуживания"
        ordering = ['-date']

    def __str__(self):
        return f"{self.type.name} - {self.machine.serial_number} ({self.date})"


# ==========================================
# СУЩНОСТЬ: РЕКЛАМАЦИИ
# ==========================================

class Reclamation(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE, related_name="reclamations", verbose_name="Машина")
    refusal_date = models.DateField(verbose_name="Дата отказа")
    operating_hours = models.IntegerField(verbose_name="Наработка, м/час")
    failure_node = models.ForeignKey(FailureNode, on_delete=models.PROTECT, verbose_name="Узел отказа")
    failure_description = models.TextField(verbose_name="Описание отказа")
    recovery_method = models.ForeignKey(RecoveryMethod, on_delete=models.PROTECT, verbose_name="Способ восстановления")
    parts_used = models.TextField(blank=True, verbose_name="Используемые запасные части")
    recovery_date = models.DateField(verbose_name="Дата восстановления")

    class Meta:
        verbose_name = "Рекламация"
        verbose_name_plural = "Рекламации"
        ordering = ['-refusal_date']

    # По ТЗ: вычисляемый срок устранения (время простоя техники)
    @property
    def downtime_days(self):
        if self.recovery_date and self.refusal_date:
            return (self.recovery_date - self.refusal_date).days
        return 0

    def __str__(self):
        return f"Отказ {self.failure_node.name} на машине {self.machine.serial_number} ({self.refusal_date})"
